{
  description = "A small daemon for automatically controlling mpris compatible media players";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry.url = "github:nix-community/poetry2nix";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, poetry }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; overlays = [ poetry.overlay ]; };
        inherit (pkgs) poetry2nix;
      in {
        defaultPackage = poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          python = pkgs.python3;
        };
      }
    );
}
