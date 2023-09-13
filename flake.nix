{
  description = "A small daemon for automatically controlling mpris compatible media players";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    #poetry2nix = {
    #  url = "github:nix-community/poetry2nix";
    #  inputs.nixpkgs.follows = "nixpkgs";
    #};
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
        {
          defaultPackage = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
          };
        });
}
