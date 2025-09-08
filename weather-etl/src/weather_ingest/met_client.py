import httpx
import backoff
from .config import settings

BASE = "https://api.met.no/weatherapi/locationforecast/2.0/compact"


def _headers(last_modified: str | None):
    h = {
        "User-Agent": settings.met_user_agent,
        "Accept-Encoding": "gzip, deflate",
    }
    if last_modified:
        h["If-Modified-Since"] = last_modified
    return h


@backoff.on_exception(backoff.expo, (httpx.HTTPError,), max_time=60)
def fetch(lat: float, lon: float, altitude: int | None, last_modified: str | None):
    params = {"lat": round(lat, 4), "lon": round(lon, 4)}
    if altitude is not None:
        params["altitude"] = int(altitude)
    with httpx.Client(timeout=20.0, headers=_headers(last_modified)) as client:
        r = client.get(BASE, params=params)
        if r.status_code == 304:
            return None, last_modified
        r.raise_for_status()
        lm = r.headers.get("Last-Modified")
        return r.json(), lm
