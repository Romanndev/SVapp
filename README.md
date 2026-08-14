 # SVapp

**SVapp** (Stock Valuation App) is an automated stock valuation tool built with FastAPI that applies Benjamin Graham's formula to companies listed on the Toronto Stock Exchange (TSX). It fetches live financial data via yfinance, calculates fair value, and exposes the results through a REST API.

> ⚠️ **Disclaimer:** The calculation results are for informational purposes only and do not constitute financial advice.

---

## 🚀 How It Works

[#-how-it-works](#-how-it-works)

1. **Data Reading:** Tickers are read from `list_of_tickers.txt` or added individually via the API.
2. **Data Parsing:** The app fetches financial metrics (EPS, BVPS, current price) from [Yahoo Finance](https://ca.finance.yahoo.com/) using `yfinance`, with a spoofed browser session to avoid rate limiting.
3. **Calculation & Storage:** Fair value is calculated using Graham's formula, and results are stored in a local SQLite database (`tickers.db`).
4. **API Access:** All data — updating, reading, filtering undervalued stocks — is exposed through a FastAPI REST API with Pydantic-validated schemas.

---

## 🔌 API Endpoints

[#-api-endpoints](#-api-endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ticker/upload_from_file` | Loads tickers from file, fetches data, and saves to DB |
| `POST` | `/ticker/update_all` | Refreshes data and valuation status for all tickers |
| `GET` | `/ticker/tickers_for_Buying` | Returns tickers currently flagged as undervalued |
| `GET` | `/ticker/{id}` | Returns ticker data by internal ID |
| `GET` | `/ticker/ticker_name/{ticker}` | Returns ticker data by symbol |
| `POST` | `/ticker/create` | Adds a new ticker record manually |
| `PATCH` | `/ticker/update/{status}` | Updates the status of a ticker |
| `DELETE` | `/ticker/delete/{id}` | Removes a ticker record |
| `GET` | `/scalar` | Interactive API documentation (via Scalar) |

---

## 🛠️ Tech Stack

[#️-tech-stack](#️-tech-stack)

- **Backend:** FastAPI + Uvicorn
- **Data Validation:** Pydantic
- **Database:** SQLite3
- **Data Collection & Parsing:**
  * [`yfinance`](https://github.com/ranaroussi/yfinance) — fetches EPS, BVPS, and current price from Yahoo Finance
  * [`requests`](https://requests.readthedocs.io/) — custom session with spoofed headers to handle anti-bot restrictions
- **API Docs:** [Scalar](https://github.com/scalar/scalar) — interactive API reference
- **Mathematical Calculations:**
  * `math` — square root calculation for Graham's formula

---

## ⚙️ Limitations and Exceptions

[#-limitations-and-exceptions](#️-limitations-and-exceptions)

- 🇨🇦 **Market:** Currently, the application only processes tickers from the Toronto Stock Exchange (using the `.TO` suffix).
- 🏢 **Asset Type:** The program is designed exclusively for corporate stocks. **ETFs are not supported**.
- 🚫 **Exceptions:** Real Estate Investment Trusts (REITs) and income funds (using the `.UN` suffix) are temporarily unsupported.

---

## 🧮 Methodology: The Graham Number

[#-methodology-the-graham-number](#-methodology-the-graham-number)

The valuation is based on the **Graham Number** — a classic metric for defensive (conservative) investors introduced by Benjamin Graham in his book *"The Intelligent Investor"*.

Graham established a rule stating that for a defensive investor, the product of the Price-to-Earnings ($P/E$) ratio and the Price-to-Book ($P/B$) ratio should not exceed **22.5** (where $P/E \le 15$ and $P/B \le 1.5$).

### Valuation Formula:

[#valuation-formula](#valuation-formula)

$$V = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}$$

Where:

- **EPS (Earnings Per Share):** The company's net earnings allocated to each outstanding share of common stock.
- **BVPS (Book Value Per Share):** The book value of the company per outstanding share.

> 💡 **Interpretation Rule:** If the current market price of a stock is lower than the calculated Graham Number ($V$), the company is potentially considered undervalued.

---

## ▶️ Running the App

[#️-running-the-app](#️-running-the-app)

```bash
uvicorn SVapp:app --reload
