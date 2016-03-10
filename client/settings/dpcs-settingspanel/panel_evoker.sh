#!/bin/bash

if [[ "$BASH_SOURCE" == "$0" ]]
then
	sudo -v 
	sudo -K
	python settingspanel.py
	sudo mv dpcs.conf /etc/dpcs.conf
fi

