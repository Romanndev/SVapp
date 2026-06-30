# SVapp

**SVapp** (Stock Valuation app) is an application designed to automate the preliminary evaluation of a stock's fair value based on fundamental metrics.

> ⚠️ **Disclaimer:** The calculation results are for informational purposes only and do not constitute financial advice.

---

## 🚀 How It Works

1. **Data Reading:** The application reads a list of target tickers from a text file named `list_of_tickers.txt`.
2. **Data Parsing:** The script fetches the required financial metrics from the [Yahoo Finance (CA)](https://ca.finance.yahoo.com/) website.
3. **Calculation & Storage:** The fair value is calculated based on the collected data, and the results are then saved to a local SQLite database (`BD_tickers.sqlite`).

---

## 🛠️ Tech Stack

The project is built using **Python** and relies on the following libraries and tools:

* **Development Language:** Python 3.x
* **Data Collection & Parsing:**
    * [`yfinance`](https://github.com/ranaroussi/yfinance) — used to fetch financial analytics, EPS, and BVPS metrics directly from the Yahoo Finance API.
    * [`requests`](https://requests.readthedocs.io/) — used for handling HTTP requests to interact with web resources.
* **Mathematical Calculations:**
    * `math` — a built-in Python module (specifically using `math.sqrt()` to calculate the square root in the Graham formula).
* **Data Storage:**
    * `sqlite3` — a built-in lightweight DBMS used to store tickers, calculation history, and evaluation results locally.

---

## ⚙️ Limitations and Exceptions

* 🇨🇦 **Market:** Currently, the application only processes tickers from the Toronto Stock Exchange (using the `.TO` suffix).
* 🏢 **Asset Type:** The program is designed exclusively for corporate stocks. **ETFs are not supported**.
* 🚫 **Exceptions:** Real Estate Investment Trusts (REITs) and income funds (using the `.UN` suffix) are temporarily unsupported.

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