import os
import sys
import subprocess
import importlib.resources
import importlib.metadata # For finding package root
from ignis.cli import init

def main():
    # Get the distribution information for the installed package
    dist = importlib.metadata.distribution('ignis_desktop')
    # The 'locate_file' method can give us the path to the installed package root
    # This will be something like /nix/store/.../lib/pythonX.Y/site-packages/ignis_desktop
    config_path = str(dist.locate_file('desktop')) # Locate the 'desktop' folder within the installed package
    print(config_path)
    init(config=config_path)
#     # This script should be installed as part of the ignis_desktop package.
#     # We need to find the root of the installed ignis_desktop package.
#     # importlib.resources.files() can help find files within the package.
#     try:
#         # Get the distribution information for the installed package
#         dist = importlib.metadata.distribution('ignis_desktop')
#         # The 'locate_file' method can give us the path to the installed package root
#         # This will be something like /nix/store/.../lib/pythonX.Y/site-packages/ignis_desktop
#         config_path = str(dist.locate_file('desktop')) # Locate the 'desktop' folder within the installed package
#
#         # Look for 'ignis' in the PATH
#         ignis_bin = os.environ.get("IGNIS_BIN_PATH") # Allow override via env var
#         if not ignis_bin:
#             ignis_bin = find_executable("ignis") # Search in PATH
#
#         if not ignis_bin:
#             print("Error: 'ignis' executable not found in PATH or IGNIS_BIN_PATH.", file=sys.stderr)
#             sys.exit(1)
#
#         # Construct the command to execute
#         cmd = [ignis_bin, "init", "-c", config_path]
#
#         print(f"Executing: {' '.join(cmd)}")
#         subprocess.run(cmd, check=True)
#
#     except importlib.metadata.PackageNotFoundError:
#         print("Error: 'ignis_desktop' package not found. Is it installed?", file=sys.stderr)
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error executing ignis-desktop: {e}", file=sys.stderr)
#         sys.exit(1)
#
# def find_executable(executable, path=None):
#     """Finds an executable in the system's PATH."""
#     if path is None:
#         path = os.environ.get("PATH", os.defpath)
#     paths = path.split(os.pathsep)
#     base, ext = os.path.splitext(executable)
#     if (ext and os.path.isfile(executable)):
#         return executable
#     for p in paths:
#         f = os.path.join(p, executable)
#         if os.path.isfile(f) and os.access(f, os.X_OK): # Check for execute permission
#             return f
#         if not ext and os.path.isfile(f + ".exe"): # Windows executables
#             return f + ".exe"
#     return None

if __name__ == "__main__":
    sys.exit(main())
