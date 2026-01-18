{ pkgs, src }:

pkgs.python3Packages.buildPythonApplication {
  pname = "ignis-desktop";
  version = "0.1.0";
  src = src;
  format = "setuptools";
  nativeBuildInputs = [
    pkgs.python3Packages.setuptools
  ];
}
