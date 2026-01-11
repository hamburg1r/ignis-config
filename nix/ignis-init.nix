{ pkgs, ignisDeps, src }:

pkgs.writeShellScriptBin "ignis-init-desktop" ''
  #!''${pkgs.runtimeShell}
  ${ignisDeps}/bin/ignis init -c ${src}/desktop
''
