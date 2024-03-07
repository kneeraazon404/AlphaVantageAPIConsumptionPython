from app import app, forms, lm
from app.forms import *
from app.dbs import *
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_required, current_user, logout_user
import requests


@lm.user_loader
def load_user(user_id):
    return User.get(user_id)


API_KEY = "demo"


@app.route("/")
def index():
    print(API_KEY)
    market_status_url = (
        f"https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={API_KEY}"
    )
    top_gainers_losers_url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}"

    market_status_response = requests.get(market_status_url)
    market_status_data = market_status_response.json()

    # print(f"Market status data: {market_status_data}")

    # Check if market status data is empty and create dummy data if necessary
    if not market_status_data or "Note" in market_status_data:
        market_status_data = {
            "status": "Unavailable",
            "message": "Market status data not available",
        }

    top_gainers_losers_response = requests.get(top_gainers_losers_url)
    top_gainers_losers_data = top_gainers_losers_response.json()
    #  print(f"Top gainers and losers data: {top_gainers_losers_data}")
    # # Check if top gainers and losers data is empty and create dummy data if necessary

    if market_status_data is None:
        market_status_data = {
            "markets": [
                {
                    "region": "North America",
                    "market_type": "Stock",
                    "primary_exchanges": "NYSE, NASDAQ",
                    "local_open": "09:30",
                    "local_close": "16:00",
                    "current_status": "open",
                    "notes": "No unusual activity.",
                },
                {
                    "region": "Europe",
                    "market_type": "Stock",
                    "primary_exchanges": "LSE, Euronext",
                    "local_open": "08:00",
                    "local_close": "16:30",
                    "current_status": "closed",
                    "notes": "Early closure due to holiday.",
                },
                {
                    "region": "Asia",
                    "market_type": "Stock",
                    "primary_exchanges": "SSE, HKEX, TSE",
                    "local_open": "09:00",
                    "local_close": "15:00",
                    "current_status": "closed",
                    "notes": "Normal trading hours.",
                },
                {
                    "region": "Australia",
                    "market_type": "Stock",
                    "primary_exchanges": "ASX",
                    "local_open": "10:00",
                    "local_close": "16:00",
                    "current_status": "open",
                    "notes": "No unusual activity.",
                },
            ]
        }
    if not top_gainers_losers_data["top_gainers"]:

        top_gainers_losers_data = {
            "metadata": "Top gainers, losers, and most actively traded US tickers",
            "last_updated": "2024-01-02 12:00:00 US/Eastern",
            "top_gainers": [
                {"ticker": "AAPL", "percentage_change": "5.4%"},
                {"ticker": "MSFT", "percentage_change": "4.8%"},
                {"ticker": "AMZN", "percentage_change": "4.2%"},
                {"ticker": "GOOGL", "percentage_change": "3.9%"},
                {"ticker": "FB", "percentage_change": "3.7%"},
                {"ticker": "TSLA", "percentage_change": "3.5%"},
                {"ticker": "BRK.A", "percentage_change": "3.2%"},
                {"ticker": "V", "percentage_change": "2.9%"},
                {"ticker": "JPM", "percentage_change": "2.5%"},
                {"ticker": "JNJ", "percentage_change": "2.3%"},
            ],
            "top_losers": [
                {"ticker": "NFLX", "percentage_change": "-5.1%"},
                {"ticker": "NVDA", "percentage_change": "-4.7%"},
                {"ticker": "PYPL", "percentage_change": "-4.3%"},
                {"ticker": "INTC", "percentage_change": "-3.8%"},
                {"ticker": "CSCO", "percentage_change": "-3.4%"},
                {"ticker": "ORCL", "percentage_change": "-3.2%"},
                {"ticker": "ADBE", "percentage_change": "-2.9%"},
                {"ticker": "CRM", "percentage_change": "-2.5%"},
                {"ticker": "IBM", "percentage_change": "-2.2%"},
                {"ticker": "QCOM", "percentage_change": "-2.0%"},
            ],
            "most_actively_traded": [
                {"ticker": "BAC", "volume": "1.2M"},
                {"ticker": "C", "volume": "1.1M"},
                {"ticker": "WFC", "volume": "1.0M"},
                {"ticker": "HSBC", "volume": "900K"},
                {"ticker": "JPM", "volume": "850K"},
                {"ticker": "GS", "volume": "800K"},
                {"ticker": "MS", "volume": "750K"},
                {"ticker": "USB", "volume": "700K"},
                {"ticker": "AXP", "volume": "650K"},
                {"ticker": "TD", "volume": "600K"},
            ],
        }

    return render_template(
        "index.html",
        market_status=market_status_data,
        top_gainers_losers=top_gainers_losers_data,
    )


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    user_name = db.session.query(User.fname).filter
    return render_template("profile.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = RegForm()
    if request.method == "POST" and form.validate_on_submit:
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return redirect(url_for("register"))
        elif not user.verify_password(form.password.data):
            flash("Incorrect password.", "message")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("profile"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if request.method == "POST" and form.validate:
        check_username = str(
            db.session.query(User.username)
            .filter(User.username == form.username.data)
            .scalar()
        )
        username = str(form.username.data)
        if username == check_username:
            flash("Username already in use", "message")
            return redirect(url_for("register"))
        elif username != check_username:
            User.register(
                form.username.data,
                form.email.data,
                form.fname.data,
                form.lname.data,
                form.password.data,
            )
            return redirect(url_for("profile"))
    elif not form.validate:
        flash("Something went wrong", "error")
    return render_template("register.html", form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/candlestick")
def candlestick():
    symbol = request.args.get("symbol", default="IBM", type=str)
    api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Alpha Vantage"}), 500

        data = response.json()
        if "Error Message" in data:
            return jsonify({"error": "Invalid symbol or query parameters"}), 400

        daily_data = data.get("Time Series (Daily)", {})

        candlestick_data = [
            {
                "t": date,
                "o": float(daily_values["1. open"]),
                "h": float(daily_values["2. high"]),
                "l": float(daily_values["3. low"]),
                "c": float(daily_values["4. close"]),
            }
            for date, daily_values in daily_data.items()
        ]

        line_chart_data = [
            {
                "t": date,
                "c": float(daily_values["4. close"]),
            }
            for date, daily_values in daily_data.items()
        ]

        scatter_data = [
            {
                "t": date,
                "o": float(daily_values["1. open"]),
                "h": float(daily_values["2. high"]),
                "l": float(daily_values["3. low"]),
                "c": float(daily_values["4. close"]),
            }
            for date, daily_values in daily_data.items()
        ]

        # Package both data formats into a single response
        formatted_data = {
            "candlestick": candlestick_data,
            "line": line_chart_data,
            "scatter": scatter_data,
        }
        # print(formatted_data)

        return jsonify(formatted_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while fetching data"}), 500


def fetch_stock_data(symbol, api_key):
    """Fetch daily stock data from Alpha Vantage."""
    api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json().get("Time Series (Daily)", {})
        # Extract dates and closing prices
        dates = list(data.keys())
        closing_prices = [data[date]["4. close"] for date in dates]
        return {"dates": dates, "prices": closing_prices}
    else:
        return None


@app.route("/stock-data")
def stock_data():
    symbol_us = request.args.get(
        "symbol_us", default="AAPL", type=str
    )  # US stock symbol
    symbol_uk = request.args.get(
        "symbol_uk", default="AZN.L", type=str
    )  # UK stock symbol
    api_key = "YOUR_API_KEY_HERE"  # Replace with your Alpha Vantage API key

    # Fetch data for both stocks
    data_us = fetch_stock_data(symbol_us, api_key)
    data_uk = fetch_stock_data(symbol_uk, api_key)

    if data_us and data_uk:
        print(f"US stock data: {data_us}")
        print(f"UK stock data: {data_uk}")
        # Return both datasets
        return jsonify({"us_stock": data_us, "uk_stock": data_uk})
    else:
        return jsonify({"error": "Failed to fetch stock data"}), 500


@app.route("/chart")
def chart():
    return render_template("candlestick.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404
