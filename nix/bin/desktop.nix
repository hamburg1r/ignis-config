{ pkgs, ignisDeps, src }:

pkgs.writeShellScriptBin "ignis-desktop" ''
  #!''${pkgs.runtimeShell}
  exec ${ignisDeps}/bin/ignis init -c ${src}/desktop
''
