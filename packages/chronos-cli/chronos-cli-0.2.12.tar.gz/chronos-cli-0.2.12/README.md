# chronos

[![pypi version](https://img.shields.io/pypi/v/chronos-cli.svg)](https://pypi.python.org/pypi/chronos-cli)
[![pypi python versions](https://img.shields.io/pypi/pyversions/chronos-cli.svg)](https://pypi.python.org/pypi/chronos-cli)
[![pipeline status](https://gitlab.com/devoperate/chronos/badges/master/pipeline.svg)](https://gitlab.com/devoperate/chronos/commits/master)
[![Documentation Status](https://readthedocs.org/projects/chronos-cli/badge/?version=latest)](https://chronos-cli.readthedocs.io/en/latest/?badge=latest)
![sonarcloud quality gate](https://sonarcloud.io/api/project_badges/measure?project=devoperate_chronos&metric=alert_status)
![sonarcloud coverage](https://sonarcloud.io/api/project_badges/measure?project=devoperate_chronos&metric=coverage)
![sonarcloud bugs](https://sonarcloud.io/api/project_badges/measure?project=devoperate_chronos&metric=bugs)
![sonarcloud reliability](https://sonarcloud.io/api/project_badges/measure?project=devoperate_chronos&metric=reliability_rating)

A CLI tool that infers a next version number for Git repos. It does its magic by looking at the commit messages of commits made since the last tag that had a [semver](https://semver.org) in it. For this to work properly, your commits should following the [Conventional Commits](https://conventionalcommits.org) spec.

# Getting started

**Requires Git 2.0+.**

To use the tool:

- `pip install --upgrade chronos-cli`
- Change into a Git repo.
- `chronos infer`

To bootstrap a development environment (after you've cloned the repo and changed into it):

- `pip install --upgrade pipenv`
- `pipenv sync --dev`

# Documentation

Docs are hosted at https://chronos-cli.readthedocs.io.

# Style

This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/).

# Testing

- `pytest` will run unit tests in this repo.
- `flake8` will lint the code.

This repo also has a CI/CD pipeline built with [Ansible](https://ansible.com) and [GitLab CI](https://about.gitlab.com/product/continuous-integration/).

The pipeline's Ansible playbook can be run on your *nix workstation too:

```sh
ansible-playbook ansible/pipeline.yml --tags build
```

# Contributing

Commits should follow the [Conventional Commits](https://conventionalcommits.org) spec.

# FAQ

TODO

# Acknowledgements

- Thanks to [Eric Poitras](https://github.com/eric-poitras) for asking me to write an earlier version of what would become this tool. This was really his idea.
