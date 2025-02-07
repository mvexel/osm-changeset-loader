"""
Database convenience functions.
"""

from typing import List, Optional
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from .model import Changeset, Metadata

DB_URL = "postgresql://mvexel@localhost:5432/osm"


def get_db_engine(db_url=DB_URL):
    """
    Get a database engine.
    """
    return create_engine(db_url)


def get_db_session(db_url=DB_URL):
    """
    Get a database session.
    """
    engine = get_db_engine(db_url)
    return Session(engine)


def create_tables(db_url=DB_URL):
    """
    Create database tables.
    """
    engine = get_db_engine(db_url)
    Metadata.__table__.create(engine, checkfirst=True)
    Changeset.__table__.create(engine, checkfirst=True)


def query_changesets(
    min_lon: Optional[float] = None,
    max_lon: Optional[float] = None,
    min_lat: Optional[float] = None,
    max_lat: Optional[float] = None,
    user: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Changeset]:
    """
    Query changesets with optional filters.
    """
    session = get_db_session()

    query = session.query(Changeset)

    # Bounding box filter
    if all([min_lon, max_lon, min_lat, max_lat]):
        query = query.filter(
            and_(
                Changeset.min_lon >= min_lon,
                Changeset.max_lon <= max_lon,
                Changeset.min_lat >= min_lat,
                Changeset.max_lat <= max_lat,
            )
        )

    # User filter
    if user:
        query = query.filter(Changeset.user == user)

    # Date range filters
    if created_after:
        query = query.filter(Changeset.created_at >= created_after)
    if created_before:
        query = query.filter(Changeset.created_at <= created_before)

    return query.offset(offset).limit(limit).all()


def get_oldest_changeset_timestamp(db_url=DB_URL):
    """
    Get the timestamp of the oldest changeset in the database.
    """
    session = get_db_session(db_url)
    oldest = session.query(Changeset.created_at).order_by(Changeset.created_at).first()
    return oldest[0] if oldest else None
