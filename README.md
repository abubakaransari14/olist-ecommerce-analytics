# Olist E-Commerce Analytics

An end-to-end data analytics project using the Brazilian Olist e-commerce dataset.

This project demonstrates a complete analytics workflow — from **raw data profiling and ETL to exploratory analysis, statistical hypothesis testing, machine learning, SQL Server data warehousing, and Power BI dashboarding**.

---

## 📌 Project Overview

The objective of this project is to analyze Olist's e-commerce operations and answer important business questions related to:

* Sales and revenue
* Customer behavior
* Product and category performance
* Seller performance
* Delivery performance
* Customer reviews
* Payment methods
* Repeat customers
* Customer segmentation
* Statistical relationships between delivery and customer satisfaction
* Prediction of late deliveries

The project follows a structured data analytics workflow rather than performing all analysis in a single notebook.

---

## 🎯 Business Objectives

The analysis focuses on the following questions:

### Sales & Revenue

* How does revenue change over time?
* Which states and cities generate the most revenue?
* What is the average order value?
* Which product categories generate the most revenue?
* How does monthly revenue change?

### Customer Analytics

* How many unique customers are there?
* How many customers make repeat purchases?
* What is the repeat customer rate?
* Which customers generate the most revenue?
* What are the different RFM customer segments?

### Product & Seller Analytics

* Which products generate the most revenue?
* Which categories have the highest sales?
* Which sellers generate the most revenue?
* How does seller location relate to business performance?

### Delivery & Customer Experience

* What is the average delivery time?
* What percentage of orders are delivered late?
* Which states have higher late-delivery rates?
* How are customer review scores distributed?
* Is delivery performance associated with customer reviews?

### Machine Learning

* Can late deliveries be predicted?
* Which features are important for predicting late deliveries?
* How do Logistic Regression and Random Forest perform?

---

# 🏗️ Project Architecture

```text
                         OLIST RAW DATA
                              │
                              ▼
                    ┌─────────────────────┐
                    │ 01 DATA PROFILING   │
                    │                     │
                    │ Missing values      │
                    │ Duplicates          │
                    │ Data types          │
                    │ Invalid values      │
                    │ Relationships       │
                    │ Data grain          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       ETL           │
                    │                     │
                    │ Extract             │
                    │ Transform           │
                    │ Validate            │
                    │ Load                │
                    └──────────┬──────────┘
                               │
                               ▼
                     PROCESSED DATA
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      02 DATA EXPLORATION  03 STATISTICS   04 MACHINE LEARNING
              │                │                │
              ▼                ▼                ▼
        Business Insights  Hypothesis      Prediction
        & Visualization     Testing         Models
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         SQL SERVER
                               │
                               ▼
                       DATA WAREHOUSE
                               │
                               ▼
                           POWER BI
                               │
                               ▼
                       BUSINESS DASHBOARD
```

---

# 📂 Project Structure

```text
olist-ecommerce-analytics/
│
├── data/
│   ├── raw/
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── processed/
│
├── notebooks/
│   ├── olistDataProfiling.ipynb
│   ├── olistEDA.ipynb
│   ├── statisticalAnalysis.ipynb
│   └── machineLearning.ipynb
│
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   └── pipeline.py
│
├── reports/
│   ├── eda/
│   ├── statistical/
│   ├── figures/
│   └── ml/
│
├── sql/
│   ├── KPIs.sql
│   └── businessAnalysis.sql
│
├── powerbi/
│   └── OlistEcommerceAnalytics.pbix
│
├── requirements.txt
└── README.md
```

---

# 🗃️ Dataset

The project uses the **Brazilian Olist e-commerce public dataset**.

The dataset contains approximately 100,000 orders from 2016–2018 and includes information about:

* Orders
* Customers
* Sellers
* Products
* Order items
* Payments
* Reviews
* Geolocation
* Product categories

### Main datasets

| Dataset              | Description                               |
| -------------------- | ----------------------------------------- |
| Customers            | Customer information and location         |
| Orders               | Order status and timestamps               |
| Order Items          | Products purchased within orders          |
| Payments             | Payment methods and installments          |
| Reviews              | Customer review scores                    |
| Products             | Product information                       |
| Sellers              | Seller information and location           |
| Geolocation          | Brazilian ZIP-code geographic information |
| Category Translation | Portuguese → English category names       |

---

# 🔎 01 — Data Profiling

The first stage examines the raw data before applying transformations.

The profiling process checks:

* Dataset dimensions
* Column names
* Data types
* Missing values
* Duplicate records
* Duplicate business keys
* Unique values
* Numeric ranges
* Invalid values
* Negative values
* Date ranges
* Relationships between datasets
* Potential derived columns

Examples of relationships checked include:

```text
orders.customer_id
        ↓
customers.customer_id
```

```text
order_items.order_id
        ↓
orders.order_id
```

```text
order_items.product_id
        ↓
products.product_id
```

```text
order_items.seller_id
        ↓
sellers.seller_id
```

The profiling stage is used to determine the appropriate ETL rules rather than blindly removing data.

---

# 🔄 02 — ETL Pipeline

The ETL pipeline is implemented using Python.

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
```

### Extract

Loads the raw CSV files from:

```text
data/raw/
```

### Transform

Transformations include:

* Datetime conversion
* Standardizing text fields
* Standardizing state codes
* Creating purchase date attributes
* Calculating delivery duration
* Calculating delivery delay
* Creating late-delivery indicators
* Calculating order-item value
* Handling appropriate missing values

### Validate

The pipeline checks important data-quality rules such as:

* Duplicate keys
* Invalid prices
* Invalid delivery durations
* Duplicate order items
* Duplicate customers

### Load

The transformed datasets are saved to:

```text
data/processed/
```
```text
MYSQLWORKBENC (LOCALHOST)
```
This creates reusable cleaned datasets for downstream analysis.

---

# 📊 03 — Data Exploration

The EDA stage focuses on business questions rather than data cleaning.

### Sales Analysis

* Monthly orders
* Monthly revenue
* Average order value
* Revenue by state
* Revenue by city
* Revenue trends

### Customer Analysis

* Customer order frequency
* Customer revenue
* Repeat customers
* RFM analysis
* Customer segmentation

### Product Analysis

* Product revenue
* Product volume
* Product category revenue
* Average product price

### Payment Analysis

* Payment method distribution
* Payment value
* Installment analysis

### Delivery Analysis

* Average delivery time
* Median delivery time
* Late-delivery rate
* Delivery performance by state

### Review Analysis

* Review score distribution
* Review score vs delivery performance

### Seller Analysis

* Seller revenue
* Seller order volume
* Seller location

EDA outputs are saved in:

```text
reports/eda/
```

Visualizations are saved in:

```text
reports/figures/
```

---

# 📐 04 — Statistical Analysis

Two statistical hypothesis tests were performed.

## Test 1 — Mann–Whitney U Test

### Business Question

> Do review scores differ between late and on-time deliveries?

The test compares the review-score distributions of:

```text
On-time deliveries
vs
Late deliveries
```

### Results

| Metric                    |        Result |
| ------------------------- | ------------: |
| On-time orders            |        91,523 |
| Late orders               |         7,701 |
| On-time median review     |           5.0 |
| Late median review        |           2.0 |
| U statistic               | 538,376,866.5 |
| Rank-biserial effect size |        ~0.528 |
| p-value                   |        < 0.05 |

The result provides statistical evidence that review-score distributions differ between late and on-time deliveries.

---

## Test 2 — Spearman Rank Correlation

### Business Question

> Is delivery duration associated with review score?

### Result

| Metric       |  Result |
| ------------ | ------: |
| Observations |  96,359 |
| Spearman ρ   | -0.2344 |
| p-value      |  < 0.05 |

The result indicates a statistically significant **negative monotonic association** between delivery duration and review score within the analyzed dataset.

In other words, longer delivery durations tend to be associated with lower review scores.

### Important Limitation

Statistical association does not establish causation.

Other factors may also influence customer reviews, including:

* Product characteristics
* Seller performance
* Geographic location
* Freight conditions
* Customer expectations
* Order characteristics

---

# 🤖 05 — Machine Learning

The machine-learning stage focuses on predicting whether an order will experience late delivery.

## Prediction Target

```text
is_late
```

The project uses two classification algorithms:

### Logistic Regression

Used as an interpretable baseline classification model.

### Random Forest

Used to capture nonlinear relationships and interactions between features.

---

## Feature Engineering

Potential predictive features include:

* Customer state
* Seller state
* Number of items
* Total product price
* Total freight
* Total order value
* Number of unique categories
* Purchase hour
* Purchase day of week
* Purchase month
* Approval delay
* Estimated delivery duration
* Same-state customer/seller indicator

### Data Leakage Prevention

Features that become available only after delivery are excluded from prediction.

Examples:

```text
delivery_days
delivery_delay_days
order_delivered_customer_date
order_delivered_carrier_date
```

This ensures that the model attempts to predict late delivery using information available before the delivery outcome is known.

---

## Model Evaluation

Models are evaluated using:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion Matrix
* ROC Curve
* Feature Importance

The model comparison results are saved under:

```text
reports/ml/
```

---

# 🗄️ 06 — SQL Server & Data Warehouse

The cleaned data is loaded into SQL Server for structured analytics.

Database:

```text
OlistAnalytics
```


# ⭐ Data Warehouse


### Tables

```text
orders
customers
order_items
order_payments
order_reviews
geolocation
category_translation
sellers
products
```


```

This structure separates descriptive dimensions from transactional facts and supports efficient analytical queries.

---

# 🧮 SQL Analysis

SQL is used for business analysis including:

* Monthly revenue
* Monthly orders
* Revenue by state
* Revenue by city
* Revenue by category
* Average order value
* Order-status analysis
* Payment analysis
* Delivery performance
* Late-delivery rate
* Review analysis
* Top sellers
* Repeat customers
* Customer revenue
* Category trends
* Rankings
* Running totals
* Month-over-month revenue growth

Advanced SQL concepts include:

```text
GROUP BY
JOIN
CASE
RANK()
LAG()
SUM() OVER()
Window Functions
```

---

# 📈 07 — Power BI Dashboard

Power BI is used to create an interactive business intelligence dashboard connected to the SQL Server data warehouse.

## Dashboard Pages

### 1. Executive Overview

Key KPIs:

* Total Revenue
* Total Orders
* Total Customers
* Total Products
* Total Sellers
* Average Order Value
* Average Delivery Days
* Late Delivery Rate
* Average Review Score

### 2. Sales & Revenue

* Monthly revenue
* Monthly orders
* Revenue growth
* Revenue by state
* Revenue by city
* Category performance

### 3. Customer Analytics

* Total customers
* Repeat customers
* Repeat customer rate
* Customer revenue
* RFM segmentation
* Customer segments

### 4. Product & Delivery Analytics

* Top products
* Delivery Status vs avg review
* Payment type revenue
* Category's orders
* Seller revenue

### 5. Delivery & Customer Experience

* Average delivery days
* Late delivery rate
* Delivery performance by state
* Review-score distribution
* Delivery vs review performance

### 6. About the Project

* Project objective
* Dataset
* Technologies
* Methodology
* Key findings

---

---

# 🛠️ Technologies Used

| Technology       | Purpose                                      |
| ---------------- | -------------------------------------------- |
| Python           | Data processing, ETL, EDA, statistics and ML |
| Pandas           | Data manipulation                            |
| NumPy            | Numerical analysis                           |
| SciPy            | Statistical hypothesis testing               |
| Matplotlib       | Data visualization                           |
| Scikit-learn     | Machine learning                             |
| SQL Server       | Database and data warehouse                  |
| SQL              | Data transformation and analysis             |
| Power BI         | Dashboard and business intelligence          |
| DAX              | Power BI measures                            |
| Jupyter Notebook | Analysis workflow                            |
| VS Code          | Development environment                      |
| Git/GitHub       | Version control and portfolio                |

---

# 📦 Python Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Step 1 — Add Raw Data

Place the Olist CSV files inside:

```text
data/raw/
```

---

## Step 2 — Run Data Profiling

Open:

```text
notebooks/olistDataProfiling.ipynb
```

Review the data-quality findings before running the ETL pipeline.

---

## Step 3 — Run ETL

From the project root:

```bash
python src/pipeline.py
```

The cleaned data will be generated in:

```text
data/processed/
```

---

## Step 4 — Run EDA

Open:

```text
notebooks/olistEDA.ipynb
```

EDA reports will be saved to:

```text
reports/eda/
```

Charts will be saved to:

```text
reports/figures/
```

---

## Step 5 — Run Statistical Analysis

Open:

```text
notebooks/statisticalAnalysis.ipynb
```

Statistical results will be saved to:

```text
reports/statistical/
```

---

## Step 6 — Run Machine Learning

Open:

```text
notebooks/machineLearning.ipynb
```

ML outputs will be saved to:

```text
reports/ml/
```

---

## Step 7 — Build SQL Server Database

Execute the SQL scripts in order:

```text
KPI's.sql
businessAnalysis.sql
```

---

## Step 8 — Open Power BI

Open:

```text
powerbi/OlistEcommerceAnalytics.pbix
```

Connect Power BI to the:

```text
OlistAnalytics
```

SQL Server database and use the data warehouse tables for reporting.

---

# 📊 Key Findings

The project identified several notable patterns in the Olist dataset.

### Delivery & Reviews

Statistical testing found evidence of differences in review-score distributions between late and on-time deliveries.

On-time deliveries had a median review score of:

```text
5.0
```

while late deliveries had a median review score of:

```text
2.0
```

The Mann–Whitney U test produced a rank-biserial effect size of approximately:

```text
0.528
```

### Delivery Duration & Reviews

Spearman correlation produced:

```text
ρ = -0.2344
```

indicating a negative monotonic association between delivery duration and review score.

These findings represent statistical associations in the analyzed dataset and should not be interpreted as causal relationships.

---

# 🚀 Future Improvements

Possible future extensions include:

* Hyperparameter tuning
* Cross-validation
* Model explainability with SHAP
* Customer churn prediction
* Customer clustering using K-Means
* More advanced delivery prediction
* Automated ETL scheduling
* SQL reporting views
* Power BI Row-Level Security
* Automated data-quality monitoring
* GitHub Actions for pipeline testing
* Cloud deployment
* Streamlit analytics application

---

# 📚 Skills Demonstrated

This project demonstrates practical experience in:

### Data Analytics

* Data cleaning
* Data profiling
* Exploratory data analysis
* Business KPI analysis
* Data visualization

### Data Engineering

* ETL pipeline development
* Data validation
* Data quality checks
* Data transformation
* Data warehouse design

### Statistics

* Hypothesis testing
* Mann–Whitney U test
* Spearman correlation
* p-value interpretation
* Effect size interpretation

### Machine Learning

* Feature engineering
* Classification
* Logistic Regression
* Random Forest
* Train/test splitting
* Model evaluation
* Precision
* Recall
* F1-score
* ROC-AUC
* Feature importance

### SQL & BI

* SQL Server
* Star schema
* SQL analytical queries
* Window functions
* DAX
* Power BI dashboards

---

# 👤 Author

**Muhammad Abu Bakar Ansari**

Data Analytics | Python | SQL | Power BI | Machine Learning

---

# 📌 Disclaimer

This project is intended for educational and portfolio purposes.

The analysis is based on the publicly available Olist dataset and reflects patterns observed within that dataset. Statistical relationships identified in the analysis should not automatically be interpreted as causal relationships.
