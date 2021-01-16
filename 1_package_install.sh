#!/usr/bin/env bash
# 
# Bootstrap script for setting up the evnironment needed

echo "Starting bootstrapping"

# installing homebrew
echo "Installing Brew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update homebrew recipes
brew update

# Installing postgres
echo "Installing Postgres..."
brew install postgresql

# Installing Python packages
echo "Installing Python packages..."
PYTHON_PACKAGES=(
    ipython
    virtualenv
    virtualenvwrapper
    lxml
    pandas
    SQLAlchemy
    psycopg2-binary
)
pip3 install ${PYTHON_PACKAGES[@]}

echo "Bootstrapping complete"