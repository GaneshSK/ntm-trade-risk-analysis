# 🌐 Agentic AI-Driven Framework for Global Trade Risk Management

> **Research Project**: Proactive trade risk management and strategic diversification using Generative AI and trade data analysis.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-UNCTAD%20|%20UN%20Comtrade-orange.svg)](https://trainsonline.unctad.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Key Metrics](#key-metrics)
- [Results](#results)
- [License](#license)
- [Citation](#citation)
- [Contact](#contact)

---

## 🎯 Overview

This repository contains the data processing pipeline and analysis framework for researching **proactive global trade risk management** using Agentic AI. The project analyzes **US-China-India bilateral trade** across 12 strategic product categories, integrating:

- **Trade flow data** (UN Comtrade)
- **Non-Tariff Measures (NTMs)** (UNCTAD TRAINS)
- **Trade indicators** (HHI, RCA, Trade Intensity)
- **Risk scoring** (geopolitical, dependency, diversification)

### **Research Goals:**

1. Develop automated trade risk assessment using Gen AI
2. Identify strategic diversification opportunities
3. Provide proactive alerts for emerging trade risks
4. Validate approach through retrospective case studies

---

## ✨ Features

### **Data Processing:**
- ✅ Automated ETL pipeline for trade data
- ✅ NTM classification and aggregation
- ✅ 32 computed trade indicators (HHI, RCA, growth rates, etc.)
- ✅ Quarterly time series (2020-Q3 to 2025-Q2)

### **Trade Indicators:**
- 📊 Market share analysis (China, India, Others)
- 📈 Concentration indices (HHI, diversification score)
- 💹 Growth rates and momentum indicators
- 🌐 Revealed Comparative Advantage (RCA)
- ⚖️ Trade intensity indices
- ⚠️ Risk scores (geopolitical, dependency)

### **NTM Integration:**
- 🏷️ 310+ measures from UNCTAD TRAINS
- 📋 Classification: SPS, TBT, Export controls, etc.
- 📊 Severity scoring (HIGH/MEDIUM/LOW)
- 🔗 Mapped to HS4 product codes

---

## 📊 Dataset

### **Coverage:**

| Dimension | Details |
|-----------|---------|
| **Products** | 12 HS4 codes across technology, agriculture, commodities |
| **Time Period** | 2020-Q3 to 2025-Q2 (20 quarters) |
| **Countries** | USA, China, India |
| **Observations** | 240 product-quarter combinations |
| **Features** | 48 columns (40 trade + 8 NTM metrics) |

### **Product Categories:**

#### **Technology:**
- HS 8517 - Telecom equipment
- HS 8471 - Computing machines
- HS 8507 - Batteries
- HS 8542 - Semiconductors

#### **Agriculture:**
- HS 0306 - Shrimp/Crustaceans
- HS 1006 - Rice
- HS 1302 - Herbal extracts

#### **Commodities:**
- HS 2504 - Natural graphite
- HS 2710 - Petroleum products
- HS 3924 - Plastic kitchenware
- HS 6302 - Bedlinen
- HS 9503 - Toys

### **Data Sources:**

- **Trade Flows**: UN Comtrade via WITS
- **NTM Measures**: UNCTAD TRAINS Database
- **Trade Indicators**: WITS analytical tools

---

## 📁 Repository Structure

```
trade-risk-analysis/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── data/                             # Raw input data
│   ├── master_data_us_china_india.csv       # Trade flows (240 rows)
│   └── NTM_details_-_data.csv               # NTM measures (310 measures)
│
├── scripts/                          # Python processing scripts
│   └── compute_trade_indices.py             # Main data processing
│
├── outputs/                          # Processed datasets
│   ├── trade_data_with_indices.csv          # Trade + indicators (40 cols)
│   ├── ntm_quarterly_aggregated.csv         # NTM aggregated (10 cols)
│   └── trade_ntm_combined.csv               # FINAL DATASET (48 cols)
│
├── docs/                             # Documentation
│   ├── INDICES_DOCUMENTATION.md             # Complete column reference
│   ├── QUICK_SUMMARY.md                     # Quick start guide
│   ├── NTM_DATA_SCHEMA.md                   # NTM data specification
│   ├── NTM_QUICK_GUIDE.md                   # NTM collection guide
│   └── COMPLETE_DATASET_SUMMARY.md          # Final dataset overview
│
└── notebooks/                        # Jupyter notebooks (future)
    └── exploratory_analysis.ipynb           # Data exploration
```

---

## 🚀 Getting Started

### **Prerequisites:**

```bash
Python 3.8+
pandas
numpy
openpyxl (for Excel files)
```

### **Installation:**

```bash
# Clone the repository
git clone https://github.com/yourusername/trade-risk-analysis.git
cd trade-risk-analysis

# Install dependencies
pip install -r requirements.txt
```

### **Quick Start:**

```python
import pandas as pd

# Load the complete dataset
df = pd.read_csv('outputs/trade_ntm_combined.csv')

# View summary
print(f"Dataset shape: {df.shape}")
print(f"Products: {df['hs_code'].nunique()}")
print(f"Time periods: {df['date'].nunique()}")

# Check a specific product
telecom = df[df['hs_code'] == '8517']
print(f"\nHS 8517 (Telecom):")
print(f"  Avg China share: {telecom['china_share_us'].mean():.1f}%")
print(f"  Avg NTMs: {telecom['ntm_count'].mean():.0f}")
print(f"  Risk level: {telecom['risk_level'].mode()[0]}")
```

---

## 💻 Usage

### **1. Reprocess Data (if needed):**

```bash
cd scripts
python compute_trade_indices.py
```

This will:
- Load raw trade data
- Compute 32 trade indicators
- Integrate NTM measures
- Generate `trade_ntm_combined.csv`

### **2. Data Analysis Examples:**

#### **Find High-Risk Products:**

```python
df = pd.read_csv('outputs/trade_ntm_combined.csv')

# High geopolitical risk + high China dependency
high_risk = df[
    (df['geopolitical_risk_score'] >= 70) & 
    (df['china_share_us'] > 50)
]

print("High-risk products:")
print(high_risk[['hs_code', 'product_name', 'china_share_us', 
                  'geopolitical_risk_score', 'ntm_count']].drop_duplicates('hs_code'))
```

#### **Identify Diversification Opportunities:**

```python
# High India opportunity + India has comparative advantage
opportunities = df[
    (df['india_opportunity_score'] > 60) & 
    (df['india_rca'] > 1)
]

print("Diversification opportunities:")
print(opportunities[['hs_code', 'india_opportunity_score', 
                     'india_rca', 'india_share_us']].drop_duplicates('hs_code'))
```

#### **Track NTM Changes Over Time:**

```python
# NTM growth by product
ntm_trends = df.groupby('hs_code').agg({
    'ntm_count': ['min', 'max', 'mean'],
    'ntm_severity': lambda x: x.mode()[0]
})

print("NTM trends:")
print(ntm_trends)
```

---

## 📈 Key Metrics

### **Trade Indicators (32 computed):**

| Category | Metrics | Description |
|----------|---------|-------------|
| **Market Share** | china_share_us, india_share_us, other_share_us | % of US market by supplier |
| **Concentration** | hhi_us_imports, diversification_score | Market concentration (0-1) |
| **Comparative Advantage** | china_rca, india_rca | Revealed comparative advantage |
| **Trade Intensity** | trade_intensity_china, trade_intensity_india | Bilateral relationship strength |
| **Growth** | *_growth (5 metrics) | Quarter-over-quarter % change |
| **Trends** | *_ma4, *_momentum (6 metrics) | Moving averages, direction |
| **Risk** | geopolitical_risk_score, china_dependency_risk | 0-100 composite scores |
| **Opportunity** | india_opportunity_score | Diversification potential |

### **NTM Metrics (8 computed):**

| Metric | Type | Description |
|--------|------|-------------|
| ntm_count | integer | Total active measures |
| ntm_codes | string | Semicolon-separated codes |
| has_sps | boolean | SPS measures present |
| has_tbt | boolean | TBT measures present |
| has_export_restriction | boolean | Export controls present |
| technical_measure_count | integer | Technical (A-C) measures |
| non_technical_count | integer | Non-technical (D-P) measures |
| ntm_severity | category | HIGH/MEDIUM/LOW/NONE |

---

## 📊 Results

### **Key Findings:**

#### **High-Risk Products (Urgent Diversification Needed):**

1. **HS 3924 (Plastic Kitchenware)**
   - China share: 78.6%
   - Risk score: 79.1 (HIGH)
   - NTMs: 11 avg
   - India share: 0.6% (opportunity gap)

2. **HS 9503 (Toys)**
   - China share: 77.6%
   - Risk score: 78.4 (HIGH)
   - NTMs: 37 avg (HIGH severity)

3. **HS 2504 (Natural Graphite)**
   - China share: 60.2%
   - Risk score: 67.1 (HIGH)
   - Critical mineral, national security concern

#### **India Success Stories (Diversification Working):**

1. **HS 0306 (Shrimp)**
   - India share: 26.3%
   - China share: 0.2%
   - India RCA: 3.29 (strong advantage)
   - Risk: LOW (38.4)

2. **HS 6302 (Bedlinen)**
   - India share: 35.2%
   - China share: 33.9%
   - India overtaking China successfully

3. **HS 1302 (Herbal Extracts)**
   - India share: 28.7%
   - China share: 19.3%
   - Leveraging ayurvedic tradition

#### **NTM Impact:**

- **High NTM products**: Petroleum (83), Toys (37), Telecom (21)
- **240 technical measures** (SPS, TBT)
- **31 non-technical measures** (export controls, licensing)
- Correlation: Higher NTMs → Higher compliance costs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📚 Citation

If you use this dataset or methodology in your research, please cite:

```bibtex
@misc{ganesh2025tradentrisk,
  title={Agentic AI-Driven Framework for Proactive Global Trade Risk Management},
  author={Ganesh S K},
  year={2025},
  howpublished={\url{https://github.com/yourusername/trade-risk-analysis}},
  note={Research proposal for Master's thesis}
}
```

---

## 👤 Contact

**Ganesh S K**
- GitHub: [@GaneshSK](https://github.com/GaneshSK)
- Email: s.k.ganesh91@gmail.com.com
- LinkedIn: [Ganesh S K](https://linkedin.com/in/ganesh-s-k)

---

## 🙏 Acknowledgments

- **UNCTAD** for TRAINS NTM database
- **UN Comtrade** for trade flow data
- **World Bank WITS** for trade indicators
- Research inspired by current geopolitical trade tensions and supply chain resilience needs

---
**Last Updated**: Nov 03, 2025

---

<div align="center">
  <b>⭐ Star this repo if you find it helpful!</b>
</div>
