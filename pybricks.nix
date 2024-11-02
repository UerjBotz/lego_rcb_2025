{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, wheel
, poetry-core
, pkgs
}:

buildPythonPackage rec {
  pname = "pybricks";
  version = "3.5.0";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-ze4jQTtBKWp+RNB6BCIs6+2BFbitYV4mW+wpmqi1sEY=sha256-ze4jQTtBKWp+RNB6BCIs6+2BFbitYV4mW+wpmqi1sEY=";
  };

  nativeBuildInputs = [
    pkgs.python3Packages.poetry-core
  ];

  # do not run tests
  doCheck = false;

  # specific to buildPythonPackage, see its reference
  pyproject = true;
  build-system = [
    setuptools
    wheel
  ];
}

