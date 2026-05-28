# Decoding the 2026 Tamil Nadu Assembly Election
### Resume Project Challenge #21 — Codebasics

> A data-only analysis for AtliQ Media's one-hour TV show on the 2026 Tamil Nadu Assembly Election results.
> All data sourced exclusively from the Election Commission of India. Non-partisan. No causal claims.

---

## 📌 Project Summary

| Field | Detail |
|---|---|
| **Challenge** | Codebasics Resume Project Challenge #21 |
| **Domain** | Media & Politics |
| **Function** | Data Analytics |
| **Difficulty** | Advanced |
| **Data Source** | Election Commission of India (ECI) only |

---

## 🔍 Three Stories Found in the Data

### Story 1 — The Turnout Record
Tamil Nadu's 2026 voter turnout reached **86.2%** — a **12.8 percentage-point jump** from 73.4% in 2021.
Only 5 of 234 constituencies crossed 85% in 2021. In 2026, **146 did**.
Chennai Metro recorded the steepest regional climb: from 63.4% to 84.6% (+21.2pp).

### Story 2 — The Seat Flip
**163 of 234 constituencies** returned a different winning party in 2026.
That is **7 in every 10 seats** changing hands compared to 2021.

### Story 3 — The Margin Shift
The median winning vote share fell from **48.2% in 2021 to 37.4% in 2026**.
**64 constituencies** were won with less than 35% of valid votes.
Despite record turnout, winners needed a smaller share of votes to win.

---

## 📁 Repository Structure

```
tn-election-2026-analysis/
│
├── dashboard/
│   └── app.py                                    # Streamlit dashboard app file
│
├── data/
│   ├── TN_2026_elections_data/
│   │   └── electors_data.html                    # Saved from elections.tn.gov.in — 2026 registered electors
│   │
│   ├── processed/
│   │   └── tn_election_combined.csv              # Master analytical dataset — output of analysis notebook
│   │
│   └── raw/
│       ├── constituency_master.csv               # Codebasics starter pack — AC master with region mapping
│       ├── tn_2021_results.csv                   # Codebasics starter pack — 2021 candidate-level results
│       └── tn_2026_results.csv                   # Codebasics starter pack — 2026 candidate-level results
│
├── image/
│   ├── bg_image.png                              # Background image used in Streamlit dashboard
│   ├── q2_sankey.png                             # Story 2: Seat flow Sankey diagram (static export)
│   └── q6_vote_share_distribution.png           # Story 3: Winner vote share distribution
│
├── notebooks/
│   ├── Tamil_Nadu_2026_Elections_—_Decoded_Dashboard_final.ipynb   # Dashboard creation + launch notebook
│   └── Tamil_Nadu_2026_Elections_—_Decoded_final.ipynb             # ← START HERE: full analysis notebook
│
├── slide_deck/
│   └── TN_Election_2026_AtliQ_Deck.pptx          # 10-slide stakeholder deck for AtliQ leadership
│
├── .gitignore
└── requirements.txt
```

---

## 📓 Notebooks — What Each One Does

### `Tamil_Nadu_2026_Elections_—_Decoded_final.ipynb` — Analysis Notebook
**Start here.** This is the primary end-to-end analysis notebook.

What it does:
- Loads all 3 raw CSVs from the Codebasics starter pack (`data/raw/`)
- Parses `electors_data.html` (sourced from elections.tn.gov.in) to get 2026 registered voters
- Merges electors data and calculates constituency-level 2026 turnout
- Identifies winners per constituency for both years
- Computes margins, vote shares, seat flips, and turnout delta
- Runs all 3 research questions (Q5 Turnout, Q2 Seat Flips, Q6 Margins)
- Generates chart images saved to `image/`
- Exports the master dataset `tn_election_combined.csv` to `data/processed/`

---

### `Tamil_Nadu_2026_Elections_—_Decoded_Dashboard_final.ipynb` — Dashboard Notebook
**Use this to launch the interactive Streamlit dashboard.**

What it does:
- Writes the complete `app.py` dashboard file using `%%writefile`
- Launches the Streamlit server on port 8501
- Generates a public URL via localtunnel for browser access
- Provides kill + relaunch cells for troubleshooting

> **Want to jump straight to the dashboard?**
> Open this notebook in Colab → make sure `tn_election_combined.csv` is in `/content/` → run all cells → open the printed URL in a new tab → enter the tunnel password when prompted.

---

## 🗂️ Data Sources

| Source | Used For | URL |
|---|---|---|
| ECI Results Portal (2026) | 2026 candidate results, votes, party | results.eci.gov.in/ResultAcGenMay2026 |
| Chief Electoral Officer, Tamil Nadu | 2026 registered electors (turnout denominator) | elections.tn.gov.in |
| Codebasics Starter Pack | Base CSVs for 2021 and 2026 results | Provided with challenge |
| ECI Statistical Reports | 2021 data cross-check | eci.gov.in/statistical-reports |

> ⚠️ **Note on 2026 turnout**: The `turnout` column in `tn_2026_results.csv` is intentionally blank (part of the challenge). Constituency-level electors data was sourced from the Tamil Nadu CEO website (ACwise Gender Count, April 2026 roll) and merged to calculate turnout. ECI Form-20 final audited data had not been released at the time of this analysis.

---

## ⚙️ Reproduction Steps

### Option A — Full analysis from scratch

#### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/tn-election-2026-analysis.git
cd tn-election-2026-analysis
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the analysis notebook

Open `notebooks/Tamil_Nadu_2026_Elections_—_Decoded_final.ipynb` in **Google Colab** (recommended) or Jupyter.

Run all cells in order. The notebook auto-detects file locations — no manual path changes needed. It outputs:
- `tn_election_combined.csv` → `data/processed/`
- Chart images → `image/`

#### 4. Launch the Streamlit dashboard

Open `notebooks/Tamil_Nadu_2026_Elections_—_Decoded_Dashboard_final.ipynb` in Colab.

Run all cells in order. Then:
1. Copy the printed URL and open it in a new browser tab
2. Enter the tunnel password printed in the output when the browser prompts
3. If the dashboard appears blank — **reload the tab 2–3 times** (this is normal on first launch)
4. If still not loading — run the **"Kill old processes"** cell, then re-run the launch cell

---

### Option B — View dashboard only (no analysis re-run needed)

1. Upload `data/processed/tn_election_combined.csv` to `/content/` in a new Colab session
2. Open `notebooks/Tamil_Nadu_2026_Elections_—_Decoded_Dashboard_final.ipynb`
3. Run all cells → open the URL → enter the tunnel password

---

### Option C — Run dashboard locally

```bash
pip install -r requirements.txt
cp data/processed/tn_election_combined.csv dashboard/
cd dashboard
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📊 Deliverables

| Deliverable | File | Description |
|---|---|---|
| Analysis Notebook | `notebooks/Tamil_Nadu_2026_Elections_—_Decoded_final.ipynb` | End-to-end Python analysis — start here |
| Dashboard Notebook | `notebooks/Tamil_Nadu_2026_Elections_—_Decoded_Dashboard_final.ipynb` | Creates app.py and launches dashboard |
| Master Dataset | `data/processed/tn_election_combined.csv` | 234 rows × 22 columns |
| Dashboard App | `dashboard/app.py` | Streamlit interactive dashboard |
| Stakeholder Deck | `slide_deck/TN_Election_2026_AtliQ_Deck.pptx` | 10 slides for AtliQ leadership |
| Chart Images | `image/` | Publication-ready chart files |

---

## 📐 Master Dataset Schema

`tn_election_combined.csv` — one row per constituency (234 rows)

| Column | Description |
|---|---|
| `ac_number` | ECI AC number (1–234) — primary key |
| `constituency` | Constituency name |
| `region` | Editorial six-region grouping (Chennai Metro / North / Central / Kongu / Delta / South) |
| `reserved` | Constituency type — GEN / SC / ST |
| `winner_2026` | Winning candidate name (2026) |
| `winning_party_2026` | Winning party abbreviation (2026) |
| `winner_votes_2026` | Votes received by winner (2026) |
| `total_votes_polled_2026` | Sum of all candidate votes in constituency (2026) |
| `total_electors_2026` | Registered electors from April 2026 roll |
| `turnout_2026` | Turnout % (2026) — calculated: total_votes_polled / total_electors × 100 |
| `winner_vote_share_2026` | Winner votes / total valid votes × 100 |
| `margin_2026` | Winner votes − runner-up votes (2026) |
| `winner_2021` | Winning candidate name (2021) |
| `winning_party_2021` | Winning party abbreviation (2021) |
| `winner_votes_2021` | Votes received by winner (2021) |
| `total_votes_polled_2021` | Sum of all candidate votes in constituency (2021) |
| `total_electors_2021` | Registered electors (2021) — back-calculated from turnout % in source data |
| `turnout_2021` | Turnout % (2021) — from Codebasics source data |
| `winner_vote_share_2021` | Winner votes / total valid votes × 100 |
| `margin_2021` | Winner votes − runner-up votes (2021) |
| `turnout_delta` | `turnout_2026 − turnout_2021` (percentage points) |
| `seat_flipped` | `True` if winning party changed between 2021 and 2026, else `False` |

---

## ⚠️ Data Limitations

1. **Turnout denominator** — 2026 electors from April 2026 electoral roll (elections.tn.gov.in). ECI Form-20 final audited data not yet released. Minor variations possible once Form-20 is published.

2. **No alliance-level data** — Parties are analysed individually as recorded by ECI. Alliance seat-sharing and vote-transfer patterns cannot be determined from candidate-level data alone.

3. **No causal claims** — This analysis describes what the data shows. It does not explain why turnout rose, why seats changed, or why margins shifted.

4. **2021 electors back-calculated** — Derived from the turnout percentage in the source data. May carry rounding from the original ECI figure.

5. **NOTA included** — NOTA votes are included in total valid votes for margin calculations, consistent with ECI methodology.

6. **Postal votes** — Included in candidate totals as reported by ECI. Polling-station level breakdown was not used.

---

## 🛡️ Non-Partisanship Statement

> This is a non-partisan data analysis exercise. All findings are described factually using only ECI data. No causal claims are made. No party, leader, alliance, community, or outcome is endorsed or criticised. Every chart title is written to read the same way to supporters of any party.
>
> Codebasics does not endorse, criticise, or take any political position on the parties, leaders, alliances, communities, or outcomes discussed in this challenge.

---

## 📦 Requirements

```
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.10.0
matplotlib>=3.6.0
seaborn>=0.12.0
streamlit>=1.20.0
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
kaleido==0.2.1
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔗 Links
- 📹 **Video walkthrough**: https://www.youtube.com/watch?v=Qwx7s5R0NQs
- 📊 **Live dashboard**: https://tn-election-2026-analysis-udpsdga3ixus4x6d2dicr6.streamlit.app/
---

## 📝 License

Data sourced from the Election Commission of India — publicly available under ECI's open data policy.
Analysis code is open for educational use.

---

*Submitted for Codebasics Resume Project Challenge #21 — Decoding the 2026 Tamil Nadu Assembly Election*
