# Deutscher Befrager
![Build Status Badge](https://img.shields.io/gitlab/pipeline/BTBTravis/deutscher-befrager.svg)

[![Coverage Status](https://coveralls.io/repos/gitlab/BTBTravis/deutscher-befrager/badge.svg?branch=HEAD)](https://coveralls.io/gitlab/BTBTravis/deutscher-befrager?branch=HEAD)

## Purpose

I'm in the process of learning german but I don't work in german so I made this as a way to practice
while I'm on the command line. 

## Usage

Ask questions: `$ befrager ask "Wo wohnen Sie?"` 

Answer questions: `$ befrager answer`

# Dev

## Useful links

* click docs: https://click.palletsprojects.com/en/7.x/quickstart/
* yaml docs: https://pyyaml.org/wiki/PyYAMLDocumentation
* yaml lang docs: https://yaml.org/
* yaml loader info: https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
* unittest: https://docs.python.org/2/library/unittest.html
* guide to unittest: https://realpython.com/python-testing/

## Tips

Remember to write requirements.txt when adding packages:

`$ pipenv run pip freeze > requirements.txt`

Run commands locally with:

`pipenv run python -m interviewer.core --help`



