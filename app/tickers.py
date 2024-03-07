import json, requests


def fetch_data_from_api(param):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={param}&apikey=W1IZOWOCKK0XHEFE"


def main():
    with open(r"THE-CURRENT-WEBSITE\app\stockID.json", "r") as file:
        IDdata = json.load(file)

    for param in IDdata["message"]:
        data = fetch_data_from_api(param)
