PyMCUTK Overview
==============

PyMCUTK is a python based toolkit on hand for MCU development or testing. It involved third-part tools, and integrate them together to unified interfaces. The project focus on toolchains and their projects, debuggers, boards support. Simple command line that could make you can quicky get started to execute build testing in automated way. We have many hard works and you may won't repeat. That is what PyMCUTK design for.


> Requirements or Bugs: You can create a JIRA ticket(Project: KTD, components: AT_PyMCUTK).
Or email to hui.guo@nxp.com.


## Prerequisites

- python 2 >= 2.7.5 or python 3 >= 3.6
- make sure `pip` command is working in your system terminal.

## Installation

Install from source code, firstly clone the git repository from [Bitbucket](https://bitbucket.sw.nxp.com/projects/MSVC/repos/pymcutk/browse),
and install by running:

`pip install -r requirements-dev.txt`


## Quickly start


### Command line usage


```bash
# Build projects in current directory.
$ mtk build .

# Build specific configuration: sdran_release
$ mtk build . -t sdram_release

# Recursive build and dump results to CSV format.
$ mtk build ./mcu-sdk-2.0/boards/ -r --results-csv

# Scan Projects dump to json format
$ mtk scan ./mcu-sdk-2.0/boards/ -o test.json
```


### Configuration

By default, mtk will automaticlly get the installation from your system.
It's also could load configuration from file system. Run bellow command that will automatic generate the configuration file, which is saved at ~/.mcutk.

```bash
$ mtk config --auto
```

If you need something special to configure, just edit the ~/.mcutk file.


<!-- ### Simple usage

`python -m mcutk -d <path to directory that contain a file name 'mcutk.json'>`

Example:

```bash
python -m mcutk -d ./examples/
``` -->




### Unittest

Before create pull requests in bitbucket, please do a test in your local to check mistakes.

pytest command:

```bash
pytest .
```