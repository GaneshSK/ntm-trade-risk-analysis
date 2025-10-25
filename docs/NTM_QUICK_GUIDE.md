# NTM DATA - QUICK COLLECTION GUIDE

---

## 🎯 SHORT ANSWER: What NTM Data Structure You Need

### **TWO Simple CSV Files:**

**File 1: `ntm_measures.csv`** (Detailed measures)
```csv
reporter_iso3,partner_iso3,hs_code,ntm_code,measure_description,start_date,year
USA,CHN,8517,A14,Telecom equipment authorization,2018-07-06,2018
USA,CHN,8517,B83,Certification requirement,2019-05-10,2019
USA,IND,0306,A31,Shrimp import authorization,2015-03-15,2015
```

**File 2: `ntm_quarterly.csv`** (Aggregated by quarter - for joining)
```csv
reporter_iso3,partner_iso3,hs_code,date,ntm_count,has_sps,has_tbt,severity_score
USA,CHN,8517,2018-Q3,5,1,1,HIGH
USA,CHN,8517,2019-Q1,6,1,1,HIGH
USA,IND,0306,2020-Q2,2,1,0,MEDIUM
```

---

## 📥 WHERE TO GET THE DATA

### **Option 1: TRAINS Online (Primary Source)**
**URL**: https://trainsonline.unctad.org/bulkDataDownload

**What to download:**
- **Countries**: USA (as reporter), China & India (as partners)
- **Products**: Your 12 HS4 codes (or HS6 equivalents)
- **Years**: 2018-2025
- **Format**: CSV

**Steps:**
1. Register (free)
2. Go to Bulk Data Download
3. Apply filters above
4. Download CSV

---

### **Option 2: WITS (Alternative/Validation)**
**URL**: https://wits.worldbank.org/

**Navigation:**
1. Login → NTM → View and Export Raw Data
2. Select: USA, products, years
3. Export CSV

---

## 📊 WHAT I NEED FROM YOU

**Just upload ONE of these:**

1. **Raw TRAINS download** (whatever format it comes in)
   - Could be 500-2,000 rows
   - Multiple columns (I'll parse)
   - CSV or Excel

2. **Raw WITS export** (their format)
   - Whatever columns they provide
   - I'll standardize

**I'll handle:**
- ✅ Parsing their format
- ✅ Filtering to your 12 products
- ✅ Converting HS6 → HS4
- ✅ Creating quarterly aggregation
- ✅ Joining with your trade data

---

## 🔑 KEY NTM CODES TO LOOK FOR

### **By Product Category:**

**Technology (8517, 8471, 8507, 8542):**
- `A14` - SPS authorization
- `B83` - Certification
- `B84` - Inspection
- `D1` - Anti-dumping
- `P13` - Export licensing

**Agriculture (0306, 1302, 1006):**
- `A31` - Hygiene requirements
- `A32` - Pest treatment
- `A85` - Traceability
- `P14` - Export ban

**Commodities (2504, 2710, 6302, 9503, 3924):**
- `B31` - Labeling
- `E1` - Import licensing
- `P13` - Export licensing

---

## ⚡ FAST TRACK: Minimum Data Needed

**If TRAINS/WITS is difficult**, provide me with:

### **At minimum, collect:**
For each HS code, just note:
- Any major US measures on China (2018-2025)
- Any major US measures on India (2018-2025)  
- Any export controls (China/India)

**Format can be simple Excel:**
```
Product | Country | Measure Type | Date | Description
8517    | China   | Anti-dumping | 2018-07 | Section 301 tariffs 25%
2504    | China   | Export ban   | 2023-10 | Graphite export licensing
```

I can formalize this into proper NTM schema.

---

## 🎓 FOR YOUR THESIS

**You need to show:**
1. NTM data collection methodology ✅
2. Data integration with trade flows ✅
3. NTM impact on risk scores ✅

**Bare minimum:** 
- 20-50 key NTM measures across your 12 products
- 2018-2025 timeframe
- Focus on US-China relationship (where most action is)

**This is sufficient** for proof-of-concept in 4-month thesis!

---

## 📋 DELIVERABLES (After You Upload)

I'll create:
1. ✅ `ntm_measures_clean.csv` (standardized)
2. ✅ `ntm_quarterly_aggregated.csv` (join-ready)
3. ✅ `trade_ntm_combined.csv` (merged dataset)
4. ✅ `prepare_ntm_data.py` (processing script)
5. ✅ NTM visualization (heat map of measures)

**Processing time: ~5 minutes**

---

## 🚀 IMMEDIATE NEXT STEP

**Choose ONE:**

**A)** "I'll download from TRAINS/WITS" 
   → Follow detailed guide in NTM_DATA_SCHEMA.md
   → Upload CSV when ready

**B)** "Need step-by-step help accessing TRAINS"
   → I'll provide screenshot instructions
   → Guide you through registration

**C)** "Can I use alternative sources?"
   → Yes! WTO I-TIP, USITC, Federal Register
   → I'll help structure whatever you find

**D)** "Start without NTM data for now"
   → OK! Your trade indices are already excellent
   → Add NTM data later when available

---

**Current Status: Trade data ✅ | NTM data ⏳ | Combined analysis ⏳**

Let me know which path you want to take! 🎯
