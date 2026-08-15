# SVapp

**SVapp** (Stock Valuation App) is an automated stock valuation tool built with FastAPI that applies Benjamin Graham's formula to companies listed on the Toronto Stock Exchange (TSX). It fetches live financial data via yfinance, calculates fair value, and exposes the results through a REST API.

> ⚠️ **Disclaimer:** The calculation results are for informational purposes only and do not constitute financial advice.

---

## 🚀 How It Works

1. **Data Reading:** Tickers are read from `list_of_tickers.txt` or added individually via the API.
2. **Data Parsing:** The app fetches financial metrics (EPS, BVPS, current price) from [Yahoo Finance](https://ca.finance.yahoo.com/) using `yfinance`, with a spoofed browser session to avoid rate limiting.
3. **Calculation & Storage:** Fair value is calculated using Graham's formula, and results are stored in a local SQLite database (`tickers.db`).
4. **API Access:** All data — updating, reading, filtering undervalued stocks — is exposed through a FastAPI REST API with Pydantic-validated schemas.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ticker/upload_tickers_from_file` | Loads tickers from file, fetches data, and saves to DB |
| `POST` | `/ticker/update_all_tickers` | Refreshes data and valuation status for all tickers |
| `GET` | `/ticker/tickers_for_buying` | Returns tickers currently flagged as undervalued |
| `GET` | `/ticker/ticker_info_by_name/{ticker}` | Returns ticker data by symbol |
| `POST` | `/ticker/create_ticker_in_db` | Adds a new ticker record manually |
| `PATCH` | `/ticker/update_status/{id}` | Updates the status of a ticker |
| `DELETE` | `/ticker/delete_ticker/{id}` | Removes a ticker record |
| `GET` | `/get_scalar_docs` | Interactive API documentation (via Scalar) |

---

## 🛠️ Tech Stack

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

2. **Prepare the input file:**
   Create a text file named `list_of_tickers.txt` in the root directory of the project and add your target Canadian tickers (e.g., `TD`, `LNR`), each on a new line.

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