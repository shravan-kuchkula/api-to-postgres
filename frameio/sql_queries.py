# define all the sql_queries we are going to be using

# drop table, add more if you have multiple tables
users_table_drop = "DROP TABLE IF EXISTS users"

# create table, add more if you have multiple tables
users_table_create= ("""CREATE TABLE IF NOT EXISTS users (
                                  user_id VARCHAR(1024) PRIMARY KEY,
                                  is_comment VARCHAR,
                                  is_asset VARCHAR
                                  );
                     """)

# select queries
count_users = ("SELECT COUNT(*) FROM users;")
count_distinct_users = ("SELECT COUNT(DISTINCT user_id) FROM users;")
users_rows = ("SELECT * FROM users LIMIT 10")
count_users_asset_created = ("SELECT COUNT(user_id) FROM users WHERE is_asset = 'yes';")
count_users_comment_created = ("SELECT COUNT(user_id) FROM users WHERE is_comment = 'yes';")
count_users_both_created = ("SELECT COUNT(user_id) FROM users WHERE is_comment = 'yes' AND is_asset = 'yes';")

# upsert query to ensure that we update comment created column
user_table_comment_insert = ("""INSERT INTO users (user_id, is_comment, is_asset) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET is_comment=excluded.is_comment;""")

# upsert query to ensure that we update asset created column
user_table_asset_insert = ("""INSERT INTO users (user_id, is_comment, is_asset) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET is_asset=excluded.is_asset;""")

# define lists, which will be imported into etl scripts
drop_table_queries = [users_table_drop]
create_table_queries = [users_table_create]

# define a dictionary of insert types
insert_table_queries = {'insert_comment': user_table_comment_insert,
                        'insert_asset': user_table_asset_insert}

# validation queries
validation_queries = [count_users, count_distinct_users, users_rows, count_users_asset_created, count_users_comment_created, count_users_both_created]
