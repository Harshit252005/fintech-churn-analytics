# ⚡ FinTech Churn & Revenue Risk Analytics Engine

An end-to-end data engineering and predictive financial analytics engine built for digital wealth management platforms. This system processes high-volume transaction data, executes complex SQL analytics, trains machine learning models to predict customer attrition, and quantifies dollar-denominated revenue risks in an executive Streamlit dashboard.

---

## 📌 Features & Key Capabilities

* **High-Performance SQL Processing**: Built on **DuckDB** to execute analytical queries across 60,000+ transaction records and 5,000 wealth accounts.
* **RFM Behavioral Segmentation**: Applied advanced SQL CTEs and `NTILE` window functions to evaluate Recency, Frequency, and Monetary (RFM) customer scores.
* **Predictive Risk Modeling**: Trained a **Gradient Boosting Classifier** (`scikit-learn`) using behavioral telemetry (app logins, support tickets, transaction frequency) to predict 30-day churn probability.
* **Financial Risk Quantification**: Calculated dynamic financial exposure:
  $$\text{Revenue at Risk} = P(\text{Churn}) \times \text{Total Customer Value}$$
* **Interactive Executive Dashboard**: Deployed a multi-tab **Streamlit** dashboard featuring cohort analytics, segment breakdowns, and actionable high-risk account filters.

---

## 🛠️ Tech Stack

* **Data Engineering & SQL**: DuckDB, Pandas, NumPy
* **Machine Learning**: Scikit-Learn (GradientBoostingClassifier), SciPy
* **Data Visualization & UI**: Streamlit, Plotly Express
* **Environment & Version Control**: Python 3.12, Git, macOS ARM

---

## 📁 Repository Structure

```text
fintech-churn-analytics/
├── data/                      # Generated CSV datasets & ML model predictions
├── sql/                       # Core SQL analytical scripts
│   ├── category_clv.sql       # Category-level CLV & AOV analysis
│   ├── cohort_analysis.sql    # Monthly behavioral retention cohorts
│   └── rfm_segmentation.sql   # RFM segmentation via CTEs & window functions
├── app.py                     # Streamlit interactive dashboard application
├── eda_and_sql.py             # DuckDB query execution driver script
├── generate_data.py          # Synthetic financial dataset generator
├── train_model.py             # Machine learning pipeline & risk scoring engine
├── requirements.txt           # Environment dependencies
└── README.md                  # Project documentation