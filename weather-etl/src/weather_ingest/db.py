import struct
import urllib.parse

import pyodbc
from azure.identity import DefaultAzureCredential
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


def _build_conn_str() -> str:
    driver = "ODBC Driver 18 for SQL Server"
    base = (
        f"Driver={{{driver}}};Server={settings.db_server};Database={settings.db_database};"
        "Encrypt=yes;TrustServerCertificate=Yes;Connection Timeout=30;"
    )
    return base


def _token_struct(token: str) -> bytes:
    # SQL Server expects an access token as UTF-16-LE prefixed with its length
    token_bytes = token.encode("utf-16-le")
    return struct.pack("=i", len(token_bytes)) + token_bytes


def _create_engine():
    base = _build_conn_str()
    if settings.use_managed_identity:
        cred = DefaultAzureCredential()
        # Scope for Azure SQL
        access_token = cred.get_token("https://database.windows.net/.default").token

        def connect():
            return pyodbc.connect(base, attrs_before={1256: _token_struct(access_token)})

        return create_engine("mssql+pyodbc://", creator=connect, pool_pre_ping=True)
    else:
        conn = base + f"UID={settings.db_user};PWD={settings.db_password};"
        return create_engine(
            "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(conn), pool_pre_ping=True
        )


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
