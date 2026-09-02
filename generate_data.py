import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

np.random.seed(42)
num_users = 5000
num_transactions = 60000

# 1. User Profiles Table
start_date = datetime(2024, 1, 1)
user_ids = [f"USR_{10000 + i}" for i in range(num_users)]

signup_dates = [start_date + timedelta(days=int(np.random.randint(0, 500))) for _ in range(num_users)]
primary_products = np.random.choice(
    ["Equities", "Crypto", "High-Yield Savings", "Robo-Advisory"], 
    size=num_users, 
    p=[0.35, 0.25, 0.25, 0.15]
)
account_tiers = np.random.choice(
    ["Standard", "Gold", "VIP Wealth"], 
    size=num_users, 
    p=[0.60, 0.30, 0.10]
)

users_df = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": signup_dates,
    "primary_product": primary_products,
    "account_tier": account_tiers,
    "support_tickets_30d": np.random.poisson(lam=0.8, size=num_users),
    "app_logins_30d": np.random.randint(0, 45, size=num_users)
})

# 2. Transactions Table
tx_user_ids = np.random.choice(user_ids, size=num_transactions)
tx_dates = [start_date + timedelta(days=int(np.random.randint(0, 700))) for _ in range(num_transactions)]
product_categories = np.random.choice(["Equities", "Crypto", "High-Yield Savings", "Robo-Advisory"], size=num_transactions)

amounts = []
for prod in product_categories:
    if prod == "Crypto":
        amounts.append(round(np.random.exponential(scale=150) + 10, 2))
    elif prod == "Equities":
        amounts.append(round(np.random.exponential(scale=500) + 50, 2))
    elif prod == "High-Yield Savings":
        amounts.append(round(np.random.exponential(scale=1200) + 100, 2))
    else:
        amounts.append(round(np.random.exponential(scale=300) + 25, 2))

transactions_df = pd.DataFrame({
    "transaction_id": [f"TX_{100000 + i}" for i in range(num_transactions)],
    "user_id": tx_user_ids,
    "transaction_date": tx_dates,
    "product_category": product_categories,
    "amount_usd": amounts
})

# Save output
users_df.to_csv("data/users.csv", index=False)
transactions_df.to_csv("data/transactions.csv", index=False)

print("Data successfully generated in 'data/' folder!")
print(f"Users records: {len(users_df)}")
print(f"Transactions records: {len(transactions_df)}")