# coderepro

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

An LLM tool for evaluating reproducibility of research code. 

## Installation

```bash
python -m pip install coderepro
```

From source:
```bash
git clone https://github.com/LydiaFrance/coderepro
cd coderepro
python -m pip install .
```

## Usage
After installation, the command `coderepro` should be available from your command line.

```bash
coderepro <github url>
```
e.g.

```bash
coderepro https://github.com/LydiaFrance/coderepro
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/LydiaFrance/coderepro/workflows/CI/badge.svg
[actions-link]:             https://github.com/LydiaFrance/coderepro/actions
[pypi-link]:                https://pypi.org/project/coderepro/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/coderepro
[pypi-version]:             https://img.shields.io/pypi/v/coderepro
<!-- prettier-ignore-end -->
