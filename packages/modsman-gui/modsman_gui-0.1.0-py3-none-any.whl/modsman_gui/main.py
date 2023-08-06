import _thread
import asyncio
import os
import subprocess
import sys
from pathlib import Path

import traits.api as t
import traitsui.api as tui
from PyQt5.QtWidgets import QInputDialog
from modsman.common import Mod
from modsman.modlist import Modlist
from modsman.modsman import Modsman
from pyface.constant import OK
from pyface.directory_dialog import DirectoryDialog
from pyface.image_resource import ImageResource
from traitsui.list_str_adapter import ListStrAdapter


class ModAdapter(ListStrAdapter):
    def _get_text(self):
        mod: Mod = self.item
        return f"{mod.file_name}" if mod else None


def button_item(name, label):
    return tui.UItem(name, label=label, springy=True, enabled_when="locked == False")


class ModsmanGui(t.HasTraits):
    modlist = t.Instance(Modlist)
    mods = t.Property(
        lambda it: sorted(
            it.modlist.mods.values(), key=lambda mod: mod.file_name.lower()
        ),
        depends_on="modlist",
    )
    n_mods = t.Property(lambda it: len(it.mods), depends_on="mods")
    game_version = t.Property(
        lambda it: it.modlist.config.game_version, depends_on="modlist"
    )

    selected_mods = t.List(Mod)
    status = t.Str()
    locked = t.Bool(False)

    remove = t.Button()
    upgrade = t.Button()
    reinstall = t.Button()
    discover = t.Button()
    open_folder = t.Button()

    traits_view = tui.View(
        tui.VGroup(
            tui.HGroup(
                tui.UReadonly(name="n_mods", format_str="%d mods tracked"),
                tui.Spring(),
                tui.UReadonly(name="game_version", format_str="MC %s"),
            ),
            tui.UReadonly(
                name="mods",
                editor=tui.ListStrEditor(
                    editable=False,
                    multi_select=True,
                    adapter=ModAdapter(),
                    selected="selected_mods",
                ),
                enabled_when="locked == False",
            ),
            tui.HGroup(
                button_item("remove", label="Remove selected"),
                button_item("upgrade", label="Upgrade selected"),
                button_item("reinstall", label="Reinstall selected"),
            ),
            tui.HGroup(
                button_item("discover", label="Check for installed mods"),
                button_item("open_folder", label="Open mods directory"),
            ),
            show_border=True,
        ),
        statusbar=[tui.StatusItem()],
        title="modsman-gui",
        icon=ImageResource("icon.png"),
        resizable=True,
    )

    def __init__(self, modlist):
        super().__init__()
        self.modlist = modlist

    def _remove_fired(self):
        project_ids = [mod.project_id for mod in self.selected_mods]

        async def task():
            with Modlist.load(self.modlist.path) as modlist:
                async for mod in Modsman(modlist).remove_mods(project_ids):
                    yield f"Deleted '{mod.file_name}'"
            self.modlist = modlist

        self._run_with_status(task(), "Removed")

    def _upgrade_fired(self):
        project_ids = [mod.project_id for mod in self.selected_mods]

        async def task():
            with Modlist.load(self.modlist.path) as modlist:
                async for mod, upgraded in Modsman(modlist).upgrade_mods(project_ids):
                    if upgraded:
                        yield f"Downloaded '{mod.file_name}'"
            self.modlist = modlist

        self._run_with_status(task(), "Upgraded")

    def _reinstall_fired(self):
        project_ids = [mod.project_id for mod in self.selected_mods]

        async def task():
            with Modlist.load(self.modlist.path) as modlist:
                async for mod in Modsman(modlist).reinstall_mods(project_ids):
                    yield f"Downloaded '{mod.file_name}'"
            self.modlist = modlist

        self._run_with_status(task(), "Reinstalled")

    def _discover_fired(self):
        async def task():
            self.status = "This may take a while..."
            with Modlist.load(self.modlist.path) as modlist:
                parent = modlist.path.parent
                jars = [str(g.relative_to(parent)) for g in parent.glob("*.jar")]

                exclude = {mod.file_name for mod in modlist.mods.values()}
                jars = [j for j in jars if j not in exclude]

                async for mod in Modsman(modlist).match_mods(jars):
                    yield f"Matched '{mod.file_name}'"

            self.modlist = modlist

        self._run_with_status(task(), "Matched")

    def _open_folder_fired(self):
        path = str(self.modlist.path.parent)
        if sys.platform.startswith("darwin"):
            subprocess.check_call(["open", path])
        elif sys.platform.startswith("linux"):
            subprocess.check_call(["xdg-open", path])
        elif sys.platform.startswith("win"):
            subprocess.check_call(["explorer", path])

    def _run_with_status(self, string_gen, verb):
        async def _run():
            count = 0
            async for log in string_gen:
                self.status = log
                count += 1
            if count != 1:
                self.status = f"{verb} {count} mods"
            self.locked = False

        self.locked = True
        _thread.start_new_thread(lambda: asyncio.run(_run()), ())


def run():
    path = None

    if len(sys.argv) >= 2:
        path = Path(sys.argv[1]).absolute()

    else:
        dir_dialog = DirectoryDialog()
        result = dir_dialog.open()
        if result is OK:
            path = Path(dir_dialog.path).absolute()
        else:
            exit(1)

    os.chdir(path)
    path = path.joinpath(".modlist.json")

    print(path.absolute())

    if path.is_file():
        ModsmanGui(Modlist.load(path)).configure_traits()
    elif not path.exists():
        ver, ok = QInputDialog.getText(None, "modsman-gui", "Enter a MC game version:")
        if ok:
            modlist = Modlist.init(path, ver)
            modlist.save()
            ModsmanGui(modlist).configure_traits()
        else:
            exit(1)
    else:
        exit(1)
