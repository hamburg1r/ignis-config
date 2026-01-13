
{ lib, config, pkgs, ... }:
let
  cfg = config.programs.ignis-desktop;
in
{
  options.programs.ignis-desktop = with lib; {
    enable = mkEnableOption "Enable ignis desktop";
    package = mkPackageOption pkgs "ignis-desktop" { };
  };

  config = lib.mkIf cfg.enable {
    environment.systemPackages = [ cfg.package ];
  };
}
