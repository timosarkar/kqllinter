{pkgs ? import <nixpkgs>}:
pkgs.mkShell {
  buildInputs = [
    pkgs.llama-cpp
  ];
}