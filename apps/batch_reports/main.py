# apps/batch-reports/main.py
# Peter Diaz

import asyncio
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from platform_core.config.settings import AppSettings
from platform_core.observability.logging import get_logger

settings = AppSettings(app_name="batch-reports")
tenant = "people-analytics"  # Example tenant

logger = get_logger(settings.app_name, tenant)

async def generate_report():
    logger.info("Starting scheduled report generation")

    async with httpx.AsyncClient() as client:
        # Query data through data-proxy
        data_resp = await client.post(
            "http://localhost:8002/query",
            json={"sql": "SELECT * FROM insights"},
            headers={"X-Tenant": tenant}
        )

        # Send telemetry
        await client.post(
            "http://localhost:8003/log",
            json={"event": "batch_report_generated"},
            headers={"X-Tenant": tenant}
        )

    logger.info(f"Report generated: {data_resp.json()}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_report, "interval", seconds=10)
    scheduler.start()

    logger.info("Batch scheduler started")
    await asyncio.Event().wait()  # Keep running


if __name__ == "__main__":
    asyncio.run(main())
