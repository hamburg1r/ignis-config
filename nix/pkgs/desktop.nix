{ ignisDeps, pkgs, src }:
pkgs.python3Packages.buildPythonApplication {
  pname = "ignis-desktop";
  version = "0.1.0";
  src = src;
  format = "setuptools";
  doCheck = false;
  
  nativeBuildInputs = [
    pkgs.python3Packages.setuptools
    pkgs.makeWrapper
  ];

  postInstall = ''
    makeWrapper ${ignisDeps}/bin/ignis $out/bin/ignis-desktop \
      --add-flags "init -c $out/${pkgs.python3.sitePackages}/desktop"
  '';
}
