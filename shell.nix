let
  pkgs = import <nixpkgs> {};

  python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
      pybricks = pyfinal.callPackage ./pybricks.nix { };
      pybricksdev = pyfinal.callPackage ./pybricksdev.nix { };
    };
  };

in pkgs.mkShell {
  packages = with pkgs; [
    #(poetry.override { python3 = python310; })
    #(poetry.override { python3 = python; })

    (python.withPackages (python-pkgs: [
      python-pkgs.pybricks
      python-pkgs.pybricksdev
    ]))
  ];
}
