# Pyscience

Pyscience is a easy python library and command-line application to work with
mathematical operations and other science related programming. Also you can
manage CSV data with the datam module.

Pyscience requires Python 3.7+ to work.

## Installation
Pyscience is available in [PyPI](https://pypi.org/project/pyscience/).
You can install Pyscience using pip (as root):

    pip3 install pyscience

If you want to install the latest development version, you can install pyscience
from the [GitHub repository](https://github.com/m-alzam/pyscience):

    pip3 install git+https://github.com/m-alzam/pyscience.git

Pre-releases have the latest features and bug fixes.

## Features
- Basic calculator
- Operate with variables, monomials and polynomials
- Solve first and second-degree equations
- Get information about chemical elements
- Manage CSV data easily (in development)
- Convert between unit with the ``units`` module (experimental)

## Basic usage
Once installed, you can run pyscience as a normal program:

    pyscience

This should start pyscience's interactive interpreter. You can operate with
variables:

    > 2x+3x
    5x
    > 2x*7y
    14xy

Or get Chemical Elements information with the ``CE`` function:

    # Returns chemical element with symbol 'H'
    > CE('H')
    ...
    # Returns chemical element with atomic number 2
    > CE(2)
    ...

Solve first-degree equations:

    > Eq(2x, 10)
    Eq(2x = 10)
    Solution: 5

## Documentation
Official documentation is available [here](https://github.com/m-alzam/pyscience/blob/v0.4/doc/source/index.rst).
You can build it using the ``sphinx`` python library and the ``make`` script.

## Todo
Pyscience is in current development. Future features:

* Update chemicals elements information
* Polynomial division
* Physics functions
* Documentation

## History
See [changelog](https://github.com/m-alzam/pyscience/blob/v0.4/doc/source/changelog.rst)

## License
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### About data used for ChemicalElement
Chemical elements information is extracted from the
[Kalzium](https://kde.org/applications/education/kalzium/) program.
