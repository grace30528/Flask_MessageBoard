#!/bin/bash

set -e

echo "Running Development Server"
flask run --host=0.0.0.0 --port=5000 --reload
