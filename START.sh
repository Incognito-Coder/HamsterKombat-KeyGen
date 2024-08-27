#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting the bot..."
python keygen.py

echo "Press any key to continue..."
read -n 1 -s
