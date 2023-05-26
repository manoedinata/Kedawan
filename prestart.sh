#! /usr/bin/env sh

# Let the DB start
sleep 25;

# Run migrations
FLASK_APP="main:app" flask db upgrade
