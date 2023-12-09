CREATE DATABASE IF NOT EXISTS test;

USE test;

CREATE TABLE IF NOT EXISTS UserData (
    id CHAR(36) PRIMARY KEY,
    hashed_password VARCHAR(255),
    email VARCHAR(255),
    username VARCHAR(35)
);
