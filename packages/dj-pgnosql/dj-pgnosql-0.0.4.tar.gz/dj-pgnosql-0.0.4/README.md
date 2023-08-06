# PG NoSQL

Using Postgres as a NoSQL database. Intended for providing a shared storage space between different django projects

**Installation**

```
pip install dj-pgnosql
```

Note: this package doesn't specify any requirements, but assumes that your project is setup to use Postgres with a version of Django that supports `JSONField`

* Add `pgnosql` to `INSTALLED_APPS` in settings.py

## Recommended usage (with a custom database)

We recommend that you configure pgnosql to use a different database from your project's default database.

The idea is that you might have multiple django projects which connect to this KV store as a means to easily share data between services

### Configure a seperate database connection:

**settings.py**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'postgres'),
        'PORT': 5432,
    },
    'pgnosql': { # <- this is our nosql db
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NOSQL_DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('NOSQL_DATABASE_USER', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'postgres'),
        'PORT': 5432,
    }
}
```

**Add the DB router**

```python
DATABASE_ROUTERS = ['pgnosql.routers.NoSQLRouter']
```

This router will send queries to the NoSQL database if the model is from the `pgnosql` app. Otherwise will send it to the default database

**Run migrations:**

You'll need to specify that you're running them for the `pgnosql` database.

```bash
web python manage.py migrate pgnosql --database=pgnosql
```

You're all setup.

## Usage

```python
from pgnosql.models import KV
key = "foo"
value = {"bar": "bus"}

KV.set(key, value) # value must be json
KV.get(key) # {"bar": "bus"}
KV.delete()
```

You can obviously also just use Django's standard ORM

**Model fields:**

```python
key = models.CharField(max_length=100, db_index=True)
value = JSONField(default=dict)
index = models.CharField(max_length=255, db_index=True, help_text='You can provide an index to make this key searchable')

time_to_live = models.PositiveIntegerField(default=0)
created_date = models.DateTimeField(auto_now_add=True)
modified_date = models.DateTimeField(auto_now=True)
```