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

-- Create Skin table
CREATE TABLE IF NOT EXISTS skin (
  skin_id SERIAL PRIMARY KEY,
  skin_name VARCHAR(64)
);

-- Create User_Favorite_Skin junction table
CREATE TABLE IF NOT EXISTS user_favorite_skin (
  user_id INT NOT NULL,
  skin_id INT NOT NULL,
  PRIMARY KEY (user_id, skin_id),
  FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (skin_id) REFERENCES skin (skin_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);