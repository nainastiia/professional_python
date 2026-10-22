import asyncio
import httpx


async def fetch_with_retry(
    client: httpx.AsyncClient, url: str, max_attempts: int = 3
) -> dict:
    """Виконує HTTP GET запит із можливістю повторних спроб (retry)."""
    for attempt in range(1, max_attempts + 1):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError):
            if attempt == max_attempts:
                raise
            await asyncio.sleep(attempt)
    raise RuntimeError("Unexpected retry state")


async def check_multiple_products_stock(
    base_url: str, product_ids: list[int]
) -> list[dict]:
    """Паралельно отримує дані про залишки товарів із використанням Semaphore та Task/gather."""
    semaphore = asyncio.Semaphore(3)  # Обмеження паралелізму

    async def limited_fetch(client: httpx.AsyncClient, pid: int) -> dict:
        url = f"{base_url}/products/{pid}"
        async with semaphore:
            return await fetch_with_retry(client, url)

    async with httpx.AsyncClient(timeout=5.0) as client:
        # Створення списку asyncio.Task
        tasks = [
            asyncio.create_task(limited_fetch(client, pid))
            for pid in product_ids
        ]

        try:
            # Паралельне виконання з таймаутом
            results = await asyncio.wait_for(
                asyncio.gather(*tasks), timeout=10.0
            )
            return list(results)
        except asyncio.TimeoutError:
            return []