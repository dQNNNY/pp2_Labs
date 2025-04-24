CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS user_score (
    username VARCHAR(50) REFERENCES users(username),
    score INTEGER,
    level INTEGER,
    PRIMARY KEY (username)
);
