[![Build Status](https://travis-ci.com/martinruefenacht/lemonspotter.svg?token=pPyajLGh7dycZ7EPBDvw&branch=develop)](https://travis-ci.com/martinruefenacht/lemonspotter)

# Lemonspotter
This is a test and benchmark suite for MPI.

The intention is to not rely on an entire library, but only incremental steps.

Lemons are both tests that fail, MPI functions that don't do the correct thing
and bad performance implementations.


# Usage

To run use the following command:
```
python -m lemonspotter [path_to_database]
```

# Requirements
To run Lemonspotter only python 3.8.0 is needed. To contribute to development,
please install all packages listed in the `requirements.txt` file.

## Arguments

#### Loading Custom Database:
```-l, --load database_path```

#### Print Lemonspotter Version
```-v, --version```
