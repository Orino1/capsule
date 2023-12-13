CREATE DATABASE IF NOT EXISTS test;

USE test;


CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    hashed_password VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    username VARCHAR(35),
    email_verification_token VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE,
    reset_password_token VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS capsules (
    capsuleid VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    user_id VARCHAR(36),
    image VARCHAR(512) DEFAULT NULL,
    message VARCHAR(1000) NOT NULL,
    open_at DATE NOT NULL,
    opened BOOLEAN DEFAULT FALSE,
    link VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);