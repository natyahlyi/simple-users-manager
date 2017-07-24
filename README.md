# Simple user management app

## Requirements
* Python 3
* Memcached

```
$ pip install -r requirements.txt
```
## Usage
Prepare db and creates initial data (requires: `DB_ROOT_PASSWORD` - password to Mysql root user in environment variables):
```
$ python manage.py create_all
```
Runs development server:
```
$ python manage.py runserver
```