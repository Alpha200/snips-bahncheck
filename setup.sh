#/usr/bin/env bash -e

# Copy config.ini.default if config.ini doesn't exist.
if [ ! -e config.ini ]
then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

pip3 install -r requirements.txt