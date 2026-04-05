# Data Wrangling Documentation

**BSAD 482 Term Project — Milestone 2**
**Decision:** Should a first-time homebuyer in HRM buy a home in 2026 or wait approximately 18 months?

---

## Overview

Three datasets were assembled and cleaned for this analysis. Wrangling was performed in Python using `pandas`. All code is available in `/src/eda.py`.

---

## Dataset 1: Interest Rate Data (`interest_rates.csv`)

**Source:** Bank of Canada (policy rate) and chartered bank posted mortgage rates

### Issues Encountered

| Issue | Resolution |
|-------|-----------|
| BoC API returns daily observations with BOM/EOM irregularities | Resampled to monthly frequency using the first observation of each month |
| Posted 5-year mortgage rate is not directly available as a clean FRED series | Reconstructed from Bank of Canada chartered bank rates table (weekly reported, converted to monthly) |
| Some months in 2020 showed duplicate entries during COVID emergency rate cut | Kept the lower (cut) rate for the month since it reflects the prevailing conditions for buyers |
| Date column included time zone metadata in ISO format | Stripped to `YYYY-MM-DD` string for consistency with other datasets |

### Assumptions

- Monthly rate is defined as the rate in effect on the first calendar day of that month.
- Posted 5-year rate reflects the chartered bank standard posted rate, not the discounted rate. This is the rate used in mortgage stress testing, making it the relevant affordability measure.

---

## Dataset 2: Halifax Housing Market Data (`halifax_housing_market.csv`)

**Source:** Nova Scotia Association of REALTORS® (NSAR) monthly statistics; CMHC Housing Market Outlook

### Issues Encountered

| Issue | Resolution |
|-------|-----------|
| NSAR reports are published as PDF press releases rather than downloadable CSV | Key metrics (average sale price, units sold, new listings, months of inventory, days on market) were extracted and compiled into a structured CSV |
| Pre-2020 data is less granular in public NSAR archives | Annual averages from CMHC historical reports were used to interpolate monthly patterns consistent with seasonal norms in the Atlantic Canada housing market |
| COVID lockdown months (March–May 2020) show extreme suppression in sales volume that is not representative of market fundamentals | These observations are retained but flagged in analysis as a structural break period; no imputation was applied |
| "Average sale price" includes all residential property types (single-family, condo, semi-detached), creating some compositional noise | Noted as a limitation; data is reported as published by NSAR and CMHC without further disaggregation |

### Assumptions

- Months of inventory is calculated as (active listings at month end) / (average monthly sales over trailing 3 months), consistent with CREA methodology.
- The COVID period (March–June 2020) is treated as a structural break and is annotated in relevant visualizations.

---

## Dataset 3: HRM Affordability and Demographic Data (`hrm_affordability.csv`)

**Source:** Statistics Canada Census; CMHC Rental Market Report; Nova Scotia Finance and Treasury Board

### Issues Encountered

| Issue | Resolution |
|-------|-----------|
| StatCan census income data is only available every 5 years (2016, 2021) | Median household income interpolated linearly between census years, with 2.5% annual growth assumption consistent with Nova Scotia wage growth data from Labour Force Survey reports |
| CMHC Rental Market Report publishes vacancy rates and average rents for Halifax CMA annually (fall survey) | Annual figures used directly; no monthly interpolation applied since affordability analysis is annual |
| Housing starts data from CMHC includes multiple dwelling types at different geographic levels | HRM-level starts were extracted from CMHC Housing Now (Halifax CMA) publication; includes single-detached, semi-detached, row, and apartment starts |
| Affordability ratio required calculation from raw inputs | Monthly mortgage payment calculated using standard formula: `P × r(1+r)^n / ((1+r)^n − 1)` where P = 90% of average sale price (10% down), r = monthly posted 5-year rate, n = 300 months (25-year amortization). Expressed as a percentage of estimated monthly median household income |

### Assumptions

- 10% down payment used for affordability calculation, consistent with the minimum for homes above $500k under CMHC stress test rules.
- 25-year amortization used throughout for comparability.
- Monthly median household income derived from annual census estimates divided by 12.

---

## Joining Datasets

For monthly trend analysis (Visualizations 1 and 2), `interest_rates.csv` and `halifax_housing_market.csv` were joined on the `date` column (left join on market data). No rows were lost.

For scatter and correlation analysis (Visualization 3), all three datasets were aggregated to annual frequency and joined on `year`. The resulting analytical frame has 11 observations (2015–2025).

---

## Final Data Quality Summary

| Dataset | Rows | Missing Values | Notes |
|---------|------|----------------|-------|
| `interest_rates.csv` | 135 | 0 | Complete 2015–2026 |
| `halifax_housing_market.csv` | 132 | 0 | Complete 2015–2025 |
| `hrm_affordability.csv` | 11 | 0 | Annual 2015–2025 |
