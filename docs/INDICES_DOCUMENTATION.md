# Trade Data Indices & Ratios - Documentation
## Computed from master_data_us_china_india.csv

---

## 📊 OUTPUT FILE

**File**: `trade_data_with_indices.csv`
**Rows**: 240 (12 products × 20 quarters)
**Columns**: 40 computed metrics

---

## 📋 COLUMN DEFINITIONS

### **Base Columns (from original data)**
| Column | Type | Description |
|--------|------|-------------|
| `date` | string | Quarter (YYYY-QN) |
| `quarter_num` | integer | Numeric quarter for sorting (e.g., 20203) |
| `year` | string | Year extracted from date |
| `hs_code` | string | HS 4-digit code |
| `product_name` | string | Product description |
| `us_import_china` | integer | US imports from China (USD thousands) |
| `us_import_india` | integer | US imports from India (USD thousands) |
| `us_import_world` | integer | Total US imports (USD thousands) |
| `china_export_world` | integer | China's total exports (USD thousands) |
| `india_export_world` | integer | India's total exports (USD thousands) |

---

### **Market Share Metrics (5 columns)**

| Column | Formula | Interpretation |
|--------|---------|----------------|
| `china_share_us` | (us_import_china / us_import_world) × 100 | China's % of US market |
| `india_share_us` | (us_import_india / us_import_world) × 100 | India's % of US market |
| `other_share_us` | 100 - china_share - india_share | Rest of world's % of US market |
| `us_share_china_exports` | (us_import_china / china_export_world) × 100 | US importance to China (% of China exports going to US) |
| `us_share_india_exports` | (us_import_india / india_export_world) × 100 | US importance to India (% of India exports going to US) |

**Key Insights:**
- High `china_share_us` (>50%) = High dependency on China
- High `us_share_china_exports` (>30%) = US is critical market for China
- Useful for identifying bilateral dependencies

---

### **Concentration Indices (3 columns)**

| Column | Formula | Interpretation |
|--------|---------|----------------|
| `hhi_us_imports` | Σ(market_share²) | Hirschman-Herfindahl Index (0-1) |
| `concentration_level` | Based on HHI | HIGH (>0.25), MODERATE (0.15-0.25), LOW (<0.15) |
| `diversification_score` | 1 - HHI | Higher = more diversified supply |

**HHI Interpretation:**
- **HHI > 0.25**: Highly concentrated market (monopoly/duopoly)
- **HHI 0.15-0.25**: Moderately concentrated
- **HHI < 0.15**: Competitive market

**Example**: HS 3924 (Plastic Kitchenware) has HHI ~0.62 → Highly concentrated (China dominates)

---

### **Trade Intensity Indices (2 columns)**

| Column | Formula | Interpretation |
|--------|---------|----------------|
| `trade_intensity_china` | (bilateral_share) / (partner_global_share) | >1 = stronger trade relationship than expected |
| `trade_intensity_india` | Same for India | >1 = stronger trade relationship than expected |

**Interpretation:**
- **TI > 1**: Trade relationship stronger than global average
- **TI < 1**: Trade relationship weaker than expected
- **TI >> 1**: Special trade relationship (FTA, proximity, etc.)

---

### **Growth Rates (5 columns)** - All Quarter-over-Quarter %

| Column | Description |
|--------|-------------|
| `us_import_china_growth` | % change in US imports from China |
| `us_import_india_growth` | % change in US imports from India |
| `us_import_world_growth` | % change in total US imports |
| `china_export_world_growth` | % change in China's global exports |
| `india_export_world_growth` | % change in India's global exports |

**Usage:**
- Positive growth = expanding trade
- Negative growth = contracting trade
- Compare China vs India growth to identify diversification trends

---

### **Trend Indicators (6 columns)**

| Column | Description |
|--------|-------------|
| `china_share_ma4` | 4-quarter moving average of China's market share |
| `india_share_ma4` | 4-quarter moving average of India's market share |
| `china_trend` | INCREASING / DECREASING / STABLE (vs MA) |
| `india_trend` | INCREASING / DECREASING / STABLE (vs MA) |
| `china_momentum` | Quarter-over-quarter change in China share |
| `india_momentum` | Quarter-over-quarter change in India share |

**Usage:**
- Smooths out quarterly volatility
- Identifies sustained trends vs temporary fluctuations
- Momentum shows acceleration/deceleration

---

### **Revealed Comparative Advantage - RCA (3 columns)**

| Column | Formula | Interpretation |
|--------|---------|----------------|
| `china_rca` | (Product % of country exports) / (Product % of world trade) | RCA > 1 = comparative advantage |
| `india_rca` | Same for India | RCA > 1 = comparative advantage |
| `rca_advantage` | CHINA / INDIA / NEUTRAL | Which country has stronger advantage |

**RCA Interpretation:**
- **RCA > 1**: Country has comparative advantage (specializes in this product)
- **RCA < 1**: Country lacks comparative advantage
- **RCA > 2**: Strong comparative advantage

**Example**: 
- India RCA for HS 0306 (Shrimp) = 3.29 → Strong advantage
- China RCA for HS 3924 (Kitchenware) = 1.8 → Moderate advantage

---

### **Risk & Dependency Metrics (5 columns)**

| Column | Formula/Logic | Interpretation |
|--------|---------------|----------------|
| `china_dependency_risk` | Same as china_share_us | 0-100 scale, higher = more dependent |
| `geopolitical_risk_score` | 0.5×china_share + 0.3×HHI×100 + 0.2×trade_intensity | 0-100 composite risk score |
| `risk_level` | Based on geo_risk_score | HIGH (≥70), MEDIUM (40-70), LOW (<40) |
| `india_opportunity_score` | 0.4×(100-india_share) + india_rca×10 + 0.4×china_share | 0-100, higher = better opportunity |
| `china_india_ratio` | us_import_china / us_import_india | How many times more imports from China vs India |

**Geopolitical Risk Score Components:**
1. **China Market Share (50% weight)**: Direct dependency
2. **HHI Concentration (30% weight)**: Lack of alternatives
3. **Trade Intensity (20% weight)**: Structural relationship strength

**Risk Level Classification:**
- **HIGH (≥70)**: Critical dependency, urgent diversification needed
- **MEDIUM (40-70)**: Moderate risk, monitor and plan alternatives
- **LOW (<40)**: Well-diversified or low China exposure

**India Opportunity Score:**
- High score = Good diversification opportunity (low current India share + India has advantage + China dominant)
- Low score = Less attractive opportunity (India already strong OR lacks competitive advantage)

---

### **Diversification Metrics (1 column)**

| Column | Formula | Interpretation |
|--------|---------|----------------|
| `china_india_ratio` | us_import_china / us_import_india | How much more from China vs India |

**Example:**
- Ratio = 100 → Imports 100× more from China than India
- Ratio = 0.1 → Imports 10× more from India than China

---

### **Metadata (1 column)**

| Column | Description |
|--------|-------------|
| `analysis_timestamp` | When analysis was run |

---

## 📊 KEY FINDINGS FROM YOUR DATA

### **Overall Trade Pattern:**
- **Average China Share**: 34.10% (China is major supplier)
- **Average India Share**: 10.65% (Growing but still smaller)
- **Average HHI**: 0.5968 (Highly concentrated markets overall)

### **Risk Distribution:**
- **HIGH Risk**: 49 observations (20.4%) - Products like HS 3924, 9503, 2504
- **MEDIUM Risk**: 127 observations (52.9%) - Products like HS 8517, 8471, 6302
- **LOW Risk**: 64 observations (26.7%) - Products like HS 0306, 1006, 1302

### **Comparative Advantage:**
- **China leads**: 108/240 observations (45%)
- **India leads**: 99/240 observations (41%)
- **Balanced competition** across portfolio

---

## 🎯 PRODUCT HIGHLIGHTS

### **HIGH RISK PRODUCTS** (Geopolitical Risk Score ≥ 70)

1. **HS 3924 - Plastic Kitchenware**
   - China Share: 78.58% | Risk Score: 79.13
   - High concentration, China dominant
   - India Share: 0.62% (huge opportunity gap)

2. **HS 9503 - Toys**
   - China Share: 77.58% | Risk Score: 78.43
   - Classic China+1 candidate
   - India gaining slowly (0.59%)

3. **HS 2504 - Natural Graphite**
   - China Share: 60.23% | Risk Score: 67.08
   - Critical mineral, national security concern
   - India almost absent (0.04%)

### **INDIA SUCCESS STORIES** (India Share > 25%)

1. **HS 0306 - Shrimp/Crustaceans**
   - India Share: 26.28% | China Share: 0.19%
   - India RCA: 3.29 (strong advantage)
   - Clear winner for India

2. **HS 1302 - Herbal Extracts**
   - India Share: 28.73% | China Share: 19.31%
   - India ahead, leveraging ayurvedic tradition
   - Balanced RCA (both countries have advantage)

3. **HS 6302 - Bedlinen**
   - India Share: 35.15% | China Share: 33.92%
   - Neck-and-neck competition
   - India overtaking China (successful diversification)

### **MEDIUM RISK - MONITORING NEEDED**

1. **HS 8517 - Telecom Equipment**
   - China Share: 47.24% | India Share: 5.17%
   - Risk Score: 57.74 (Medium)
   - Tech competition, Section 301 tariffs

2. **HS 8507 - Electric Batteries**
   - China Share: 45.31% | India Share: 0.17%
   - Risk Score: 58.37 (Medium)
   - IRA opportunity for India

3. **HS 8471 - Computing Machines**
   - China Share: 38.92% | India Share: 0.03%
   - Risk Score: 55.72 (Medium)
   - Data center / cloud infrastructure

---

## 🚀 USAGE FOR GEN AI & ANALYSIS

### **For Risk Assessment Prompts:**
```python
"Analyze HS {hs_code} with China share of {china_share_us}%, 
HHI of {hhi_us_imports}, and geopolitical risk score of {geopolitical_risk_score}. 
Trend is {china_trend}. Provide risk assessment and recommendations."
```

### **For Diversification Recommendations:**
```python
"Product HS {hs_code} has India opportunity score of {india_opportunity_score}. 
India's RCA is {india_rca} while China's is {china_rca}. 
India share trending {india_trend}. Generate diversification strategy."
```

### **For Trend Analysis:**
```python
"HS {hs_code} shows China momentum of {china_momentum}% and 
India momentum of {india_momentum}%. Moving averages indicate 
China {china_trend} and India {india_trend}. Analyze implications."
```

---

## 📈 VISUALIZATION IDEAS

### **Heat Maps:**
- Risk Score by Product × Time
- China Share by Product × Time
- India Opportunity Score by Product × Time

### **Time Series:**
- Market share trends (China vs India)
- Growth rate comparisons
- Momentum indicators

### **Scatter Plots:**
- Risk Score vs Trade Value
- India RCA vs India Opportunity Score
- HHI vs Diversification Score

### **Bar Charts:**
- Risk level distribution by product
- Average market shares by product
- RCA advantage comparison

---

## 🔧 PYTHON USAGE EXAMPLES

### **Load and Filter:**
```python
import pandas as pd

df = pd.read_csv('trade_data_with_indices.csv')

# Get high-risk products in latest quarter
high_risk = df[(df['risk_level'] == 'HIGH') & (df['date'] == '2025-Q2')]

# Products where India is gaining momentum
india_rising = df[df['india_momentum'] > 2]

# Products with strong India comparative advantage
india_advantage = df[(df['india_rca'] > 1.5) & (df['rca_advantage'] == 'INDIA')]
```

### **Time Series Analysis:**
```python
# Plot China share trend for specific product
product = df[df['hs_code'] == '8517']
product.plot(x='date', y=['china_share_us', 'china_share_ma4'])
```

### **Risk Aggregation:**
```python
# Average risk by product
risk_by_product = df.groupby('hs_code')['geopolitical_risk_score'].mean()
```

---

## ✅ READY FOR:

1. ✅ Gen AI Agent Ingestion (structured data with context)
2. ✅ Statistical Analysis (growth rates, correlations, regressions)
3. ✅ Visualization (heat maps, dashboards, charts)
4. ✅ Risk Assessment (pre-computed scores and levels)
5. ✅ Retrospective Validation (trend indicators, momentum)
6. ✅ Policy Simulation (what-if scenarios with base metrics)

---

## 📚 NEXT STEPS

1. **Use this data for Gen AI prompts** → Feed indices as context
2. **Create visualizations** → Risk heat maps, trend charts
3. **Build dashboard** → Streamlit/Plotly interactive explorer
4. **Retrospective analysis** → Compare pre/post tariff patterns
5. **NTM integration** → Join with NTM data by hs_code + date

---

**File Locations:**
- 📊 Enriched Data: `/mnt/user-data/outputs/trade_data_with_indices.csv`
- 🐍 Python Script: `/mnt/user-data/outputs/compute_trade_indices.py`
- 📖 This Guide: Auto-generated documentation

**All 40 metrics computed and ready for analysis!** 🎉
