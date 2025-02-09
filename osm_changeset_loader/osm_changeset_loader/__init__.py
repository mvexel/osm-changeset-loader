"""OSM Changeset Loader package."""

from .config import Config
from .replication import ReplicationClient
from .api import app
from .db import get_db_engine, get_db_session, create_tables
from .model import Changeset, Metadata
from .path import Path

__version__ = "0.1.0"
__all__ = [
    "Config",
    "ReplicationClient",
    "app",
    "get_db_engine",
    "get_db_session",
    "create_tables",
    "Changeset",
    "Metadata",
    "Path"
]

# Make the package available for direct imports
import sys
import os

package_dir = os.path.dirname(os.path.abspath(__file__))
if package_dir not in sys.path:
    sys.path.append(package_dir)
