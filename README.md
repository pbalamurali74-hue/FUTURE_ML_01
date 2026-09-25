# 📈 Superstore Sales Forecasting & Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Machine Learning](https://img.shields.io/badge/ML-Time--Series%20Forecasting-FF6F00?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

An end-to-end data analytics and predictive modeling project developed as **Task 1** during the **Future Interns Machine Learning Internship**. This system combines exploratory data analysis, time-series forecasting, and an interactive executive **Power BI** dashboard to predict retail sales trends and optimize inventory planning.

---

## 🔍 Business Context & Problem Statement

Retail supply chains face critical challenges with inventory management:
- **Overstocking** ties up working capital and increases warehouse depreciation.
- **Stockouts** cause direct revenue loss and customer dissatisfaction.

Using historical transactional records from the **Sample Superstore** dataset, this project models underlying seasonal trends, consumer buying patterns, and regional demand to deliver accurate 12-month sales forecasts for executive decision-makers.

---

## ✨ Key Features & Workflow

1. **Exploratory Data Analysis (EDA):**
   - Cleaned and normalized 9,000+ transaction rows (`Sample - Superstore.csv`).
   - Analyzed category sales distribution (Furniture, Office Supplies, Technology) across Central, East, South, and West regions.
   - Identified recurring seasonal sales surges in Q4 (holiday shopping peaks).

2. **Time-Series Forecasting Model (`forecasting_model.ipynb`):**
   - Transformed raw order dates into uniform monthly time-series frequencies.
   - Trained time-series forecasting models to project future 12-month sales volume.
   - Generated evaluation metrics and exported forecasted points (`forecast_data.csv`).

3. **Interactive Power BI Executive Dashboard (`Sales_Dashboard.pbix`):**
   - Real-time slicers for **Region**, **Category**, and **Year**.
   - Comparative KPIs tracking **Actual Sales vs. Forecasted Sales**.
   - Visual trend line showing monthly historical and projected trajectory.

---

## 📊 Dashboard Visualizations

The Power BI dashboard provides multi-dimensional intelligence:

| View | Metric Tracked | Key Strategic Insight |
| :--- | :--- | :--- |
| **Regional Performance** | Sales by State & Territory | Highlights high-density revenue states (e.g., California, New York) |
| **Category Breakdown** | Technology vs. Furniture vs. Office | Technology delivers highest profit margin despite lower unit volumes |
| **Trend Forecaster** | Monthly Projected Revenue | Visualizes expected Q3-Q4 demand surges for proactive inventory stocking |

*(Dashboard screenshots and layout files are included in the repository folder).*

---

## 📁 Repository Structure

```
FUTURE_ML_01/
├── FUTURE_ML_01-main/
│   ├── forecasting_model.ipynb     # Jupyter Notebook: Data cleaning, EDA & time-series modeling
│   ├── Sales_Dashboard.pbix        # Interactive Power BI visual intelligence dashboard
│   ├── Sample - Superstore.csv     # Raw multi-year retail transactions dataset
│   ├── cleaned_data.csv            # Preprocessed and normalized data
│   ├── forecast_data.csv           # Model output containing 12-month projections
│   ├── Screenshot 2025-12-17 152353.png  # Dashboard preview 1
│   ├── Screenshot 2025-12-17 152400.png  # Dashboard preview 2
│   └── README.md
└── README.md                       # Comprehensive project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- Jupyter Notebook / VS Code
- Microsoft Power BI Desktop (to explore `.pbix`)

### 2. Setup Environment
```bash
git clone https://github.com/pbalamurali74-hue/FUTURE_ML_01.git
cd FUTURE_ML_01/FUTURE_ML_01-main
pip install pandas numpy matplotlib seaborn prophet
```

### 3. Run the Notebook
Launch Jupyter to inspect the time-series model:
```bash
jupyter notebook forecasting_model.ipynb
```

### 4. Open Power BI Dashboard
Double-click `Sales_Dashboard.pbix` in Power BI Desktop to interact with the executive analytics visuals.

---

## 👤 Author

**Purushotham Balamurali**  
- **Role:** Machine Learning Intern @ Future Interns  
- **GitHub:** [@pbalamurali74-hue](https://github.com/pbalamurali74-hue)  
- **LinkedIn:** [purushothambalamurali](https://www.linkedin.com/in/purushothambalamurali/)  
- **Portfolio:** [Purushotham Balamurali Portfolio](https://github.com/pbalamurali74-hue)
