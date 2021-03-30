#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE naks_ndt_db;
    CREATE USER naks_ndt_user WITH PASSWORD 'password';
    ALTER ROLE naks_ndt_user SET client_encoding TO 'utf8';
    ALTER ROLE naks_ndt_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE naks_ndt_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE naks_ndt_db TO naks_ndt_user;
    ALTER USER naks_ndt_user CREATEDB;
EOSQL
