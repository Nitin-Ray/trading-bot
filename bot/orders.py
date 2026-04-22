from typing import Optional

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logger
from bot.validators import ValidationError, validate_all

logger = setup_logger()


def print_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]):
    print("\n" + "=" * 50)
    print("         ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("=" * 50)


def print_order_response(response: dict):
    print("\n" + "-" * 50)
    print("         ORDER RESPONSE")
    print("-" * 50)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print(f"  Exec. Qty  : {response.get('executedQty', 'N/A')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    print(f"  Avg Price  : {avg_price}")
    print("-" * 50)
    print("  ✅ Order placed successfully!")
    print("-" * 50 + "\n")


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
):
    # Validate inputs
    try:
        symbol, side, order_type, qty, price_val = validate_all(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        print(f"\n  ❌ Validation Error: {e}\n")
        return

    # Show request summary
    print_order_summary(symbol, side, order_type, qty, price_val)

    # Place order
    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=qty,
            price=price_val,
        )
        print_order_response(response)
    except BinanceClientError as e:
        logger.error(f"Order failed: {e}")
        print(f"\n  ❌ Order Failed: {e}\n")
    except Exception as e:
        logger.exception(f"Unexpected error during order placement: {e}")
        print(f"\n  ❌ Unexpected error: {e}\n")
