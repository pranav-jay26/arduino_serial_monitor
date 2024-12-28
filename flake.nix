{
  description = "A simple Python-based serial monitor for Arduino microcontrollers";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in {
        # Development shell
        devShells.default = pkgs.mkShell {
          buildInputs = with pythonPackages; [
            matplotlib
            pyserial
            click
            # Add other dependencies as needed
          ];
        };

        # Python package
        packages.default = pythonPackages.buildPythonApplication {
          pname = "arduino_serial_monitor";
          version = "0.1.0";

          format = "pyproject";
          src = ./.;

          nativeBuildInputs = with pkgs.python3Packages; [
            setuptools
            wheel
          ];

          propagatedBuildInputs = with pythonPackages; [
            matplotlib
            pyserial
            click
            # Add other dependencies as needed
          ];
        };
      }
    );
}

