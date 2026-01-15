{
  description = "Flake utils demo";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    ignis = {
      url = "github:ignis-sh/ignis";
      # ! Important to override
      # Nix will not allow overriding dependencies if the input
      # doesn't follow your system pkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ignis }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        ignisDeps = ignis.packages.${system}.ignis.override {
          enableAudioService = true;
          enableBluetoothService = true;
          enableNetworkService = true;
          enableRecorderService = true;

          extraPackages = with pkgs; [
            dart-sass
          ];
        };

        ignis-desktop = import ./nix/bin/desktop.nix {
          inherit pkgs ignisDeps;
          src = self;
        };
      in
      rec {
        packages = rec {
          inherit ignis-desktop;
          ignis = ignisDeps;
          default = ignis-desktop;
        };
        apps = rec {
          default = flake-utils.lib.mkApp { drv = packages.default; };
        };
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            gtk3
            gtk4
            glib
          ];
          nativeBuildInputs = with pkgs; [
            (python3.withPackages(ps: with ps; [
              ipython
              ignisDeps
              gobject-introspection
              pygobject3
              pygobject-stubs
            ]))
            basedpyright
            gobject-introspection
          ];
          shellHook = ''
            export GI_TYPELIB_PATH="${pkgs.gtk3}/lib/girepository-1.0:${pkgs.gtk4}/lib/girepository-1.0:${pkgs.glib}/lib/girepository-1.0:$GI_TYPELIB_PATH"
          '';
        };
      }
    ) //
    {
nixosModules =
          let mod = import ./nix/modules/nixos { inherit self; };
          in {
            default = mod;
            ignis-desktop = mod;
          };
        homeManagerModules =
          let mod = import ./nix/modules/home-manager { inherit self; };
          in {
            default = mod;
            ignis-desktop = mod;
          };
    };
}
