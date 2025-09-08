from datetime import datetime


def _parse_ts(s: str) -> datetime:
    # Handle trailing 'Z' as UTC
    if s.endswith("Z"):
        s = s.replace("Z", "+00:00")
    return datetime.fromisoformat(s)


def extract_points(doc: dict):
    meta_updated = doc["properties"]["meta"]["updated_at"]
    updated_at = _parse_ts(meta_updated)

    for t in doc["properties"]["timeseries"]:
        ts = _parse_ts(t["time"])
        inst = t["data"]["instant"]["details"]
        next1 = (t["data"].get("next_1_hours") or {}).get("details", {})
        next6 = (t["data"].get("next_6_hours") or {}).get("details", {})
        sym = (t["data"].get("next_1_hours") or {}).get("summary", {}).get("symbol_code")
        yield {
            "forecast_time": ts,
            "updated_at": updated_at,
            "temp_c": inst.get("air_temperature"),
            "wind_mps": inst.get("wind_speed"),
            "wind_from_deg": inst.get("wind_from_direction"),
            "precip_mm_1h": next1.get("precipitation_amount"),
            "precip_mm_6h": next6.get("precipitation_amount"),
            "cloud_area_frac": inst.get("cloud_area_fraction"),
            "symbol_code": sym,
        }
