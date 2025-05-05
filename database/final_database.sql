-- Schema: public (default in Supabase)

-- Create User table
CREATE TABLE IF NOT EXISTS "user" (
  user_id SERIAL PRIMARY KEY,
  firstName VARCHAR(64),
  lastName VARCHAR(64),
  username VARCHAR(64),
  password VARCHAR(128),
  email VARCHAR(64),
  profilePicture VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS favorite (
  skin_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  image VARCHAR(256),
  skinName VARCHAR(64),
  description VARCHAR(256),
  type VARCHAR(32),
  series VARCHAR(64),
  rarity VARCHAR(16),
  set VARCHAR(64),
  introduced VARCHAR(64),
  FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS steam (
  game_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  image VARCHAR(256),
  gameName VARCHAR(64),
  salePrice VARCHAR(32),
  regularPrice VARCHAR(32),
  deal_id VARCHAR(32),
  steam_id VARCHAR(64),
  FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS free (
  game_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(128),
  thumbnail VARCHAR(256),
  genre VARCHAR(64),
  short_description VARCHAR(1028),
  platform VARCHAR(64),
  publisher VARCHAR(128),
  developer VARCHAR(128),
  release_date VARCHAR(256),
  url VARCHAR(256),
  FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);