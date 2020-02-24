## api-to-postgres
Store data from an API into a Postgres table

## Project layout
```bash
.
├── README.md
├── frameio
│   ├── __init__.py
│   ├── api_client.py
│   ├── db_connection.py
│   └── sql_queries.py
├── configs.cfg
├── requirements.txt
├── etl.py
└── validation.py
```

## How to run this project

* **Step 1**: `git clone https://github.com/shravan-kuchkula/api-to-postgres.git` OR unzip the zip file.
* **Step 2**: Create a database in postgres. Ex `createdb -h localhost -p 5432 -U postgres frameiodb`
* **Step 3**: `cd api-to-postgres`
* **Step 4**: Update `configs.cfg` file with database connection details and API access key
* **Step 5**: Run `pip install virtualenv`
* **Step 6**: Run `virtualenv venv`
* **Step 7**: Run `. venv/bin/activate`
* **Step 8**: Run `pip install -r requirements.txt`
* **Step 9**: Run `python etl.py`
* **Step 10**: Run `python validation.py`

## validation Output
```bash
(etl) shravan-api-to-postgres$ python validation.py
Executing: b'SELECT COUNT(*) FROM users;'
Output:
(125,)
Executing: b'SELECT COUNT(DISTINCT user_id) FROM users;'
Output:
(125,)
Executing: b'SELECT * FROM users LIMIT 10'
Output:
('e2f9ddf5-f9e5-4279-ba83-850e98f1de49', 'no', 'yes')
('3b83a844-ab0d-4881-968e-66d73bb8a99a', 'yes', 'no')
('442c913e-e767-47b5-b100-78693a6678a8', 'no', 'yes')
('3ecba4d7-1bd0-46a9-b526-a6724527b843', 'no', 'yes')
('fe6fee15-9d1f-41c3-98b3-34b0497c686a', 'no', 'yes')
('76d63f2d-0cf0-40ab-8b32-b63ff32da3d3', 'no', 'yes')
('658f6100-9359-45c9-bbdf-3ceaf355351a', 'no', 'yes')
('9c7bae2e-5987-4209-a145-41c584d465d9', 'no', 'yes')
('c13010a3-7d55-4267-acdc-a39b8b015a90', 'no', 'yes')
('89cce5dd-caee-4c9f-9ca3-d174d3cd380b', 'yes', 'no')
Executing: b"SELECT COUNT(user_id) FROM users WHERE is_asset = 'yes';"
Output:
(96,)
Executing: b"SELECT COUNT(user_id) FROM users WHERE is_comment = 'yes';"
Output:
(29,)
Executing: b"SELECT COUNT(user_id) FROM users WHERE is_comment = 'yes' AND is_asset = 'yes';"
Output:
(0,)
(etl) shravan-api-to-postgres$
```
