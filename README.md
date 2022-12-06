<h1 align="center">
  <b>Jesper - AI based Trading Bot</b><br>
</h1>

### Calculate the Intrinsic Value of a Stock

Intrinsic value is an all-important concept that offers the only logical approach to evaluating the relative attractiveness of investments and businesses. Intrinsic value can be defined simply: It is the discounted value of the cash that can be taken out of a business during its remaining life.

For more [information](https://finmasters.com/intrinsic-value/).

```python
from jesper.eval_sheet import eval_value_based_stocks

# Calculate evaluation facilitating value based investing.
df = eval_value_based_stocks(['AAPL', 'META'])

# Apply styling for highlighting outstanding values.
df['intrinsic value'] = df['intrinsic value'].astype(float).round(2)
df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)

# Print the final results.
print("\n", df, "\n")
```

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
