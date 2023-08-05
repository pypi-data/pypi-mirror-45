# Parallel Foreach Submodule

[![PyPI Version](https://img.shields.io/pypi/v/pfs.svg)](https://pypi.python.org/pypi/pfs)
[![PyPI Compatibility](https://img.shields.io/pypi/pyversions/pfs.svg)](https://pypi.python.org/pypi/pfs)
[![PyPI License](https://img.shields.io/pypi/l/pfs.svg)](https://github.com/RDCH106/parallel_foreach_submodule/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9000e198e34c4f93a8320942e5b8524e)](https://www.codacy.com/app/RDCH106/parallel_foreach_submodule?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RDCH106/parallel_foreach_submodule&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/RDCH106/parallel_foreach_submodule.svg?branch=master)](https://travis-ci.org/RDCH106/parallel_foreach_submodule)

Parallel Foreach Submodule (PFS) is a tool for "git submodule foreach" execution in parallel.


### What can I do with PFS?

* Execute git submodule foreach in parallel
* Use it from terminal when it is installed
* Multiplatform execution (it is developed in Python)


### Installation

You can install or upgrade PFS with:

`$ pip install pfs --upgrade`

Or you can install from source with:

```bash
$ git clone https://github.com/RDCH106/parallel_foreach_submodule.git --recursive
$ cd parallel_foreach_submodule
$ pip install .
```


### Quick example

```bash
$ pfs -p "D:\project" -c "git pull origin" -j 8
```

The example executes command `git pull origin` for each submdoule in `D:\project` using 8 threads.


### Shortcuts

List of shortcuts or aliases to write faster some usual operations

* `pfs --pull` ~ `pfs -c "git pull origin"`
* `pfs --status` ~ `pfs -c "git status"` 
* `pfs --pending` ~ `pfs -c "git log <since origin/current>..<until current>"`

⚠️ Shortcuts only show repositories affected with changes, use `--verbose` for full log


### Help

Run the following command to see all options available:

`pfs --help` or ` pfs -h`
