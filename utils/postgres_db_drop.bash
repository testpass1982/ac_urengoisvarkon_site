#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    DROP DATABASE IF EXISTS naks_ndt_db;
    DROP DATABASE IF EXISTS test_naks_ndt_db;
    DROP USER IF EXISTS naks_ndt_user;
    DROP USER IF EXISTS test_naks_ndt_db;
EOSQL
