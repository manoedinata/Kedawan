#! /usr/bin/env sh

# Let the DB start
sleep 10;

# Run migrations
FLASK_APP="main:app" flask db upgrade
