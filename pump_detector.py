
import httpx

BASE_URL = "https://api.binance.com"


async def get_ticker(symbol: str):
    """
    دریافت اطلاعات 24 ساعته یک نماد
    """
    url = f"{BASE_URL}/api/v3/ticker/24hr"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params={"symbol": symbol.upper()})
        response.raise_for_status()
        return response.json()


async def detect_pump(symbol: str):
    """
    بررسی اولیه پامپ
    """

    data = await get_ticker(symbol)

    price_change = float(data["priceChangePercent"])
    volume = float(data["quoteVolume"])

    result = {
        "symbol": symbol.upper(),
        "price_change": price_change,
        "volume": volume,
        "is_pump": False,
    }

    # شرط اولیه تشخیص پامپ
    if price_change >= 5 and volume >= 1_000_000:
        result["is_pump"] = True

    return result
