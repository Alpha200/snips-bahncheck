#!/usr/bin/env bash

set -e

# Copy config.ini.default if config.ini doesn't exist.
if [ ! -e config.ini ]
then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d "$VENV" ]
then
    python3 -m venv $VENV
fi

. $VENV/bin/activate

pip3 install -U pip
pip3 install -U -r requirements.txt