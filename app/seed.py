from dbs import Stocks, db, app, MonthlyAdj
import json, requests

# apikey = 'W1IZOWOCKK0XHEFE'

stocksURL = "https://www.alphavantage.co/query"

sampleTickers = ["IBM", "GOOG", "AAPL"]


for i in sampleTickers:
    stocksParams = {"function": "OVERVIEW", "apikey": "W1IZOWOCKK0XHEFE", "symbol": i}
    r = requests.get(stocksURL, params=stocksParams)
    stocksData = r.json()

with open(stocksData, "r") as file:
    IDdata = json.load(file)

with app.app_context():
    # Deleting the data in the table( if exist )
    try:
        num_rows_deleted = db.session.query(Stocks).delete()
        db.session.commit()
        print(f"Deleted {num_rows_deleted} rows from Stocks.")

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting rows: {e}")

    # Accesing the data inside the db.json file
    for entry in IDdata:
        new_item = Stocks(
            ticker=entry.get("Symbol"),
        )

        db.session.add(new_item)
        db.session.commit()

    for entry in IDdata:
        new_item = Stocks(
            companyName=entry.get("Name"),
        )

        db.session.add(new_item)

    for entry in IDdata:
        new_item = Stocks(
            sector=entry.get("Sector"),
        )

        db.session.add(new_item)

    for entry in IDdata:
        new_item = Stocks(
            description=entry.get("Description"),
        )

        db.session.add(new_item)

    for entry in IDdata:
        new_item = Stocks(
            address=entry.get("Address"),
        )

        db.session.add(new_item)

    for entry in IDdata:
        new_item = Stocks(
            assetType=entry.get("AssetType"),
        )

        db.session.add(new_item)

    # Adding it to the table
    for i in sampleTickers:
        monthly_timeseries = {
            "symbol": sampleTickers[i],
            "function": "OVERVIEW",
            "apikey": "W1IZOWOCKK0XHEFE",
        }
        r = requests.get(stocksURL, params=monthly_timeseries)
        data = r.json()
        new_item = MonthlyAdj(ticker=sampleTickers[i])
        db.session.add(new_item)
        for entry in data["Monthly Adjusted Time Series"]:
            x = data["Monthly Adjusted Time Series"][entry]["5. adjusted close"]
            new_item = MonthlyAdj(adjClose=x)
            db.session.add(new_item)
            x = data["Monthly Adjusted Time Series"][entry]["6. volume"]
            new_item = MonthlyAdj(volume=x)
            db.session.add(new_item)

    try:
        db.session.commit()
        print("Data stored successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error importing data: {e}")
