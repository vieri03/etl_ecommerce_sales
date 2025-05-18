#!/bin/bash

if [ "$1" = "jupyter" ]; then
    exec jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
elif [ "$1" = "python" ]; then
    shift
    exec python "$@"
elif [ "$1" = "ipython" ]; then
    exec ipython
elif [ "$1" = "bash" ]; then
    exec bash
else
    exec "$@"
fi