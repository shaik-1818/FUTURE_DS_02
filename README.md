# 📉 Customer Retention & Churn Analysis
### Future Interns — Data Science & Analytics | Task 2

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4c72b0)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel%20Reading-green)
![Status](https://img.shields.io/badge/Status-Completed✅-2dc653)

---

## 📌 Objective

Analyze customer data from a subscription-based Telco business to identify:
- Overall churn rate and retention trends
- Key churn drivers (contract type, tenure, charges, services)
- Cohort-based retention patterns across tenure groups
- Customer Lifetime Value (CLTV) differences between churned and retained
- Actionable recommendations to reduce customer loss

---

## 📁 Repository Structure

```
FUTURE_DS_02/
├── FUTURE_DS_02_FullCode.py     # Complete Python analysis script
├── FUTURE_DS_02_Report.pdf      # Client-ready analysis report with charts
├── Telco_Churn.xlsx             # Dataset used for analysis
└── README.md                    # Project documentation
```

---

## 📦 Dataset

| Property | Details |
|----------|---------|
| Name | Telco Customer Churn |
| Rows | 7,043 |
| Columns | 21 |
| Source | IBM Sample Dataset (Kaggle) |
| Features | Tenure, Contract, Internet Service, Monthly Charges, Total Charges, CLTV, Churn Label, Churn Reason, Payment Method, and more |

---

## 🛠️ Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core programming language |
| Pandas | Data loading, cleaning, aggregation |
| Matplotlib | Charts and visualizations |
| Seaborn | Heatmaps and violin plots |
| ReportLab | PDF report generation |
| OpenPyXL | Reading Excel (.xlsx) files |

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/FUTURE_DS_02.git
cd FUTURE_DS_02
```

**2. Install dependencies**
```bash
pip install pandas matplotlib seaborn reportlab openpyxl
```

**3. Run the analysis**
```bash
python FUTURE_DS_02_FullCode.py
```

**4. Outputs generated**
- 7 chart PNG files
- `FUTURE_DS_02_Report.pdf` — complete analysis report

---

## 📊 Analysis Sections

| # | Section | Description |
|---|---------|-------------|
| 1 | Data Loading & Cleaning | Load Excel, handle missing values, feature engineering |
| 2 | KPI Dashboard | Churn Rate, Retention Rate, Avg Tenure, Avg CLTV |
| 3 | Churn Overview | Overall donut + by Contract Type + by Internet Service |
| 4 | Tenure & Charges | Tenure distribution, tenure group rates, monthly charges boxplot |
| 5 | Churn Drivers | Churn rate by Gender, Senior Citizen, Partner, Dependents, Billing |
| 6 | Services Impact | Churn rate by Phone, Security, Backup, Device, Support, Streaming |
| 7 | Retention Cohort | Retention curve by tenure cohort (6 groups) |
| 8 | CLTV Analysis | Violin plot comparing CLTV: Churned vs Retained |
| 9 | Churn Reasons & Heatmap | Top 12 reasons + Contract × Internet heatmap |
| 10 | PDF Report | Auto-generated client-ready PDF report |

---

## 📈 Key Findings

| Metric | Value |
|--------|-------|
| Total Customers | 7,043 |
| Overall Churn Rate | 26.5% |
| Retention Rate | 73.5% |
| Avg Tenure — Churned | 17.9 months |
| Avg Tenure — Retained | 37.6 months |
| Avg CLTV — Churned | $2,556 |
| Avg CLTV — Retained | $4,051 |

### 🔑 Business Insights

- **1 in 4 customers** churn — a major recurring revenue risk
- **Month-to-month** contract holders have the highest churn rate by far
- Customers are most at risk in the **first 12 months** of subscription
- **Fiber Optic** users churn more than DSL despite paying premium prices
- Customers **without Online Security and Tech Support** churn significantly more
- **Electronic check** payment method strongly correlates with higher churn
- Retained customers have **58% higher CLTV** than churned customers

### ✅ Recommendations

1. Convert **Month-to-Month** customers to annual contracts with discounts/incentives
2. Launch a **First-Year Loyalty Program** targeting the 0–12 month high-risk cohort
3. Bundle **Online Security & Tech Support** free for new customers' first 3 months
4. Review **Fiber Optic pricing** — premium users are churning most
5. Incentivize **Auto-Pay enrollment** to reduce electronic check churn risk

---

## 📷 Visualizations Generated

| Chart | Description |
|-------|-------------|
| `t2_kpi.png` | 5-card KPI dashboard |
| `t2_churn_overview.png` | Donut + by Contract + by Internet Service |
| `t2_tenure_charges.png` | Tenure histogram + Tenure group rates + Boxplot |
| `t2_churn_drivers.png` | 6-panel demographics & billing churn rates |
| `t2_services_churn.png` | 6-panel services subscription churn rates |
| `t2_cohort_cltv.png` | Retention cohort curve + CLTV violin plot |
| `t2_reasons_heatmap.png` | Top 12 churn reasons + risk heatmap |

---

## 🏢 About This Internship

This project was completed as part of the **Future Interns Data Science & Analytics** program.

- 🌐 Website: [futureinterns.com](https://futureinterns.com)
- 💼 LinkedIn: [Future Interns](https://www.linkedin.com/company/future-interns/)
- 📧 Contact: contact@futureinterns.com

---

## 👤 Author

**[Your Name]**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)

---

*Completed as Task 2 of the Future Interns Data Science & Analytics Internship*
*Track Code: **FUTURE_DS_02***
