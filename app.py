from flask import Flask, render_template, jsonify
import requests
import os


app = Flask("mondo_loyalty")

points = {"Starbucks": 5}


@app.route("/", methods={'GET'})
def home():
    token = os.environ['TOKEN']
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get("https://staging-api.getmondo.co.uk/transactions?expand[]=merchant&account_id=acc_000095qmPpiHooW8Mllzov", headers=headers)
    transactions = response.json()["transactions"]

    summary = {}

    for t in transactions:
      if not t["merchant"]:
        continue

      merchant_name = t["merchant"]["name"] #get the key merchant from last, the dictionary. Then get name from merchant dictionary.
      if merchant_name != "Starbucks":
        continue

      points_this_transaction = points[merchant_name] * int(t["amount"] / 100.0) * -1
      if merchant_name not in summary:
        logo_url = t["merchant"]["logo"]
        summary[merchant_name] = {"logo": logo_url, "points": points_this_transaction}
      else:
        data = summary[merchant_name]
        data["points"] += points_this_transaction


    return jsonify(**summary)

app.run(debug=True)
