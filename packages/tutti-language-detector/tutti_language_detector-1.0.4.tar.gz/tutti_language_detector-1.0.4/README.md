# Python package `tutti_language_detector`

Python package to detect the language of tutti ads.

## Requirements

The main requirement for using this package is the command-line _Vowpal Wabbit_ executable, `vw`, which can be installed
following the instructions in their [GitHub site](https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Getting-started).
However **do not use the PyPI version** since it only installs the Python package but not the `vw` binary that
`tutti_language_detector` uses.

This repository contains pretrained model files that are hosted in a public S3 bucket via DVC. You will need to have
[DVC](https://dvc.org) installed and the AWS S3 necessary
[configurations](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in your machine.  

## Installation

1. Clone the repository like this: `git clone https://github.com/tutti-ch/tutti-language-detector`
2. Enter the repository directory `cd tutti-language-detector`
3. Pull model files from DVC remote: `dvc pull`
4. Install with `pip3 install --user -e .`. 

Uninstall with: `pip3 uninstall tutti_language_detection`.
