# dixtribution

[![PyPI - Version](https://img.shields.io/pypi/v/dixtribution.svg)](https://pypi.org/project/dixtribution)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dixtribution.svg)](https://pypi.org/project/dixtribution)

---

Dixtribution is a CLI tool to gather stats and test the performance of your [Dix](https://wiki.aediroum.ca/wiki/Jeu_du_10)
bot using the [onze](https://github.com/matteodelabre/onze?tab=readme-ov-file) game master.

**Table of Contents**

- [Installation](#installation)
- [Dixtributors](#Dixtributor)
- [Custom Dixtributors](#adding-a-custom-dixtributor)
- [License](#license)

## Installation

```sh
git clone https://github.com/Ecoral360/dixtribution.git
cd dixtribution
hatch shell
pip install your/path/to/onze
dixtribution --version  # should output the version
```

## Dixtributors

Dixtributors are middleware programs that take the debug messages from [onze](https://github.com/matteodelabre/onze?tab=readme-ov-file)
and produce stats, analytics, and much more from it!

You can add dixtributors to your execution with the `-d <DIXTRIBUTOR_NAME>` attribute in the `dixtribution` cli command.

For example, the `plt_final` dixtributor plots the final score of each game in a graph.

> To get a list of all the supported Dixtributors, run the `dixtribution --help` command

## Adding a custom Dixtributor

To add your custom Dixtributor: 
1. Add a python file in the `src/dixtribution/dixtributors` directory.
2. In that file, add a class that inherits from [Dixtributor](src/dixtribution/dixtributor.py)
3. Add the `CLI_NAME` class attribute (that's how you will trigger it in the `dixtribution` command)
4. Add the required methods from the Dixtributor abstract class to your class
5. Run the `dixtribution` command with the `-d <your-CLI_NAME>` to see it in action!

## License

`dixtribution` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
