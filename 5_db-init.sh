#!/usr/bin/env bash
# 
# Bootstrap script for setting up the Postgres db

# start postgres service at start
brew services start postgresql

# verify postgres installation
postgres -V

# start psql instance
psql postgres

echo "process complete"