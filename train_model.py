import duckdb
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# 1. Load Data via DuckDB
con = duckdb.connect()
con.execute("CREATE TABLE users AS SELECT * FROM 'data/users.csv'")
con.execute("CREATE TABLE transactions AS SELECT * FROM 'data/transactions.csv'")

# Load RFM Query
with open("sql/rfm_segmentation.sql", "r") as f:
    rfm_sql = f.read()

df = con.execute(rfm_sql).fetchdf()

# Merge user metrics
users_df = pd.read_csv("data/users.csv")
df = df.merge(users_df[['user_id', 'support_tickets_30d', 'app_logins_30d']], on='user_id')

# 2. Target Label & Features
df['is_churn'] = np.where((df['recency_days'] > 90) | (df['app_logins_30d'] < 5), 1, 0)

features = ['recency_days', 'total_transactions', 'total_monetary_value', 'support_tickets_30d', 'app_logins_30d']
X = df[features]
y = df['is_churn']

# Categorical One-Hot Encoding
X = pd.concat([X, pd.get_dummies(df[['account_tier', 'primary_product']], drop_first=True)], axis=1)

# 3. Train Gradient Boosting Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = GradientBoostingClassifier(
    n_estimators=100, 
    max_depth=4, 
    learning_rate=0.05, 
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"✅ Gradient Boosting Model Trained | ROC-AUC Score: {auc_score:.4f}")

# 4. Quantify Revenue at Risk ($)
df['churn_probability'] = model.predict_proba(X)[:, 1]
df['revenue_at_risk_usd'] = np.round(df['churn_probability'] * df['total_monetary_value'], 2)

# Save processed output for UI
df.to_csv("data/model_predictions.csv", index=False)
print("✅ Output successfully saved to 'data/model_predictions.csv'!")