import warnings

from server.utils.deprecation import RemovedInDjango30Warning

warnings.warn(
    "The server.db.backends.postgresql_psycopg2 module is deprecated in "
    "favor of server.db.backends.postgresql.",
    RemovedInDjango30Warning, stacklevel=2
)
