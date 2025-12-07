import os
from ignis import utils
from ignis.css_manager import CssInfoPath, CssManager
from desktop.windows.bar import Bar
from desktop.windows.osd import Osd
from desktop.windows.search import SearchList

css_manager=CssManager.get_default()

def patch_style_scss(path):
    with open(path) as file:
        string = file.read()

        return utils.sass_compile(
            string=string, extra_args=["--load-path", utils.get_current_dir()]
        )

css_manager.apply_css(
    CssInfoPath(
        name="main",
        path=os.path.join(utils.get_current_dir(), "style.scss"),
        priority="user",
        compiler_function=patch_style_scss,
    )
)

print(css_manager.list_css_infos())

Bar(0)
Osd()
SearchList()
