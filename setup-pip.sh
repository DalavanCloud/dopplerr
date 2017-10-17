#!/bin/bash

# Freeze the version of pip and pipenv for setup reproductibility
pip install -U 'pip==9.0' 'pipenv==4.1.4' 'setuptools!=36.0.0' || echo "you may need to sudo me !"
echo "Done"
