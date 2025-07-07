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
          extraPackages = [
            # Add extra packages if needed
          ];
        };

      in
      {
        packages = rec {
          # hello = pkgs.hello;
          # default = hello;
        };
        apps = rec {
          # hello = flake-utils.lib.mkApp { drv = self.packages.${system}.hello; };
          # default = hello;
        };
        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            (python3.withPackages(ps: with ps; [
              ignisDeps
            ]))
          ];
        };
      }
    );
}
