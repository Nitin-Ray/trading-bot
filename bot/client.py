import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"

logger = setup_logger()


class BinanceClientError(Exception):
    pass


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise BinanceClientError("API key and secret must not be empty.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: Dict[str, Any]) -> str:
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _timestamp(self) -> int:
        return int(time.time() * 1000)

    def _post(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = self._timestamp()
        params["signature"] = self._sign(params)

        url = f"{BASE_URL}{endpoint}"
        logger.debug(f"POST {url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")

        try:
            response = self.session.post(url, data=params, timeout=10)
            logger.debug(f"Response [{response.status_code}]: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise BinanceClientError("Network error: could not reach Binance Testnet. Check your internet connection.")
        except requests.exceptions.Timeout:
            raise BinanceClientError("Request timed out. Binance Testnet may be slow. Try again.")
        except requests.exceptions.HTTPError as e:
            try:
                error_body = response.json()
                code = error_body.get("code", "N/A")
                msg = error_body.get("msg", str(e))
                raise BinanceClientError(f"API error {code}: {msg}")
            except Exception:
                raise BinanceClientError(f"HTTP error: {e}")

    def ping(self) -> bool:
        try:
            url = f"{BASE_URL}/fapi/v1/ping"
            resp = self.session.get(url, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        logger.info(f"Placing {order_type} {side} order | symbol={symbol} qty={quantity} price={price}")
        result = self._post("/fapi/v1/order", params)
        logger.info(f"Order placed successfully | orderId={result.get('orderId')} status={result.get('status')}")
        return result
