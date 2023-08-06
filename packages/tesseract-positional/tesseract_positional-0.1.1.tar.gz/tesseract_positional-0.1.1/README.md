# Tesseract-Positional
A tool to save positional OCR data to a text file

[![GitHub version](https://badge.fury.io/gh/tjkessler%2Ftesseract-positional.svg)](https://badge.fury.io/gh/tjkessler%2Ftesseract-positional)
[![PyPI version](https://badge.fury.io/py/tesseract-positional.svg)](https://badge.fury.io/py/tesseract-positional)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/tjkessler/tesseract-positional/master/LICENSE.txt)

Tesseract-Positional allows positional data extracted using OCR to be saved as plain-text. Positional data includes text spacing and line breaks.

## Installation

Installation via pip:

```
$ pip install tesseract-positional
```

Installation via cloned repository:

```
$ cd tesseract-positional
$ python setup.py install
```

Additional dependencies (pytesseract, Pillow) will be installed during Tesseract-Positional's installation.

## Basic Usage

### Via a Python script

Saving extracted text to a file:

```python
from tesseract_positional import positional_ocr
positional_ocr('image.tiff', 'output.txt')
```

Obtaining extracted text:

```python
from tesseract_positional import positional_ocr
text = positional_ocr('image.tiff')
```

### Via the command line

```
$ tesseract-positional image.tiff output.txt
```

## Contributing, Reporting Issues and Other Support

To contribute to Tesseract-Positional, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).
