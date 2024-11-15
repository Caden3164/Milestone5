import pandas as pd

# Load the data
df = pd.read_csv("faucet_usage_data.csv")

# Display the first few rows
print(df.head())

# Calculate total water usage per faucet
total_usage = df.groupby("faucet_id")["usage_liters"].sum()
print("\nTotal water usage (liters) per faucet:\n", total_usage)

# Calculate daily water usage for each faucet
df['date'] = pd.to_datetime(df['timestamp']).dt.date
daily_usage = df.groupby(["date", "faucet_id"])["usage_liters"].sum().unstack()
print("\nDaily water usage (liters) per faucet:\n", daily_usage)
