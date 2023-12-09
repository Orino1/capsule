CREATE DATABASE IF NOT EXISTS test;

USE test;

CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    hashed_password VARCHAR(255),
    email VARCHAR(255),
    username VARCHAR(35),
    token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);