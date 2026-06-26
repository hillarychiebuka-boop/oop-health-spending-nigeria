# 🇳🇬 Out-of-Pocket Health Spending vs Income — Nigerian Households

> **The problem:** When Nigerians get sick, most pay entirely from their own pocket.
> But nobody has clearly shown how that burden distributes across income levels —
> or which households are being financially destroyed by healthcare costs.

> **The finding:** The poorest 20% of Nigerian households spend 65% of their
> income on healthcare. The richest 20% spend 1.2%. That 55x gap is not a
> statistic — it is evidence of a health financing system that punishes poverty.

> **The action:** NHIA subsidy design must prioritise the bottom two income
> quintiles. Any coverage expansion that ignores this gap will protect the people
> who need it least.

**Author:** Hillary Onah — Finance & Data Science Analyst, DHIN

**Built:** June 2026 | **Stack:** Python · Pandas · Scikit-learn · Streamlit · Plotly

**Data:** Nigeria Living Standards Survey (NLSS) 2022 — National Bureau of Statistics

A screen recording of the live dashboard is available in the LinkedIn post linked below:

https://www.linkedin.com/posts/chiebuka-hillary-onah_healthfinance-datascience-nigeria-ugcPost-7476062809840144385-0AF3/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEFljTsBnhfx761Pb9UwpEsh9xn7sYfuVGA

---

## The story: Problem → Analysis → Insight → Recommendation → Impact

### Statement of Problem
Nigeria's NHIA covers less than 5% of the population. The majority of Nigerians
pay for healthcare entirely out of pocket, no insurance, no reimbursement,
no safety net. But the conversation about coverage expansion rarely starts with
the most important question: **who is bearing the heaviest burden right now,
and how heavy is it?**

Without answering that question with data, policy remains guesswork.

### Data Analysis
Used the NLSS 2022 microdata from Nigeria's National Bureau of Statistics,
covering 22,607 households across all 36 states and FCT Abuja. Extracted
four direct out-of-pocket spending variables (consultation fees, drug purchases,
hospital stays, transport costs), aggregated to household level, merged with
household income data, and calculated OOP burden as a percentage of income.

Built two machine learning models: Logistic Regression and Random Forest was built
to predict which households are at risk of catastrophic health expenditure
before it happens.

### Insight

| Finding | What it means |
|---------|--------------|
| Q1 median OOP burden: **65.8%** | The poorest households spend two-thirds of income on healthcare |
| Q5 median OOP burden: **1.2%** | The richest households barely notice the cost |
| **80% of Q1 households** above WHO catastrophic threshold | Financial crisis from healthcare is the normal experience for the poorest Nigerians |
| **Hospital stays (45.3%) + drugs (44.7%)** = 90% of all spending | Two categories drive nearly all the burden |
| **Kebbi (100%), Kaduna (55.6%), Ebonyi (30%)** — highest state burden | Northern states dominate the crisis geography |
| **FCT Abuja (0.7%), Lagos (0.5%)** — lowest burden | Urban economic advantage is stark and measurable |

### Recommendation

1. **Target NHIA subsidies at Q1 and Q2 households first**: These are the
   households already in financial crisis. Coverage expansion that starts
   with formal sector workers misses the people who need it most.

2. **Prioritise hospitalisation insurance**: At ₦14,501 average cost,
   hospital stays are the single largest cost shock. A catastrophic illness
   fund covering inpatient costs would address 45% of the burden immediately.

3. **Subsidise essential medicines access**: Drugs account for 44.7% of
   spending. Generic drug programs and community pharmacy subsidies would
   address the second largest cost category.

4. **Geographic targeting for northern states**: Kebbi, Kaduna, Adamawa,
   Jigawa, and Zamfara should be prioritised for Contributory Health Scheme
   rollout. The data shows these states carry burden levels that no
   uninsured household can sustainably absorb.

5. **Deploy the risk prediction model**: The Random Forest classifier can
   flag high-risk households from census or survey data before they
   experience catastrophic spending. Proactive enrollment targeting is more
   efficient than reactive emergency support.

### Impact
This framework applied directly to NHIA enrollment data with LGA-level
geography and household income proxies becomes a practical tool for
targeting subsidised coverage where the financial need is most acute.

The same model can be adapted by state governments designing Contributory
Health Schemes, by international health funders allocating Nigeria-specific
grants, and by HMOs identifying underserved markets with policy-backed
growth potential.

---

## Machine learning results

**Model objective:** Predict which households will experience catastrophic
health expenditure (>10% of income on healthcare) based on income, location,
zone, and state.

| Metric | Logistic Regression | Random Forest |
|--------|:-------------------:|:-------------:|
| Accuracy | 0.71 | 0.71 |
| ROC-AUC | 0.76 | 0.79 |
| F1 Score (Catastrophic class) | 0.74 | 0.69 |

**Why classification here vs regression in Project 1:**
Project 1 predicted *how much* a claim would cost (a number).
This project predicts *whether* a household will hit the catastrophic
threshold (yes or no). The policy question drives the model choice always.

---

## Key charts

**Chart 1 — OOP burden by income quintile**
The headline finding. A 55x gap between Q1 (65.8%) and Q5 (1.2%)
visualised with the WHO catastrophic threshold line showing that
only the two richest quintiles are safely below the danger line.

**Chart 2 — Urban vs Rural burden**
Whether geography compounds income poverty in health financing.

**Chart 3 — All-state burden ranking**
Every Nigerian state ranked by median OOP burden. The geographic
concentration of the crisis in northern states is immediately visible.

**Chart 4 — Spending category breakdown**
Where the money goes: hospital stays and drugs dominate at 90% combined,
making consultation fee waivers — a common policy tool — largely
ineffective at addressing the actual burden.

**Chart 5 — Catastrophic expenditure by quintile**
Not averages but crisis counts: 80% of Q1 households, 66.6% of Q2,
46.8% of Q3 — all above WHO's catastrophic threshold. The majority
of Nigerian households are in financial danger from healthcare costs.

---

## How to run

```bash
# Install dependencies
pip install pandas numpy pyreadstat matplotlib seaborn scikit-learn streamlit plotly

# Run ML notebook
jupyter notebook oop_analysis.ipynb

A screen recording of the live dashboard is available in the LinkedIn post linked below:

https://www.linkedin.com/posts/chiebuka-hillary-onah_healthfinance-datascience-nigeria-ugcPost-7476062809840144385-0AF3/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEFljTsBnhfx761Pb9UwpEsh9xn7sYfuVGA
```

**Note:** Place all three NLSS 2022 DTA files in the same folder:
- `2022nlss_sect03_health.dta`
- `2022nlss_sect00_cover.dta`
- `2022nlss_sect13_other_income.dta`

---

## Project structure

```
oop-health-spending-nigeria/
│
├── oop_analysis.ipynb              # Full analysis notebook
├── dashboard.py                    # Streamlit interactive dashboard
├── requirements.txt                # Dependencies
├── README.md                       # This file
│
├── chart1_oop_burden_by_quintile.png
├── chart2_urban_rural_burden.png
├── chart3_top10_states_burden.png
├── chart4_spending_breakdown.png
├── chart5_catastrophic_expenditure.png
├── chart6_feature_importance_ml.png
├── chart7_roc_curve.png
└── chart8_confusion_matrix.png
```

---

## Dataset

Nigeria Living Standards Survey (NLSS) 2022
National Bureau of Statistics (NBS) Nigeria
22,607 households · 36 states + FCT · All geopolitical zones

Access: microdata.nigerianstat.gov.ng

**Key variables used:**
- `s3q14` — Consultation fees paid
- `s3q15` — Transport costs to healthcare
- `s3q18a` — Drug purchases (over the counter)
- `s3q21a` — Hospital stay costs
- `s13q2` — Household income by source

---

## Limitations

- 5,485 households had complete income and health spending records
  (24% of full sample) — households too poor to seek care may be
  underrepresented, meaning the true Q1 burden could be worse than shown.
- Kebbi's 100% figure should be interpreted cautiously given small
  state-level sample sizes.
- Income data captures reported income only — informal income sources
  may be underreported, which could affect quintile classification.
---

*Built as part of a structured health finance data science portfolio
at the Digital Healthcare Interoperability Network (DHIN), Abuja, Nigeria.*
*This is Project 2 of an ongoing series at the intersection of finance,
data science, and Nigerian health systems.*
