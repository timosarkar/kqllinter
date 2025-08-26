{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.gradle
  ];

  shellHook = ''
  ./gradlew -p app build --refresh-dependencies
  ./gradlew -p app run
  '';
}

