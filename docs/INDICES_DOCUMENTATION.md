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
