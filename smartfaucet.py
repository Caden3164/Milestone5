import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define the two faucets
faucets = ["Bathroom_1", "Bathroom_2"]

# Set start and end dates for one week
start_date = datetime(2023, 1, 1)  # Example start date
end_date = start_date + timedelta(days=7)

# Initialize empty list to hold data
data = []

# Generate data for each faucet
for faucet in faucets:
    current_date = start_date
    while current_date < end_date:
        # Generate random number of usage events per day (4-6)
        usage_events = np.random.randint(4, 7)
        for _ in range(usage_events):
            # Random time of the day
            time_of_day = timedelta(
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            timestamp = current_date + time_of_day
            # Random water usage in liters (between 0.1 and 1.5 liters)
            usage_liters = round(np.random.uniform(0.1, 1.5), 2)
            # Append entry to the data list
            data.append([timestamp, faucet, usage_liters])
        # Move to the next day
        current_date += timedelta(days=1)

# Create DataFrame
df = pd.DataFrame(data, columns=["timestamp", "faucet_id", "usage_liters"])

# Save to CSV
df.to_csv("faucet_usage_data.csv", index=False)

print("Data has been saved to 'faucet_usage_data.csv'")
