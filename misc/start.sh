#!/bin/sh
PSERVE_BIN=../python_setup/env/bin/pserve
$PSERVE_BIN  production.ini --daemon --reload
