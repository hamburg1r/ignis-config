import os
import ignis
from ignis import utils
from ignis.css_manager import CssInfoPath, CssManager
from desktop.windows.bar import Bar
from desktop.windows.osd import Osd
from desktop.windows.search import SearchList
from desktop.windows.icons import IconBrowser
from desktop.windows.launcher import Launcher

css_manager = CssManager.get_default()

# --- SCSS Compilation Caching ---
scss_path = os.path.join(utils.get_current_dir(), "style.scss")
css_path = os.path.join(ignis.CACHE_DIR, "style.css")
scss_imports = [
    os.path.join(utils.get_current_dir(), "scss/general.scss"),
    os.path.join(utils.get_current_dir(), "scss/osd.scss"),
    os.path.join(utils.get_current_dir(), "scss/search.scss"),
    os.path.join(utils.get_current_dir(), "scss/settings.scss"),
]

def compile_scss():
    print("Compiling SCSS...")
    with open(scss_path) as file:
        string = file.read()
        compiled_css = utils.sass_compile(
            string=string, extra_args=["--load-path", utils.get_current_dir()]
        )
    with open(css_path, "w") as file:
        file.write(compiled_css)
    print("SCSS compiled.")

needs_recompile = True
if os.path.exists(css_path):
    try:
        css_mtime = os.path.getmtime(css_path)
        scss_mtime = os.path.getmtime(scss_path)
        if css_mtime > scss_mtime:
            needs_recompile = False
            for imp in scss_imports:
                if os.path.exists(imp) and os.path.getmtime(imp) > css_mtime:
                    needs_recompile = True
                    break
    except FileNotFoundError:
        needs_recompile = True

if needs_recompile:
    compile_scss()

css_manager.apply_css(
    CssInfoPath(
        name="main",
        path=css_path,
        priority="user",
    )
)
# --- End of SCSS Caching ---

print(css_manager.list_css_infos())

Bar(0)
Osd()
# IconBrowser()
