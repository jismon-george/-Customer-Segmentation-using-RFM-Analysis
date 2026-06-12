# 📊 Customer Segmentation using RFM Analysis

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Completed-success?style=for-the-badge)

---

# 📌 Project Overview

Customer retention is one of the most critical factors for business growth. Understanding customer purchasing behavior enables organizations to identify valuable customers, predict churn, and design personalized marketing strategies.

This project performs **Customer Segmentation using RFM (Recency, Frequency, Monetary) Analysis**, a widely used marketing analytics technique that categorizes customers based on their transaction history.

The project was developed as part of the **SyntecxHub Data Analytics Internship – Project 1** and demonstrates how customer data can be transformed into actionable business insights using Python and data visualization.

---

# 🎯 Objectives

The primary objectives of this project are:

- Analyze customer purchasing behavior.
- Calculate Recency, Frequency, and Monetary metrics.
- Generate customer RFM scores.
- Classify customers into meaningful business segments.
- Visualize customer distributions and revenue contribution.
- Provide targeted marketing recommendations.
- Build a complete customer segmentation dashboard.

---

# 🧠 What is RFM Analysis?

RFM stands for:

| Metric | Description |
|----------|-------------|
| **Recency (R)** | How recently a customer made a purchase |
| **Frequency (F)** | How often a customer purchases |
| **Monetary (M)** | How much money a customer spends |

Customers with:

- Low Recency → Purchased recently
- High Frequency → Purchase often
- High Monetary Value → Spend more money

are considered the most valuable customers.

---

# 🛠️ Tech Stack

| Category | Tools Used |
|-----------|------------|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Dataset | Simulated Customer Transactions |
| IDE | Jupyter Notebook / VS Code |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
Customer-Segmentation-using-RFM-Analysis/
│
├── README.md
├── rfm_analysis.py
├── transactions.csv
├── rfm_results.csv
├── rfm_dashboard.png
│
└── outputs/
    ├── rfm_results.csv
    ├── transactions.csv
    └── rfm_dashboard.png
```

---

# 📊 Dataset Information

The project simulates a retail customer dataset containing:

- 500 Customers
- 2000+ Transactions
- 2 Years of Purchase History

### Dataset Fields

| Column | Description |
|----------|------------|
| CustomerID | Unique Customer Identifier |
| OrderDate | Purchase Date |
| Amount | Transaction Value |

Example:

| CustomerID | OrderDate | Amount |
|------------|------------|---------|
| C0001 | 2024-03-14 | 215.67 |
| C0002 | 2024-08-02 | 89.25 |
| C0003 | 2024-11-10 | 420.50 |

---

# ⚙️ Project Workflow

## Step 1: Data Generation & Loading

The project generates realistic customer transaction data including:

- Loyal Customers
- Regular Customers
- New Customers
- Churn Risk Customers

```python
customer_types = np.random.choice(
    ['loyal', 'churn_risk', 'new', 'regular'],
    size=n_customers,
    p=[0.20, 0.25, 0.25, 0.30]
)
```

---

## Step 2: Data Cleaning

Data quality checks include:

```python
df = df.dropna()
df = df[df['Amount'] > 0]
df = df[df['OrderDate'] <= analysis_date]
```

### Cleaning Tasks

✅ Remove missing values

✅ Remove invalid transactions

✅ Remove future dates

✅ Ensure positive transaction values

---

## Step 3: Calculate RFM Metrics

```python
rfm = df.groupby('CustomerID').agg(
    Recency=('OrderDate',
             lambda x: (analysis_date - x.max()).days),
    Frequency=('OrderDate','count'),
    Monetary=('Amount','sum')
)
```

Generated Metrics:

### Recency

Days since last purchase.

### Frequency

Number of purchases.

### Monetary

Total spending by customer.

---

## Step 4: Generate RFM Scores

Customers receive scores from 1–5 for each metric.

### Recency Score

```python
rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    5,
    labels=[5,4,3,2,1]
)
```

### Frequency Score

```python
rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    5,
    labels=[1,2,3,4,5]
)
```

### Monetary Score

```python
rfm['M_Score'] = pd.qcut(
    rfm['Monetary'].rank(method='first'),
    5,
    labels=[1,2,3,4,5]
)
```

---

## Step 5: Compute Final RFM Score

```python
rfm['RFM_Score'] = (
    rfm['R_Score'] +
    rfm['F_Score'] +
    rfm['M_Score']
)
```

### Score Range

| Minimum | Maximum |
|----------|----------|
| 3 | 15 |

Higher scores indicate more valuable customers.

---

# 👥 Customer Segmentation Logic

Customers are categorized into six business segments.

```python
if total >= 12 and r >= 4:
    return 'Loyal'

elif r <= 2 and total <= 7:
    return 'Churn Risk'

elif r >= 4 and f <= 2:
    return 'New Customer'

elif total >= 9:
    return 'Promising'

elif r <= 2 and f >= 3:
    return 'At Risk'

else:
    return 'Regular'
```

---

# 🎯 Customer Segments

## 🏆 Loyal Customers

Characteristics:

- Recent purchases
- Frequent buyers
- High spending

Marketing Strategy:

- VIP rewards
- Early product access
- Premium loyalty benefits

---

## 🌟 Promising Customers

Characteristics:

- Good engagement
- Moderate spending

Marketing Strategy:

- Upselling campaigns
- Personalized offers

---

## 👋 New Customers

Characteristics:

- Recently acquired
- Limited purchase history

Marketing Strategy:

- Welcome offers
- Product education

---

## 📧 Regular Customers

Characteristics:

- Average activity

Marketing Strategy:

- Newsletters
- Seasonal promotions

---

## ⚠️ At Risk Customers

Characteristics:

- Less recent purchases
- Potential disengagement

Marketing Strategy:

- Win-back campaigns
- Discounts

---

## 🚨 Churn Risk Customers

Characteristics:

- Long inactive period
- Low purchase activity

Marketing Strategy:

- Retention offers
- Personal outreach

---

# 📈 Dashboard Visualizations

The project generates a complete analytical dashboard.

---

## 1️⃣ Customer Segment Distribution

### Doughnut Chart

Shows:

- Percentage of customers in each segment
- Overall customer composition

Insights:

- Loyal customers represent high-value users.
- Churn Risk customers highlight retention challenges.

---

## 2️⃣ Revenue Contribution by Segment

### Horizontal Bar Chart

Displays:

- Total revenue generated by each segment

Business Insight:

A small number of Loyal customers contribute a significant portion of total revenue.

---

## 3️⃣ RFM Score Distribution

### Box Plot

Visualizes:

- Score spread within each segment
- Customer quality consistency

Insights:

- Loyal customers maintain high scores.
- Churn Risk customers show lower scores.

---

## 4️⃣ Recency vs Monetary Analysis

### Scatter Plot

Shows relationship between:

- Purchase recency
- Customer spending

Insights:

- High spenders generally purchase more frequently.
- Churn customers tend to spend less and have longer inactivity periods.

---

# 📊 Dashboard Preview

## Customer Segmentation Dashboard

Features included:

- Segment Distribution
- Revenue Analysis
- RFM Score Comparison
- Customer Spend Analysis

The dashboard provides an executive-level summary of customer behavior and business value.

---

# 📈 Business Insights Generated

### Key Findings

✔ Loyal customers generate the highest revenue.

✔ Churn Risk customers form a significant portion of the customer base.

✔ Promising customers can be converted into loyal customers.

✔ New customers require onboarding campaigns.

✔ Retention strategies should prioritize high-value churn-risk customers.

---

# 💡 Marketing Recommendations

| Segment | Recommended Action |
|-----------|------------------|
| Loyal | VIP Programs, Rewards |
| Promising | Upsell & Cross-sell |
| New Customer | Welcome Campaigns |
| Regular | Newsletters |
| At Risk | Win-back Offers |
| Churn Risk | Aggressive Retention Strategies |

---

# 🚀 How to Run the Project

## Clone Repository

```bash
git clone https://github.com/yourusername/Customer-Segmentation-using-RFM-Analysis.git
```

## Navigate to Project Folder

```bash
cd Customer-Segmentation-using-RFM-Analysis
```

## Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn
```

## Run Analysis

```bash
python rfm_analysis.py
```

---

# 📤 Outputs Generated

### CSV Files

```text
transactions.csv
rfm_results.csv
```

### Dashboard

```text
rfm_dashboard.png
```

---

# 📚 Learning Outcomes

Through this project, the following skills were demonstrated:

- Customer Analytics
- RFM Segmentation
- Data Cleaning
- Feature Engineering
- Business Intelligence
- Data Visualization
- Marketing Analytics
- Customer Lifetime Value Concepts
- Python Data Analysis

---

# 🔮 Future Enhancements

Possible improvements:

- Interactive Power BI Dashboard
- Tableau Integration
- Customer Lifetime Value Prediction
- Machine Learning Based Segmentation
- K-Means Clustering
- Churn Prediction Model
- Real E-commerce Dataset Integration
- Automated Marketing Recommendations

---

# 👨‍💻 Author

**Jismon George**

Data Analyst | AI & Machine Learning Enthusiast

📍 Kottayam, Kerala, India

### Skills

- Python
- SQL
- Power BI
- Machine Learning
- Data Analytics
- Data Visualization

---

# ⭐ Repository Highlights

✅ End-to-End Customer Segmentation Project

✅ Business-Oriented Analytics

✅ Realistic RFM Framework

✅ Marketing Recommendation Engine

✅ Professional Dashboard Visualization

✅ Internship Project Showcase

---

## 📜 License

This project is intended for educational, portfolio, and internship demonstration purposes.

---

### ⭐ If you found this project useful, don't forget to Star the Repository!
