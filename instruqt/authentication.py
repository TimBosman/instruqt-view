#!/bin/python

import json
import os

def read_api_key(conf_file="~/.config/instruqt/credentials"):
    with open(os.path.expanduser(conf_file), "r") as openfile:
        config = json.load(openfile)
    return config.get("access_token")
