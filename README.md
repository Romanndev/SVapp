# SVapp

**SVapp** (Stock Valuation App) is an automated stock valuation tool built with FastAPI that applies Benjamin Graham's formula to companies listed on the Toronto Stock Exchange (TSX). It fetches live financial data via yfinance, calculates fair value, and exposes the results through a REST API, storing data in a **CockroachDB Serverless** cluster.

> ⚠️ **Disclaimer:** The calculation results are for informational purposes only and do not constitute financial advice.

---

## 🚀 How It Works

1. **Data Input:** Tickers are added individually via the API.
2. **Data Parsing:** The app fetches financial metrics (EPS, BVPS, current price) from [Yahoo Finance](https://ca.finance.yahoo.com/) using `yfinance`, with a spoofed browser session to avoid rate limiting.
3. **Calculation & Storage:** Fair value is calculated using Graham's formula, and results are stored in a **CockroachDB Serverless** database via `psycopg2`.
4. **API Access:** All data — updating, reading, filtering undervalued stocks — is exposed through a FastAPI REST API with Pydantic-validated schemas.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check / root endpoint |
| `GET` | `/ticker/tickers_for_buying` | Returns tickers currently flagged as undervalued |
| `GET` | `/ticker/ticker_info_by_name/{ticker}` | Returns ticker data by symbol |
| `POST` | `/ticker/create_ticker_in_db/{ticker}` | Adds a new ticker record by symbol, fetches data, and saves to DB |
| `PATCH` | `/ticker/update_status/{ticker}?status=...` | Updates the status of a ticker by symbol (`status` passed as a query parameter) |
| `DELETE` | `/ticker/delete_ticker/{ticker}` | Removes a ticker record by symbol |
| `GET` | `/get_scalar_docs` | Interactive API documentation (via Scalar) |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Data Validation:** Pydantic
- **Database:** [CockroachDB](https://www.cockroachlabs.com/) Serverless (`svapp-db`) — accessed via `psycopg2`
- **Data Collection & Parsing:**
  * [`yfinance`](https://github.com/ranaroussi/yfinance) — fetches EPS, BVPS, and current price from Yahoo Finance
  * [`requests`](https://requests.readthedocs.io/) — custom session with spoofed headers to handle anti-bot restrictions
  * `asyncio` (`TaskGroup` + `to_thread`) — fetches data for multiple tickers concurrently
- **Database Connectivity:**
  * [`psycopg2`](https://www.psycopg.org/) — connects to CockroachDB (PostgreSQL wire protocol)
- **API Docs:** [Scalar](https://github.com/scalar/scalar) — interactive API reference
- **Mathematical Calculations:**
  * `math` — square root calculation for Graham's formula

---

## ⚙️ Limitations and Exceptions

- 🇨🇦 **Market:** Currently, the application only processes tickers from the Toronto Stock Exchange (using the `.TO` suffix).
- 🏢 **Asset Type:** The program is designed exclusively for corporate stocks. **ETFs are not supported**.
- 🚫 **Exceptions:** Real Estate Investment Trusts (REITs) and income funds (using the `.UN` suffix) are temporarily unsupported.

---

## 🧮 Methodology: The Graham Number

The valuation is based on the **Graham Number** — a classic metric for defensive (conservative) investors introduced by Benjamin Graham in his book *"The Intelligent Investor"*.

Graham established a rule stating that for a defensive investor, the product of the Price-to-Earnings ($P/E$) ratio and the Price-to-Book ($P/B$) ratio should not exceed **22.5** (where $P/E \le 15$ and $P/B \le 1.5$).

### Valuation Formula:

$$V = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}$$

Where:
* **EPS (Earnings Per Share):** The company's net earnings allocated to each outstanding share of common stock.
* **BVPS (Book Value Per Share):** The book value of the company per outstanding share.

> 💡 **Interpretation Rule:** If the current market price of a stock is lower than the calculated Graham Number ($V$), the company is potentially considered undervalued.

---

## 📥 Installation & Running

Follow these steps to set up and run the application locally:

1. **Install required dependencies:**
   Make sure you have Python installed. You can install all required libraries at once using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the database connection:**
   The app reads the connection string directly from the `DATABASE_URL` environment variable (`os.environ["DATABASE_URL"]`) — there's no `.env` auto-loading, so it must be set in your shell or system environment before running the app. Get the connection string from the CockroachDB Cloud console → **Connect** → language **Python**, tool **Psycopg2**:
   ```bash
   # macOS/Linux
   export DATABASE_URL="postgresql://admin-svapp:PASSWORD@svapp-db-33183.j77.aws-us-east-1.cockroachlabs.cloud:26257/svapp-db?sslmode=verify-full&sslrootcert=system"
   ```
   ```powershell
   # Windows (PowerShell)
   $env:DATABASE_URL="postgresql://admin-svapp:PASSWORD@svapp-db-33183.j77.aws-us-east-1.cockroachlabs.cloud:26257/svapp-db?sslmode=verify-full&sslrootcert=system"
   ```
   Replace `PASSWORD` with your actual credentials. `sslrootcert=system` uses your OS's trusted certificate store, so there's no need to download or reference a separate CA cert file.
   > 🔐 Never commit real credentials — if you keep them in a local `.env` file for reference, make sure it's listed in `.gitignore`. On deployment platforms like Render, set `DATABASE_URL` as an environment variable in the service settings instead.

3. **Launch the application:**
   Run the main script using Python:
   ```bash
   python SVapp.py
   ```
   or with auto-reload via Uvicorn:
   ```bash
   uvicorn SVapp:app --reload
   ```

4. **Explore the API:**
   Once running, visit `/get_scalar_docs` for interactive API documentation.