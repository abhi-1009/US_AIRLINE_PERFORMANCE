# ✈️ U.S. Airline Performance & Delay Analysis — 2015

> A comprehensive end-to-end data analytics project analysing **5,819,079 domestic U.S. flights** across **14 airlines** for the full calendar year 2015 — using MySQL, Python, and Power BI.

**Prepared by:** Abhijit Sinha
**Internship:** Labmentix | May 2026
**GitHub:** [github.com/abhi-1009](https://github.com/abhi-1009)

---

## 📊 Key Metrics at a Glance

| Metric | Value |
|---|---|
| ✈️ Total Flights Analysed | 5,819,079 |
| ⏱️ Delayed Flights | 1,023,498 (17.6%) |
| ❌ Cancelled Flights | 89,884 (1.54%) |
| ✅ Overall On-Time Performance | 82.14% |
| 📅 Average Arrival Delay | 4.41 min |
| 🏆 Best OTP Airline | Hawaiian Airlines (89.47%) |
| ⚠️ Worst OTP Airline | Spirit Air Lines (71.25%) |
| 📆 Best Month to Fly | October (88.2% OTP) |
| 📆 Worst Delay Month | March (9.6 min avg delay) |
| 🎛️ Controllable Delays | 72% (Airline + Late Aircraft) |

---

## 📁 Table of Contents

1. [Problem Statement](#problem-statement)
2. [Objectives](#objectives)
3. [Tech Stack](#tech-stack)
4. [Dataset](#dataset)
5. [Project Workflow](#project-workflow)
6. [Key Findings](#key-findings)
7. [Airline Performance Rankings](#airline-performance-rankings)
8. [Delay Analysis](#delay-analysis)
9. [Cancellation Analysis](#cancellation-analysis)
10. [Time Trend Analysis](#time-trend-analysis)
11. [Route & Airport Analysis](#route--airport-analysis)
12. [Power BI Dashboard](#power-bi-dashboard)
13. [Actionable Recommendations](#actionable-recommendations)
14. [Project Structure](#project-structure)

---

## 🎯 Problem Statement

Despite advances in scheduling technology, U.S. airlines continue to suffer from high delay and cancellation rates. Airline operations teams, airport authorities, and passengers lack consolidated, actionable visibility into:

- The **root causes** of delays and cancellations
- **Timing patterns** — which months, days, and hours carry the highest risk
- **Airline-level performance differentials**
- Whether delays are within airline control or driven by external factors

This project addresses that gap with a full end-to-end analytics pipeline.

---

## 🎯 Objectives

- Which airlines deliver the **best and worst on-time performance (OTP)**?
- What are the **primary causes** of flight delays and cancellations?
- Which **months, days of week, and time-of-day slots** carry the highest delay risk?
- Which **routes and airports** are most prone to delays?
- What proportion of delays are **within airline control** vs external factors?
- How do delay patterns **vary across the calendar year**?

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **MySQL 8.0** | Database creation, data ingestion, staging, transformation, indexing, views |
| **Python** | Bulk loading of 5.8M rows via chunked inserts into MySQL |
| **Power BI Desktop** | Interactive 7-page dashboard — overview, delay, airline, route, time, cancellation, conclusion |

---

## 📂 Dataset

**Source:** 2015 U.S. Flight Delays and Cancellations — Bureau of Transportation Statistics (BTS) via Kaggle

| File | Contents | Size |
|---|---|---|
| `flights.csv` | Flight-level operational data (delays, times, distances) | 5,819,079 rows |
| `airlines.csv` | IATA codes and full airline names | 14 airlines |
| `airports.csv` | Airport codes, cities, states, coordinates | 322 airports |

---

## ⚙️ Project Workflow

```
Raw CSV Files
      │
      ▼
┌─────────────────────────────────┐
│  PHASE 1 — Data Ingestion       │
│  Python chunked loader →        │
│  MySQL staging table (all TEXT) │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  PHASE 2 — Transformation       │
│  Cast columns, derive:          │
│  FLIGHT_DATE, DEPARTURE_HOUR,   │
│  IS_DELAYED, CANCEL_REASON_DESC │
│  Set NULL delays → 0            │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  PHASE 3 — Indexing & Views     │
│  9 indexes on key columns       │
│  vw_flights_enriched view       │
│  (flights + airlines + airports)│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  PHASE 4 — Analysis & Dashboard │
│  SQL queries → OTP, delay       │
│  causes, routes, time trends    │
│  Power BI 7-page dashboard      │
└─────────────────────────────────┘
```

### Derived Columns Created

| Column | Type | Description |
|---|---|---|
| `FLIGHT_DATE` | DATE | Parsed from raw date fields |
| `SCHEDULED_DEP_TIME` | TIME | Standardised departure time |
| `ACTUAL_ARR_TIME` | TIME | Standardised arrival time |
| `DEPARTURE_HOUR` | TINYINT | Hour of departure (0–23) |
| `IS_DELAYED` | Binary Flag | 1 if arrival delay > 15 min AND not cancelled |
| `CANCELLATION_REASON_DESC` | VARCHAR | Human-readable label (Weather / Airline / NAS / Security) |

> **Delay Classification:** A flight is classified as delayed if its arrival delay exceeds **15 minutes** — the FAA standard — and it was not cancelled.

---

## 🔍 Key Findings

### 🔴 The Most Important Discovery
> **72% of all delay minutes are directly controllable by airlines.**
> Weather — the most emotionally blamed factor — accounts for only **~5% of delay minutes**.

| Delay Category | Share | Nature |
|---|---|---|
| Late Aircraft (Cascading) | 39.84% | ✅ Controllable — prior flight arrived late |
| Airline / Carrier | 32.20% | ✅ Controllable — maintenance, crew, turnaround |
| Air System (NAS) | 22.88% | ⚠️ Partially controllable — ATC, runway congestion |
| Weather | 4.95% | ❌ External / uncontrollable |
| Security | 0.13% | ❌ External / uncontrollable |

---

## 🏆 Airline Performance Rankings

| Rank | Airline | Total Flights | OTP Rate % | Cancel Rate % | Avg Arr Delay (min) |
|---|---|---|---|---|---|
| 🥇 1 | Hawaiian Airlines | 76,272 | **89.47** | 0.22 | 2.02 |
| 🥈 2 | Alaska Airlines | 172,521 | 87.69 | 0.39 | −0.98 |
| 🥉 3 | Delta Air Lines | 875,881 | 87.03 | 0.44 | 0.19 |
| 4 | American Airlines | 725,984 | 82.49 | 1.50 | 3.45 |
| 5 | US Airways | 198,715 | 82.05 | 2.05 | 3.71 |
| 6 | SkyWest Airlines | 588,353 | 82.05 | 1.69 | 5.85 |
| 7 | Southwest Airlines | 1,261,855 | 81.75 | 1.27 | 4.37 |
| 8 | Virgin America | 61,903 | 81.51 | 0.86 | 4.74 |
| 9 | Atlantic Southeast | 571,977 | 81.08 | 2.66 | 6.59 |
| 10 | United Air Lines | 515,723 | 80.10 | 1.27 | 5.43 |
| 11 | American Eagle | 294,632 | 79.03 | **5.10** | 6.46 |
| 12 | JetBlue Airways | 267,048 | 78.21 | 1.60 | 6.68 |
| 13 | Frontier Airlines | 90,836 | 74.68 | 0.65 | 12.50 |
| ⚠️ 14 | Spirit Air Lines | 117,379 | **71.25** | 1.71 | **14.47** |
| — | **System Total** | **5,819,079** | **82.14** | **1.54** | **4.41** |

### Key Insights
- 🏆 **Hawaiian Airlines** leads with 89.47% OTP and the lowest cancellation rate (0.22%) — benefits from short, controlled inter-island routes and stable Pacific weather
- 📈 **Alaska Airlines & Delta** are standout large-network performers — both above 87% OTP, well above the 82.14% system average
- 💪 **Southwest Airlines** operates the highest volume (1.26M flights) while maintaining 81.75% OTP — strong operational efficiency at scale
- ⚠️ **Spirit Airlines** records the worst OTP (71.25%) and highest average delay (14.47 min)
- ❌ **American Eagle** has the highest cancellation rate (5.10%) — 3.3x the system average

---

## 📅 Delay Analysis

### Monthly Delay Trend

| Month | Avg Arrival Delay (min) | Note |
|---|---|---|
| January | 5.81 | Winter weather impacts begin |
| February | 6.10 | Elevated — winter storms, highest cancellations (4.78%) |
| **March** | **9.60** | ⚠️ **Peak delay month** |
| April | −0.80 | ✅ Best month — flights arrive early on average |
| May | 3.20 | Stable — spring shoulder season |
| **June** | **8.30** | ⚠️ Second-highest — summer travel surge |
| July | 4.60 | Moderate — mid-summer |
| August | 4.90 | Moderate — late summer |
| September | 4.50 | Stable — post-summer demand ease |
| **October** | **1.10** | ✅ **Second-best delay month, best OTP (88.2%)** |
| November | 6.40 | Rises — early holiday travel pressure |
| December | −0.80 | ✅ Early flights mask year-end pressure |

---

## ❌ Cancellation Analysis

**Total Cancellations: 89,884 (1.54% system rate)**

### Cancellation by Cause

| Reason | Count | Share |
|---|---|---|
| Weather | 48,851 | **54.35%** — dominant cause |
| Airline / Carrier | 25,262 | 28.11% |
| National Air System | 15,749 | 17.52% |
| Security | ~18 | 0.02% |

> Note: Weather dominates **cancellations** (54%) but only contributes ~5% of **delay minutes** — airlines absorb weather impact into delays wherever possible, resorting to cancellations only when flights are entirely non-viable.

### Monthly Cancellation Rate

| Month | Cancel Rate % |
|---|---|
| **February** | **4.78% — Peak ⚠️** |
| January | 2.55% |
| March | 2.18% |
| June | 1.81% |
| **September** | **0.45% — Lowest ✅** |
| **October** | **0.50% — Second Lowest ✅** |

### Highest Cancellation Airlines
- **American Eagle Airlines** — 5.10% (highest)
- **Atlantic Southeast** — 2.66%
- **US Airways** — 2.05%

### Most-Cancelled Origin Cities
- Ithaca, NY — 11.76%
- Mammoth Lakes, CA — 10.26%
- Hailey (Sun Valley), ID — 9.21%
- Devils Lake, ND — 8.76%
- Aspen, CO — 7.75%

---

## ⏰ Time Trend Analysis

### Day of Week — Delay Rates

| Day | Delay Rate % | Assessment |
|---|---|---|
| **Saturday** | **15%** | ✅ Best day — lowest delay risk |
| Tuesday | 17% | Good |
| Wednesday | 17% | Good |
| Sunday | 17% | Moderate |
| Friday | 18% | High — weekend leisure travel |
| **Monday** | **19%** | ⚠️ Worst — business travel peak |
| **Thursday** | **19%** | ⚠️ Worst — end-of-week surge |

### Departure Hour Analysis

| Time Slot | Avg Arrival Delay | Assessment |
|---|---|---|
| **05:00–08:00** | **Negative (early)** | ✅ Best time to fly |
| 10:00–14:00 | Moderate | Delays building |
| **20:00–21:00** | **10+ minutes** | ⚠️ Worst — ripple effect peaks |

> The "ripple effect" — aircraft accumulate cascading delays throughout the day. First flight of the day has the cleanest slate.

---

## 🗺️ Route & Airport Analysis

### Top Busiest Routes

| Route | Flights | Avg Delay (min) |
|---|---|---|
| SFO → LAX | 13,744 | 11.44 |
| LAX → SFO | 13,457 | 10.74 |
| JFK → LAX | 12,016 | −2.67 ✅ |
| LAX → JFK | 12,015 | 0.61 |
| LAS → LAX | 9,715 | 11.97 |

### Highest-Delay Routes

| Route | Avg Delay (min) | Delay Rate % |
|---|---|---|
| Aspen → Dallas-Fort Worth | 39.97 | 33% |
| New York → Eagle, CO | 38.01 | 30% |
| Atlantic City → Detroit | 30.90 | 41% |
| Minneapolis → Trenton | 30.23 | 42% |

### Top Airports by Volume

| Airport | Total Departures |
|---|---|
| Chicago (O'Hare + Midway) | 366,770 |
| Atlanta (Hartsfield-Jackson) | 346,836 |
| Dallas-Fort Worth | 239,551 |
| Houston | 198,664 |
| Denver | 196,055 |
| Los Angeles | 194,673 |

---

## 📊 Power BI Dashboard

**7 interactive pages — all pages include Month Name, Airline Name & Day Name slicers for cross-filtering**

| Page | Title | Key Visuals |
|---|---|---|
| Cover | Dashboard Entry | Full-screen visual + Enter Dashboard button |
| 1 | Overview | 6 KPI cards, OTP Rate by Airline bar, Flight Volume by Airline |
| 2 | Airline Performance | Airline logo slicers, Avg Delay bar, OTP vs Delay Rate scatter, full summary table |
| 3 | Delay Analysis | Delay Causes donut, Monthly Delay Trend line, Delay Rate by Airline, Monthly OTP Heatmap |
| 4 | Route & Airport Analysis | Total Flights map, Top Airports by volume & delay, Busiest Routes, Highest-Delay Routes |
| 5 | Time Trends | Monthly OTP line, Delay Rate by Day of Week, Avg Delay by Departure Hour |
| 6 | Cancellation Analysis | Cancellation Reasons donut, Monthly Trend, Cancel Rate by Airline, Most Cancelled Cities |
| 7 | Conclusion | Best/Worst summary cards + 5 headline findings |

---

## 💡 Actionable Recommendations

### For Airlines
- 🔧 **Reduce late-aircraft cascades** — 39.84% of delays stem from prior-flight lateness; build buffer time into mid-day and evening schedules at Chicago, Atlanta, and Dallas-Fort Worth
- ⚙️ **Invest in turnaround efficiency** — predictive maintenance analytics and crew scheduling optimisation can directly reduce the 32.2% airline-controlled delay share
- 📈 **Focus on bottom-quartile carriers** — Spirit, Frontier, and JetBlue (OTP: 71–78%) have the greatest improvement opportunity
- ✈️ **American Eagle cancellation reduction** — with a 5.10% rate, route-level weather-risk assessment and proactive re-accommodation protocols are essential

### For Airport Authorities
- 🏗️ **Chicago O'Hare capacity management** — investment in runway throughput and gate management would generate system-wide benefits as the busiest and most delay-prone hub
- 🌨️ **Regional airport resilience** — airports like Ithaca, Mammoth Lakes, and Aspen (above 8% cancellation) need improved ground handling and de-icing infrastructure

### For Passengers
- ⏰ **Book early morning departures (05:00–08:00)** — average arrival delays are negative; flights arrive early
- 📅 **Fly on Saturdays** — 15% delay rate vs 19% on Mondays/Thursdays
- 🗓️ **Best travel months: October, April, September** — avoid March (worst delays) and February (worst cancellations)
- ✈️ **Choose Hawaiian, Alaska, or Delta** for the highest reliability

---

## 📁 Project Structure

```
us_airline_analysis/
│
├── data/
│   ├── flights.csv              # 5.8M flight records (raw)
│   ├── airlines.csv             # 14 airline IATA codes
│   └── airports.csv             # 322 airport details
│
├── sql/
│   ├── 01_create_staging.sql    # Staging table with all-TEXT columns
│   ├── 02_create_flights.sql    # Production table with correct data types
│   ├── 03_transform.sql         # Derived columns & NULL handling
│   ├── 04_indexes.sql           # 9 performance indexes
│   ├── 05_views.sql             # vw_flights_enriched view
│   └── 06_analysis_queries.sql  # OTP, delay, route, cancellation queries
│
├── python/
│   └── load_flights.py          # Chunked bulk loader for 5.8M rows
│
├── dashboard/
│   └── US_Flight_Analysis.pbix  # Power BI 7-page dashboard
│
└── README.md
```

---

## 📌 Conclusion

This analysis of 5.82 million U.S. domestic flights in 2015 reveals:

- The system operates at **82.14% on-time rate** — with substantial variance across airlines, routes, seasons, and departure times
- **72% of delay minutes are airline-controllable** — the industry has considerable power to improve without waiting for weather to change
- **Hawaiian Airlines** demonstrates high OTP is achievable; **Southwest** proves the highest-volume operator can maintain competitive punctuality
- **October** is the standout month; **early-morning departures** are strongly preferable; **Saturday** is the safest day to fly
- **Weather dominates cancellations** (54.35%) but contributes only ~5% of delay minutes

---

## 👤 Author

**Abhijit Sinha** — Data Analyst
- 📧 sinhaabhijit12@yahoo.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/abhijit-sinha-053b159a)
- 🐙 [GitHub](https://github.com/abhi-1009)

---

*Project completed during Data Analyst Internship at Labmentix | May 2026*

