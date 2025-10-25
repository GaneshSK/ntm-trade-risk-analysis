# NTM Data Schema Specification
## For US-China-India Trade Analysis

---

## 📚 DATA SOURCES OVERVIEW

Based on your requirements, here are the two main sources:

### **Option 1: UNCTAD TRAINS Database (Recommended)**
- **URL**: https://trainsonline.unctad.org/
- **Access**: Requires free registration
- **Coverage**: 109+ countries, 65,000+ measures
- **Format**: CSV, Stata, Excel
- **Granularity**: HS 6-digit (can aggregate to HS4)
- **Classification**: International Classification of NTMs (177 types)

### **Option 2: WITS (World Bank)**
- **URL**: https://wits.worldbank.org/
- **Access**: Free, requires WITS login for bulk download
- **Coverage**: Same as TRAINS (uses TRAINS data)
- **Format**: CSV download via "NTM - View and Export Raw Data"
- **Granularity**: HS 6-digit

**Recommendation**: Use TRAINS Online for bulk download, cross-check with WITS.

---

## 🎯 IDEAL NTM DATA STRUCTURE FOR YOUR THESIS

### **File: `ntm_data_us_china_india.csv`**

I recommend **TWO tables** approach:

---

## 📋 TABLE 1: NTM MEASURES (Core Data)

### **Schema Structure:**

```csv
reporter_iso3,reporter_name,partner_iso3,partner_name,hs_code,ntm_code,ntm_chapter,ntm_type,measure_description,start_date,end_date,year,affected_product,legal_source,regulation_id,measure_status
USA,United States,CHN,China,8517,A14,A,SPS,Telecommunications equipment conformity assessment,2018-07-06,,2018,Telephone sets and cellular network equipment,Federal Register 83 FR 28710,FCC-18-133,Active
USA,United States,CHN,China,8517,B83,B,TBT,Certification and testing requirements for telecom,2019-05-10,,2019,Telecommunications equipment,47 CFR Part 2,FCC-19-39,Active
USA,United States,IND,India,0306,A31,A,SPS,Import authorization for shrimp,2015-03-15,,2015,Frozen shrimp,FDA Import Alert 16-131,FDA-2015-N-0001,Active
CHN,China,USA,United States,2504,P13,P,Export,Export licensing for graphite products,2023-10-01,,2023,Natural graphite,MOFCOM Announcement No. 53,MOFCOM-2023-53,Active
IND,India,WLD,World,1006,P14,P,Export,Rice export restrictions,2022-09-09,2023-08-31,2022,Non-basmati white rice,DGFT Notification 22/2022,DGFT-2022-22,Expired
```

### **Column Definitions:**

| Column | Type | Description | Example | Required |
|--------|------|-------------|---------|----------|
| `reporter_iso3` | string | Imposing country (ISO3) | `USA`, `CHN`, `IND` | ✅ |
| `reporter_name` | string | Imposing country name | `United States` | ✅ |
| `partner_iso3` | string | Affected partner (ISO3) | `CHN`, `IND`, `WLD` (world) | ✅ |
| `partner_name` | string | Affected partner name | `China`, `India`, `World` | ✅ |
| `hs_code` | string | HS 4-digit or 6-digit code | `8517`, `030613` | ✅ |
| `ntm_code` | string | NTM code (3-digit ICNTM) | `A14`, `B83`, `P13` | ✅ |
| `ntm_chapter` | string | NTM chapter (letter) | `A`, `B`, `C`, `P` | ✅ |
| `ntm_type` | string | NTM type description | `SPS`, `TBT`, `Export` | ✅ |
| `measure_description` | text | Description of the measure | Full text description | ✅ |
| `start_date` | date | Effective start date (YYYY-MM-DD) | `2018-07-06` | ✅ |
| `end_date` | date | Expiry date (if applicable) | `2023-08-31` or empty | optional |
| `year` | integer | Year measure imposed | `2018` | ✅ |
| `affected_product` | text | Product description | `Telephone sets...` | optional |
| `legal_source` | text | Source document | `Federal Register...` | optional |
| `regulation_id` | string | Official regulation ID | `FCC-18-133` | optional |
| `measure_status` | string | Active/Expired/Suspended | `Active` | ✅ |

---

## 📊 TABLE 2: NTM AGGREGATED METRICS (For Analysis)

### **Schema Structure:**

```csv
reporter_iso3,partner_iso3,hs_code,year_quarter,ntm_count,ntm_types,has_sps,has_tbt,has_export_restriction,has_tariff_quota,technical_measure_count,non_technical_count,newest_measure_date,severity_score
USA,CHN,8517,2018-Q3,5,A14;B83;B31;A11;D1,1,1,0,0,4,1,2018-07-06,HIGH
USA,CHN,8517,2019-Q1,6,A14;B83;B31;A11;D1;E1,1,1,0,0,4,2,2019-01-15,HIGH
USA,IND,0306,2020-Q2,2,A31;A32,1,0,0,0,2,0,2015-03-15,MEDIUM
CHN,USA,2504,2023-Q4,1,P13,0,0,1,0,0,1,2023-10-01,HIGH
IND,WLD,1006,2022-Q3,1,P14,0,0,1,0,0,1,2022-09-09,HIGH
```

### **Column Definitions:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `reporter_iso3` | string | Imposing country | `USA` |
| `partner_iso3` | string | Affected partner | `CHN`, `IND`, `WLD` |
| `hs_code` | string | HS 4-digit code | `8517` |
| `year_quarter` | string | Time period (YYYY-QN) | `2018-Q3` |
| `ntm_count` | integer | Total measures in force | `5` |
| `ntm_types` | string | Semicolon-separated NTM codes | `A14;B83;B31` |
| `has_sps` | boolean | 1 if SPS measure present | `1` or `0` |
| `has_tbt` | boolean | 1 if TBT measure present | `1` or `0` |
| `has_export_restriction` | boolean | 1 if export control | `1` or `0` |
| `has_tariff_quota` | boolean | 1 if tariff-rate quota | `1` or `0` |
| `technical_measure_count` | integer | Count of technical measures (A-C) | `4` |
| `non_technical_count` | integer | Count of non-technical (D-P) | `1` |
| `newest_measure_date` | date | Date of most recent measure | `2018-07-06` |
| `severity_score` | string | HIGH/MEDIUM/LOW | `HIGH` |

---

## 🔤 NTM CLASSIFICATION SYSTEM (ICNTM 2012)

### **Chapter Codes (Letter-based):**

| Chapter | Type | Description | Examples |
|---------|------|-------------|----------|
| **A** | Technical | Sanitary & Phytosanitary (SPS) | Food safety, animal health, plant health |
| **B** | Technical | Technical Barriers to Trade (TBT) | Product standards, testing, certification |
| **C** | Technical | Pre-shipment & other formalities | Inspection, formalities |
| **D** | Non-technical | Contingent trade protective | Anti-dumping, safeguards |
| **E** | Non-technical | Non-automatic licensing, quotas | Import licensing, quotas |
| **F** | Non-technical | Price control measures | Minimum prices, additional charges |
| **P** | Export | Export-related measures | Export licenses, export taxes |

### **Key 3-Digit Codes for Your Products:**

#### **Technology Products (HS 8517, 8471, 8507, 8542):**
- `A14` - Authorization for SPS reasons
- `B31` - Labeling requirements
- `B33` - Packaging requirements
- `B83` - Certification requirement
- `B84` - Inspection requirement
- `D1` - Anti-dumping measures
- `D2` - Countervailing duties
- `P13` - Export licensing

#### **Agricultural Products (HS 0306, 1302, 1006):**
- `A11` - Prohibitions for SPS reasons
- `A31` - Hygienic requirements
- `A32` - Treatment for elimination of pests
- `A33` - Authorized use of additives
- `A41` - Microbiological criteria
- `A42` - Hygienic practices during production
- `A85` - Traceability requirements
- `B31` - Labeling requirements
- `P14` - Export prohibition

#### **Minerals/Commodities (HS 2504, 2710, 6302, 9503, 3924):**
- `B14` - Authorization for TBT reasons
- `B31` - Labeling requirements
- `B84` - Inspection requirement
- `D1` - Anti-dumping measures
- `E1` - Non-automatic import licensing
- `P13` - Export licensing
- `P19` - Export prohibition

---

## 🎯 WHAT YOU NEED TO COLLECT

### **Priority Countries & Directions:**

1. **USA → China** (US measures affecting Chinese exports)
2. **USA → India** (US measures affecting Indian exports)
3. **China → World** (Chinese export restrictions, especially graphite)
4. **India → World** (Indian export restrictions, especially rice)

### **For Each of Your 12 HS Codes:**

| HS Code | Product | Key NTM Types to Track |
|---------|---------|------------------------|
| 0306 | Shrimp | A31, A32, A41, A85 (SPS/food safety) |
| 1006 | Rice | A11, A31, P14 (SPS + export restrictions) |
| 1302 | Herbal Extracts | A33, A85, B31 (additives, traceability, labeling) |
| 2504 | Graphite | P13, P19, B84 (export controls, inspection) |
| 2710 | Petroleum | E1, F1 (licensing, price controls) |
| 3924 | Kitchenware | A33, B31, B33 (additives, labeling, packaging) |
| 6302 | Bedlinen | B31, B84 (labeling, inspection) |
| 8471 | Computing | B83, B84, D1 (certification, anti-dumping) |
| 8507 | Batteries | A14, B33, B84, C1 (authorization, packaging, inspection) |
| 8517 | Telecom | A14, B83, B84, D1 (authorization, certification) |
| 8542 | Semiconductors | B83, B84, P13 (certification, export controls) |
| 9503 | Toys | A33, B31, B83 (safety standards, labeling, certification) |

### **Time Period:**
- **Focus**: 2018-2025 (matches your trade data)
- **Priority**: Quarterly aggregation (match to your YYYY-QN format)

---

## 📥 DATA COLLECTION WORKFLOW

### **Step 1: TRAINS Online Bulk Download**

1. Register at https://trainsonline.unctad.org/
2. Navigate to **Bulk Data Download** section
3. Filter by:
   - **Reporter**: USA, China, India
   - **HS Codes**: Your 12 products (use HS6 then aggregate to HS4)
   - **Years**: 2018-2025
   - **NTM Chapters**: A, B, C, D, E, P
4. Download as **CSV**

### **Step 2: WITS Cross-Check**

1. Go to https://wits.worldbank.org/
2. Login (free registration)
3. Navigate to **NTM → View and Export Raw Data**
4. Query by:
   - Country: USA
   - Partner: China, India
   - Product: Your HS4 codes
   - Year: 2018-2025
5. Export CSV for validation

### **Step 3: Manual Supplement (If Needed)**

For recent measures (2024-2025), manually check:
- **USA**: Federal Register (https://www.federalregister.gov/)
- **China**: MOFCOM announcements
- **India**: DGFT notifications

---

## 🔧 DATA PREPARATION SCRIPT (What I'll Build)

Once you provide the raw TRAINS/WITS download, I'll create:

```python
# Script: prepare_ntm_data.py
# Input: raw_trains_download.csv
# Output: 
#   1. ntm_measures.csv (detailed measures)
#   2. ntm_quarterly_aggregated.csv (for joining with trade data)
```

**The script will:**
1. Parse TRAINS/WITS format
2. Filter to your 12 HS codes
3. Aggregate HS6 → HS4
4. Create quarterly time series (2020-Q3 to 2025-Q2)
5. Compute NTM metrics (count, types, severity)
6. Join-ready format (hs_code + year_quarter)

---

## 📋 SAMPLE DATA TO PROVIDE

**Please download and share with me:**

### **Minimum Viable Dataset:**

```
From TRAINS Online or WITS:
- Reporter: USA, CHN, IND
- Partner: CHN, IND, WLD (World)
- HS Codes: 0306, 1006, 1302, 2504, 2710, 3924, 6302, 8471, 8507, 8517, 8542, 9503
- Years: 2018-2025
- Format: CSV
```

### **Expected File Size:**
- Detailed measures: ~500-2,000 rows (depends on granularity)
- After aggregation: ~240 rows (12 products × 20 quarters)

---

## 🎯 DELIVERABLES I'LL CREATE

Once you upload the raw NTM data:

### **1. Cleaned NTM Measures Table**
- Standardized columns
- HS6 → HS4 aggregation
- Date parsing and validation

### **2. Quarterly Aggregated Table**
- Joinable with `trade_data_with_indices.csv`
- Key: `hs_code` + `date` (quarter)
- NTM metrics ready for Gen AI

### **3. NTM Processing Script**
- `prepare_ntm_data.py`
- Reusable for updates
- Fully documented

### **4. Merged Dataset**
- `trade_ntm_combined.csv`
- All trade indices + NTM metrics
- 240 rows × 50+ columns
- Ready for Gen AI analysis

---

## 📊 EXPECTED MERGED OUTPUT COLUMNS

After joining trade + NTM data:

```
Base columns (10): date, hs_code, product_name, trade flows...
Trade indices (30): china_share_us, risk_score, RCA, HHI...
NTM metrics (10): ntm_count, has_sps, has_tbt, severity_score...
---
Total: ~50 columns, 240 rows
```

---

## ✅ WHAT TO DO NOW

### **Option A: If You Have Access (Recommended)**

1. **Register** at https://trainsonline.unctad.org/
2. **Download** NTM data using filters above
3. **Upload** the CSV file to me
4. I'll process and integrate with your trade data

### **Option B: If You Need Help**

Let me know and I can:
- Provide detailed screenshot instructions
- Create a query template for WITS
- Guide you through TRAINS bulk download
- Suggest alternative sources (WTO I-TIP, USITC)

---

## 🚦 READY STATUS

- ✅ Trade data processed (240 rows, 40 columns)
- ✅ Trade indices computed (HHI, RCA, risk scores)
- ⏳ **NTM data needed** (waiting for your download)
- ⏳ Join trade + NTM data
- ⏳ Ready for Gen AI analysis

---

## 📞 NEXT STEPS

**Tell me:**
1. Do you have access to TRAINS/WITS?
2. Can you download the CSV with filters specified above?
3. Or do you need detailed step-by-step instructions?

Once you upload the raw NTM CSV, I'll have your complete dataset ready in ~5 minutes! 🚀

