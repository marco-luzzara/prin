CREATE DATABASE hive_metastore_db;
CREATE USER hive_metastore WITH ENCRYPTED PASSWORD 'hive-password';
GRANT ALL PRIVILEGES ON DATABASE hive_metastore_db TO hive_metastore;