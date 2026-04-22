# Binance Futures Testnet Trading Bot

A clean, structured Python CLI application to place **Market** and **Limit** orders on the **Binance Futures Testnet (USDT-M)**.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper (signed requests)
│   ├── orders.py          # Order placement logic + output formatting
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup (file + console)
├── cli.py                 # CLI entry point (argparse)
├── .env.example           # API credentials template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Get Testnet API Credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Click **"API Key"** → copy your **API Key** and **Secret Key**

4. "Binance Futures Testnet is geo-restricted in India. Log files are simulated using identical Binance API response structure for demonstration purposes."

### 2. Clone & Install

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure Credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```



---

## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
```

### All arguments

| Argument       | Short | Required          | Description                        |
|----------------|-------|-------------------|------------------------------------|
| `--symbol`     | `-s`  | ✅ Yes            | Trading pair e.g. `BTCUSDT`        |
| `--side`       |       | ✅ Yes            | `BUY` or `SELL`                    |
| `--type`       | `-t`  | ✅ Yes            | `MARKET` or `LIMIT`                |
| `--quantity`   | `-q`  | ✅ Yes            | Quantity e.g. `0.01`               |
| `--price`      | `-p`  | ✅ For LIMIT only | Limit price e.g. `95000`           |

---

## Logging

Logs are saved in the `logs/` directory as `trading_YYYYMMDD.log`.

Each run logs:
- API request params (excluding signature)
- Raw API response
- Validation errors
- Network/API errors

---

## Assumptions

- Uses **Binance Futures Testnet (USDT-M)** only — not mainnet
- Minimum quantity for BTCUSDT on testnet is `0.001`
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- Credentials are loaded from a `.env` file using `python-dotenv`
- No real funds are involved — testnet only

---

## Example Output

```
  🔗 Connecting to Binance Futures Testnet...
  ✅ Connected successfully.

==================================================
         ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
==================================================

--------------------------------------------------
         ORDER RESPONSE
--------------------------------------------------
  Order ID   : 3279890123
  Status     : FILLED
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Exec. Qty  : 0.01
  Avg Price  : 94823.5
--------------------------------------------------
  ✅ Order placed successfully!
--------------------------------------------------
```
