import random
import time
from datetime import datetime, timezone

from apscheduler.schedulers.blocking import BlockingScheduler

from . import met_client, transform
from .config import settings
from .db import SessionLocal, engine
from .models import Base, ForecastPoint, ForecastRaw, Location


def ensure_schema():
    Base.metadata.create_all(bind=engine)


def seed_locations(sess: SessionLocal):
    if sess.query(Location).count() == 0:
        for entry in settings.locations.split(","):
            name, lat, lon, alt = entry.split(":")
            sess.add(
                Location(name=name, lat=float(lat), lon=float(lon), altitude_m=int(alt))
            )
        sess.commit()


def run_once():
    ensure_schema()
    s = SessionLocal()
    try:
        seed_locations(s)
        # Fetch per location with caching and jitter
        for loc in s.query(Location).all():
            last = (
                s.query(ForecastRaw)
                .filter(ForecastRaw.location_id == loc.id)
                .order_by(ForecastRaw.id.desc())
                .first()
            )
            last_mod = last.last_modified if last else None
            doc, lm = met_client.fetch(loc.lat, loc.lon, loc.altitude_m, last_mod)
            if not doc:
                continue  # Not modified

            s.add(
                ForecastRaw(
                    location_id=loc.id,
                    fetched_at=datetime.now(timezone.utc),
                    last_modified=lm,
                    payload_json=doc,
                )
            )
            for p in transform.extract_points(doc):
                s.merge(ForecastPoint(location_id=loc.id, **p))
            s.commit()
            time.sleep(random.uniform(0.2, 1.0))  # jitter between calls
    finally:
        s.close()


def main():
    if settings.schedule_cron:
        minute, hour, dom, mon, dow = settings.schedule_cron.split()
        sched = BlockingScheduler()
        sched.add_job(
            run_once,
            "cron",
            minute=minute,
            hour=hour,
            day=dom,
            month=mon,
            day_of_week=dow,
            misfire_grace_time=60,
        )
        # Run the job once on startup so the first scheduled run isn't missed
        run_once()
        sched.start()
    else:
        run_once()


if __name__ == "__main__":
    main()
