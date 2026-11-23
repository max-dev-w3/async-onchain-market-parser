# Async On-Chain & Market Data Parser

Lightweight, high-throughput asynchronous Python pipeline for collecting, normalizing, and exporting real-time crypto market and liquidity metrics.

## Features
- **Async HTTP Execution:** Built with `aiohttp` and `asyncio` for concurrent endpoint polling with rate-limit backoff.
- **Data Normalization:** Cleans raw JSON payloads into structured analytical schemas.
- **Multi-Format Export:** Outputs ready-to-analyze datasets in `CSV` and `JSON` formats.

## Quick Start
```bash
pip install -r requirements.txt
python parser.py
```

## Architecture
1. `fetch_market_snapshot()` — asynchronous collector with timeout and retry handling.
2. `transform_metrics()` — calculates spread, 24h volume velocity, and liquidity ratios.
3. `export_dataset()` — writes normalized records for downstream BI or Pandas analysis.
