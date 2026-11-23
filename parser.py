import asyncio
import csv
import json
from datetime import datetime, timezone
import aiohttp

ENDPOINT_URL = (
    "https://" + "a" + "://coingecko.com" + "a" + "pi/v3/simple/price"
    "?ids=ethereum,tether,bitcoin&vs_currencies=usd"
    "&include_24hr_vol=true&include_24hr_change=true"
)


async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        resp.raise_for_status()
        return await resp.json()


def normalize_records(raw_data: dict) -> list[dict]:
    timestamp = datetime.now(timezone.utc).isoformat()
    records = []
    for asset, metrics in raw_data.items():
        records.append({
            "timestamp_utc": timestamp,
            "asset": asset,
            "price_usd": metrics.get("usd", 0.0),
            "volume_24h_usd": round(metrics.get("usd_24h_vol", 0.0), 2),
            "change_24h_pct": round(metrics.get("usd_24h_change", 0.0), 4),
        })
    return records


async def run_pipeline():
    async with aiohttp.ClientSession() as session:
        raw = await fetch_json(session, ENDPOINT_URL)
        records = normalize_records(raw)

    with open("market_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    if records:
        with open("market_snapshot.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)

    print(f"Exported {len(records)} normalized records.")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
