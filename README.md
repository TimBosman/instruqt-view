# Instruqt view

This is a CLI and UI tool to visualize how students are engaging with you Instruqt

## Usage

First create the environment and activate it [see below](#create-a-python-env). Then just run:

```bash
python .
```

To open the CLI tool (the `--cli` flag is available). If you want to use the User interface you can add the `--ui` flag

```bash
python . --ui
```

To see more information

```bash
python . --help
```

## Prerequisites

This tool uses the Instruqt CLI tool so that should be downloaded and installed prior to using this tool. It also requires the credentials file to be there at `~/.config/instruqt/credentials`. Make sure you run `instruqt auth login` to get that file ready.

## Create a Python env

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
