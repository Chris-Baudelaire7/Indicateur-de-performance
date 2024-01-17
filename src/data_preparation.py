import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


data = pd.read_csv("data/sales_data.csv")

data.drop(index=data.index[-1], inplace=True)
data.Revenues = data.Revenues.str.replace(",", "")
data.Target = data.Target.str.replace(",", "")

data["Total Cost (Sales & Marketing)"] = data["Total Cost (Sales & Marketing)"].str.replace(",", "")

data.Revenues = data.Revenues.str.replace(",", "")
data.Target = data.Target.str.replace(",", "")
data["Total Cost (Sales & Marketing)"] = data["Total Cost (Sales & Marketing)"].str.replace(",", "")

for col in data.iloc[:, 1:]:
    data[col] = data[col].astype(int)
    
data["Revenues_difference"] = data.Revenues.diff(1)
data["pct_change"] = data.Revenues.pct_change() * 100

data = data.copy().fillna(0)
filter_by_month = data[data.Months == "FEB"]

revenues = filter_by_month.Revenues.iloc[0]
revenues_diference = filter_by_month.Revenues_difference.iloc[0]

data["Profit"] = data["Revenues"] - data["Total Cost (Sales & Marketing)"]
data['Sales'] = data['Orders Placed']
data["AVG / Customers"] = data["Revenues"] / data["Customers"]
