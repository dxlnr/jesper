<h1 align="center">
  <b>Jesper - AI based Trading Bot</b><br>
</h1>

### Get the Annual Report Readings of a Stock
```python
from jesper.valuation import annual_report_readings
from jesper.utils.style import readable_df

# Define the stock
stock = "AAPL"
# Get the report
df = annual_report_readings(stock)
# Print it to screen
print(f"\n\t{stock}\n".expandtabs(4))
print(readable_df(df))
```

### Calculate the Intrinsic Value of a Stock
```python
from jesper.eval_sheet import eval_value_based_stocks

# Calculate evaluation facilitating value based investing.
df = eval_value_based_stocks(sp500[:10])

# Apply styling for highlighting outstanding values.
df = df.round({'intrinsic value': 2})
df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)

# Print the final results.
print("\n", df, "\n")
```
