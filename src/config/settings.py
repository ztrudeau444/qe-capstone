"""Where things are: the config layer.

Names of things only. Every value can be overridden from the environment,
which is how the pipeline points the tests at its own database. The default
is the disposable local database from docker-compose.yml, whose throwaway
password is already public in that file; a real credential would never be
written here, only read from the environment.
"""
import os

DB_URL = os.environ.get("DB_URL", "postgresql://qe:qe@127.0.0.1:5432/qe")
