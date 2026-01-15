{ self, ... }: { lib, config, pkgs, ... }:
let
  cfg = config.programs.ignis-desktop;
in
{
  options.programs.ignis-desktop = with lib; {
    enable = mkEnableOption "Enable ignis desktop";
    package = mkOption {
      type = types.package;
      default = self.packages.${pkgs.system}.ignis-desktop;
      description = "The ignis-desktop package to install.";
    };
  };

  config = lib.mkIf cfg.enable {
    home.packages = [ cfg.package self.packages.${pkgs.system}.ignis ];
  };
}
