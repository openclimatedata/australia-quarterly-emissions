import json
from pathlib import Path

import pandas as pd

root = Path(__file__).parents[1]

for gas in ["co2", "ch4", "n2o", "other"]:

    data = json.load(open(root / f"{gas}.json"))

    columns = ["Quarter"] + [
        item["G1"]
        for item in data["results"][0]["result"]["data"]["dsr"]["DS"][0]["SH"][0]["DM1"]
    ]

    values = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    rows = [
        [item["G0"]] + [float(i["M0"] if "M0" in i else 0) for i in item["X"]]
        for item in values
    ]

    df = pd.DataFrame(rows, columns=columns)
    df["Quarter"] = df["Quarter"].apply(
        lambda x: pd.Timestamp(x, unit="ms").strftime("%B %Y")
    )
    df = df.set_index("Quarter")
    df = df.round(2)

    df.to_csv(root / f"{gas}.csv")
