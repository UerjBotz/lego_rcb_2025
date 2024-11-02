{ lib
, pkgs
, buildPythonPackage
, fetchPypi
, setuptools
, wheel
, poetry
#, poetry-core
#, poetry-core-masonry
}:

buildPythonPackage rec {
  pname = "pybricksdev";
  version = "1.0.0a50";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-jpUpDNV79XPO3uFyLySX7Od7ESfRAwmWZZMZGzEjAzM=";
  };

  nativeBuildInputs = [
    #pkgs.python3Packages.poetry-core
    #pkgs.python3Packages.poetry-core-masonry
    pkgs.poetry
  ];

  preferWheels = true; #!

  # do not run tests
  doCheck = false;

  # specific to buildPythonPackage, see its reference
  pyproject = true;
  build-system = [
    setuptools
    wheel
  ];
}

