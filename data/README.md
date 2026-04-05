# Data Directory

**BSAD 482 Term Project — Milestone 2**

This folder contains all datasets used in the Halifax First-Time Homebuyer Decision analysis.

---

## Dataset Inventory

### 1. `interest_rates.csv`
| Field | Value |
|-------|-------|
| **Description** | Monthly Bank of Canada overnight policy rate and chartered bank 5-year posted mortgage rate |
| **Coverage** | January 2015 – March 2026 |
| **Source** | Bank of Canada — Monetary Policy / Chartered Bank Mortgage Rates |
| **URL** | https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rates/ |
| **Date Accessed** | April 2026 |
| **Usage Restrictions** | Freely available; Bank of Canada terms of use apply |
| **Format** | CSV, 135 rows |

**Columns:**
- `date` — First day of month (YYYY-MM-DD)
- `boc_policy_rate_pct` — BoC overnight target rate (%)
- `mortgage_5yr_posted_rate_pct` — Chartered bank 5-year conventional posted mortgage rate (%)

**Citation (APA):**
Bank of Canada. (2026). *Key interest rates: Chartered bank interest rates*. https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rates/

---

### 2. `halifax_housing_market.csv`
| Field | Value |
|-------|-------|
| **Description** | Monthly Halifax Regional Municipality MLS residential housing market statistics |
| **Coverage** | January 2015 – December 2025 |
| **Source** | Nova Scotia Association of REALTORS® (NSAR) Market Statistics; Canada Mortgage and Housing Corporation (CMHC) Housing Market Outlook |
| **URL** | https://nsrealtors.com/market-statistics/ and https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-markets/housing-market-outlook |
| **Date Accessed** | April 2026 |
| **Usage Restrictions** | Publicly available market statistics; NSAR and CMHC terms of use apply |
| **Format** | CSV, 132 rows |

**Columns:**
- `date` — First day of month (YYYY-MM-DD)
- `avg_sale_price_cad` — Average residential sale price (CAD)
- `units_sold` — Number of residential units sold
- `new_listings` — Number of new listings added
- `months_of_inventory` — Active listings divided by trailing 3-month average sales
- `median_days_on_market` — Median days from listing to sale

**Citation (APA):**
Nova Scotia Association of REALTORS®. (2026). *Market statistics*. https://nsrealtors.com/market-statistics/

Canada Mortgage and Housing Corporation. (2026). *Housing market outlook: Halifax*. https://www.cmhc-schl.gc.ca

---

### 3. `hrm_affordability.csv`
| Field | Value |
|-------|-------|
| **Description** | Annual Halifax affordability metrics, demographics, housing starts, and rental market indicators |
| **Coverage** | 2015–2025 |
| **Source** | Statistics Canada (Census and Labour Force Survey); CMHC Rental Market Report; Nova Scotia Department of Finance and Treasury Board |
| **URLs** | https://www12.statcan.gc.ca ; https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-markets/rental-market-reports |
| **Date Accessed** | April 2026 |
| **Usage Restrictions** | Open Government Licence — Canada |
| **Format** | CSV, 11 rows |

**Columns:**
- `year` — Calendar year (YYYY)
- `median_hh_income_cad` — Estimated annual median household income, Halifax CMA (CAD)
- `hrm_population` — Estimated population, Halifax Regional Municipality
- `housing_starts` — Total residential housing starts, Halifax CMA (all types)
- `affordability_ratio_pct` — Monthly mortgage payment as % of median monthly household income (10% down, 25yr amort, posted 5yr rate)
- `rental_vacancy_rate_pct` — CMHC fall rental vacancy rate, Halifax CMA (%)
- `avg_monthly_rent_2br_cad` — CMHC average monthly rent for a 2-bedroom unit, Halifax CMA (CAD)

**Citation (APA):**
Statistics Canada. (2022). *Census profile, 2021 census of population: Halifax, census metropolitan area*. https://www12.statcan.gc.ca

Canada Mortgage and Housing Corporation. (2026). *Rental market report: Halifax*. https://www.cmhc-schl.gc.ca
