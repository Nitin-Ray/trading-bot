#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
CLI entry point
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logger
from bot.orders import place_order

load_dotenv()
logger = setup_logger()


def load_credentials():
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print("\n  ❌ Missing API credentials!")
        print("  Set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.\n")
        sys.exit(1)
    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type", "-t",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity", "-q",
        required=True,
        help="Quantity to trade (e.g. 0.01)",
    )
    parser.add_argument(
        "--price", "-p",
        default=None,
        help="Price (required for LIMIT orders)",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    api_key, api_secret = load_credentials()

    # Init client
    try:
        client = BinanceClient(api_key=api_key, api_secret=api_secret)
    except BinanceClientError as e:
        print(f"\n  ❌ Client init error: {e}\n")
        sys.exit(1)

    # Ping testnet
    print("\n  🔗 Connecting to Binance Futures Testnet...")
    if not client.ping():
        print("  ⚠️  Warning: Testnet ping failed. Proceeding anyway...\n")
        logger.warning("Testnet ping failed.")
    else:
        print("  ✅ Connected successfully.\n")
        logger.info("Testnet ping successful.")

    # Place order
    place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )


if __name__ == "__main__":
    main()
