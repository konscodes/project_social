import sqlite3
from pathlib import Path
from sqlite3 import Error

script_path = Path(__file__).parent
db_path = script_path / 'main.sqlite'

create_users_table = '''--sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  nationality TEXT
);
'''

create_posts_table = '''--sql
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id)
);
'''

create_comments_table = '''--sql
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  text TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  post_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
'''

create_likes_table = '''--sql
CREATE TABLE IF NOT EXISTS likes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  user_id INTEGER NOT NULL, 
  post_id integer NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
'''

create_users = '''--sql
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
'''

create_posts = '''--sql
INSERT INTO
  posts (title, description, user_id)
VALUES
  ("Happy", "I am feeling very happy today", 1),
  ("Hot Weather", "The weather is very hot today", 2),
  ("Help", "I need some help with my work", 2),
  ("Great News", "I am getting married", 1),
  ("Interesting Game", "It was a fantastic game of tennis", 5),
  ("Party", "Anyone up for a late-night party today?", 3);
'''

create_comments = '''--sql
INSERT INTO
  comments (text, user_id, post_id)
VALUES
  ('Count me in', 1, 6),
  ('What sort of help?', 5, 3),
  ('Congrats buddy', 2, 4),
  ('I was rooting for Nate though', 4, 5),
  ('Help with your thesis?', 2, 3),
  ('Many congratulations', 5, 4);
'''

create_likes = '''--sql
INSERT INTO
  likes (user_id, post_id)
VALUES
  (1, 6),
  (2, 3),
  (1, 5),
  (5, 4),
  (2, 4),
  (4, 2),
  (3, 6);
'''

select_users = '''--sql
SELECT * from users;
'''

select_posts = '''--sql
SELECT * from posts;
'''


def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        print('Connection to DB successful')
    except Error as e:
        print(f'Error: {e}')

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed successfully')
    except Error as e:
        print(f'Error: {e}')


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    connection = create_connection(db_path)
    # execute_query(connection, query=create_users_table)
    # execute_query(connection, query=create_posts_table)
    # execute_query(connection, query=create_likes_table)
    # execute_query(connection, query=create_comments_table)
    # execute_query(connection, query=create_users)
    # execute_query(connection, query=create_posts)
    # execute_query(connection, query=create_comments)
    # execute_query(connection, query=create_likes)

    users = execute_read_query(connection, select_users)
    if users:
        [print(user) for user in users]

    posts = execute_read_query(connection, select_posts)
    if posts:
        [print(post) for post in posts]
