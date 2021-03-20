from datetime import datetime, date
from typing import Dict

import psycopg2
from flask import g

from server import settings


class DBHelper:
    def __init__(self):
        self._conn = None

    @classmethod
    def conn(cls):
        if "db" not in g:
            g.db = psycopg2.connect(settings.DATABASE_URL)
        return g.db

    @classmethod
    def close_db(cls, e=None):
        db = g.pop("db", None)

        if db is not None:
            db.close()

    @classmethod
    def init_db(cls):
        c = cls.conn().cursor()
        c.execute(
            """
CREATE TABLE IF NOT EXISTS piantina(
    day  DATE, 
    hour INT, 
    temperature INT, 
    dryness INT, 
    light INT, 
    humidity INT
)
            """
        )
        cls.conn().commit()

    @classmethod
    def cursor(cls):
        return cls.conn().cursor()

    @classmethod
    def get_latest_data(cls) -> Dict[str, int]:
        c = cls.conn().cursor()
        c.execute(
            "SELECT temperature, humidity, dryness, light FROM piantina ORDER BY day, hour DESC LIMIT 1"
        )
        try:
            data = c.fetchone()
            return {
                "temperature": data[0],
                "humidity": data[1],
                "dryness": data[2],
                "light": data[3],
            }
        except Exception:
            return {}

    @classmethod
    def write_data(
        cls, *, temperature: int, humidity: int, dryness: int, light: int, hour: int
    ):
        c = cls.conn().cursor()
        c.execute(
            "INSERT INTO piantina(day, hour, temperature, humidity, dryness, light) VALUES(%s, %s, %s, %s, %s, %s)",
            (_today(), hour, temperature, humidity, dryness, light),
        )
        cls.conn().commit()

    @classmethod
    def get_report_data(cls, date_from: date, date_to: date):
        c = cls.conn().cursor()
        c.execute(
            "SELECT day, hour, temperature, humidity, dryness, light "
            + "FROM piantina "
            + "WHERE day > %s AND day < %s "
            + "ORDER BY day, hour ASC",
            (date_from, date_to),
        )
        result = []
        try:
            rows = c.fetchall()
            for row in rows:
                timestamp = datetime.combine(row[0], datetime.min.time()).replace(
                    hour=row[1]
                )
                result.append(
                    {
                        "timestamp": timestamp,
                        "temperature": row[2],
                        "humidity": row[3],
                        "dryness": row[4],
                        "light": row[5],
                    }
                )
        except Exception as exp:
            print(exp)
            return []

        return result


def _today():
    return datetime.now(settings.TIMEZONE).isoformat()[:10]


def _hour():
    return datetime.now(settings.TIMEZONE).hour
