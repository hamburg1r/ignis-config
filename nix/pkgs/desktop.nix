{ ignisDeps, pkgs, src }:
pkgs.python3Packages.buildPythonApplication {
  pname = "ignis-desktop";
  version = "0.1.0";
  src = src;
  format = "setuptools";
  doCheck = false;
  
  # propagatedBuildInputs = [
  #   ignisDeps
  # ];
  
  nativeBuildInputs = [
    ignisDeps
    pkgs.python3Packages.setuptools
    pkgs.gobject-introspection
  ];
  
  buildInputs = [
    pkgs.gtk3
    pkgs.gtk4
    pkgs.glib
    pkgs.gtk4-layer-shell
  ];
  
  # The key: inherit GI_TYPELIB_PATH from ignisDeps

}
