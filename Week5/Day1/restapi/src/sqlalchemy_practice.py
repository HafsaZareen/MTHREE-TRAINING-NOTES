from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select
import os

# Define a global database path
db_path = "/mnt/d/mthree/notes/week5/data.db"

# Ensure the directory exists
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Create a global engine with an absolute path
engine = create_engine(f"sqlite:///{db_path}", echo=True)

# A container that holds all table definitions
metadata = MetaData()

# Define 'users' table
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer),
    Column('city', String),
)

# Define 'posts' table
posts = Table('posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('content', String),
    Column('user_id', Integer, ForeignKey('users.id')),
)

# Create tables in the database if they don’t exist
metadata.create_all(engine)

try:
    with engine.connect() as conn:
        # Insert user data
        insert_stmt = insert(users).values(name='John', age=20, city='New York')
        result = conn.execute(insert_stmt)
        print(result.rowcount, "count1")

        # Insert post data
        insert_stmt = insert(posts).values(title='Post 1', content='Content 1', user_id=1)
        result = conn.execute(insert_stmt)
        print(result.rowcount, "count2")

        # Commit the transaction
        conn.commit()

        # Select and print all users
        select_stmt = select(users)
        result = conn.execute(select_stmt)
        for row in result:
            print(row, "rowwwwwwwwwww")

        # Select and print all posts
        select_stmt = select(posts)
        result = conn.execute(select_stmt)
        for row in result:
            print(row, "rowsssssss")

except Exception as e:
    print(f"An error occurred: {e}")