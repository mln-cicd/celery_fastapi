#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE postgres"

psql postgres -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"