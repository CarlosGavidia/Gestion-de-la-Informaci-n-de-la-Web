BEGIN TRANSACTION;
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
INSERT INTO users VALUES(0,'pepe',1234);
COMMIT;