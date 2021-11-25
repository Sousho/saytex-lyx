# SayTeX-LyX
Speak math, get WYSIWYM formulae directly in your LyX editor!

SayTeX is a tool for converting spoken math into LaTeX equations. 

Read the documentation at [saytex.readthedocs.io](https://saytex.readthedocs.io).

Experience the demo at [demo.saytex.xyz](https://demo.saytex.xyz).

## Overview

SayTeX is distributed as a Python package, enabling users of it to easily convert between transcribed spoken math and LaTeX.

SayTeX-LyX is offered as part of the Sousho dictation extension for Talon voice.

The package is [highly configurable](https://saytex.readthedocs.io/en/latest/advancedusage.html).

## Installation

Install SayTeX using PyPI: `pip install saytex-lyx`.

Read more in the [installation documentation](https://saytex.readthedocs.io/en/latest/gettingstarted.html#installation).

## Usage

```python
from saytex import Saytex

saytex_compiler = Saytex()

print(saytex_compiler.to_latex("pi squared over six"))
```

The above minimal example will print `\frac{\pi^2}{6}`. For advanced use, read the [documentation](https://saytex.readthedocs.io).

## Repository Structure

- `blog`: A collection of Markdown files written during the second half of SayTeX development, in diary format.
- `docs`: Documentation files, generated using [Sphinx](https://sphinx-doc.org), for the [documentation website](https://saytex.readthedocs.io).
- `experimental`: Everything that is not currently in use by the project, but was experimented with during development and might become useful in the future.
- `saytex`: The Python package. This is the core of the SayTeX project.
- `syntax-specifications`: Specifications of the SayTeX Syntax.
- `tests`: Tests for the Python package.
- `website`: The static website served at [saytex.xyz](https://saytex.xyz).

## About

SayTeX was developed during the academic year 2018-2019 as a research project by Arvid Lunnemark, under the supervision of Dr. Kyle Keane within the Department of Materials Science in the Interactive Materials Education Laboratory at MIT. The research proposals can be found in the folder `research-proposals`.

All code is open source and licensed under the MIT License. Contributions are welcome.
