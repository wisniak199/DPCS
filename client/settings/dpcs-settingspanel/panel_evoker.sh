#!/bin/bash

if [[ "$BASH_SOURCE" == "$0" ]]
then 
	sudo -s python2 settingspanel.py
	sudo -K
fi

