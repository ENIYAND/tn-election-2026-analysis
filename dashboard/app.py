
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────
# BACKGROUND IMAGE SETUP
# ─────────────────────────────────────────────
import base64

def add_bg_image(image_path: str, opacity: float = 0.06):
    """
    Adds a low-opacity background image to the Streamlit app.
    """
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        # Detect format from filename
        ext = image_path.split('.')[-1].lower()
        mime = {'jpg':'jpeg','jpeg':'jpeg',
                'png':'png','svg':'svg+xml'}.get(ext, 'png')

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/{mime};base64,{encoded}");
            background-size: contain;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(255, 255, 255, {1 - opacity});
            pointer-events: none;
            z-index: 0;
        }}
        /* Keep all content readable above background */
        .block-container {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        pass


add_bg_image('/content/bg_image.png', opacity=0.10)


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TN Election 2026 | AtliQ Media",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)


add_bg_image('/content/bg_image.png', opacity=0.06)

# ─────────────────────────────────────────────
# LOAD DATA — direct path, no drive.mount
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    # Tries current directory first, then /content
    for path in ['tn_election_combined.csv',
                 '/content/tn_election_combined.csv']:
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            continue
    st.error("❌ Data file not found. Make sure tn_election_combined.csv "
             "is in the same folder as app.py")
    st.stop()

combined = load_data()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.title("🗳️ Filters")
st.sidebar.markdown("---")

all_regions = sorted(combined['region'].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Select Region(s)", options=all_regions, default=all_regions
)

all_reserved = sorted(combined['reserved'].dropna().unique().tolist())
selected_reserved = st.sidebar.multiselect(
    "Constituency Type", options=all_reserved, default=all_reserved
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data Source:** Election Commission of India  \n"
    "results.eci.gov.in  \n"
    "elections.tn.gov.in  \n\n"
    "*Non-partisan. ECI data only.*"
)

# Apply filters
filtered = combined[
    combined['region'].isin(selected_regions) &
    combined['reserved'].isin(selected_reserved)
].copy()

total_n   = len(filtered)
flipped_n = int(filtered['seat_flipped'].sum())

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center;color:#1E3A5F;font-size:2rem;'>
    🗳️ Decoding the 2026 Tamil Nadu Assembly Election
</h1>
<p style='text-align:center;color:#6B7280;font-size:1rem;'>
    Data-only analysis for AtliQ Media &nbsp;|&nbsp;
    Source: Election Commission of India
</p>
<hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP METRIC STRIP
# ─────────────────────────────────────────────
m1,m2,m3,m4,m5 = st.columns(5)

m1.metric("Constituencies", f"{total_n}", "in selection")
m2.metric("Avg Turnout 2026",
          f"{filtered['turnout_2026'].mean():.1f}%",
          f"+{(filtered['turnout_2026']-filtered['turnout_2021']).mean():.1f}pp vs 2021")
m3.metric("Seats Changed",
          f"{flipped_n}",
          f"{flipped_n/total_n*100:.0f}% of selection")
m4.metric("Median Win Share 2026",
          f"{filtered['winner_vote_share_2026'].median():.1f}%",
          f"{filtered['winner_vote_share_2026'].median()-filtered['winner_vote_share_2021'].median():.1f}pp vs 2021")
m5.metric("Avg Margin 2026",
          f"{filtered['margin_2026'].mean():,.0f} votes",
          f"{filtered['margin_2026'].mean()-filtered['margin_2021'].mean():+,.0f} vs 2021")

st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════
# STORY 1 — TURNOUT
# ═════════════════════════════════════════════
st.markdown("""
<div style='background:#EFF6FF;padding:16px 24px;
            border-left:5px solid #2563EB;border-radius:6px;'>
<h2 style='color:#1E3A5F;margin:0;font-size:1.25rem;'>
📈 The Turnout story — Tamil Nadu's 2026 voter turnout reached 86.2%,
a 12.8 percentage-point jump from 2021
</h2></div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Turnout by Region: 2021 vs 2026")
    region_t = (
        filtered.groupby('region')
        .agg(t21=('turnout_2021','mean'),
             t26=('turnout_2026','mean'))
        .reset_index()
        .sort_values('t26', ascending=False)
    )
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Bar(
        name='2021', x=region_t['region'], y=region_t['t21'],
        marker_color='#93C5FD',
        text=region_t['t21'].round(1).astype(str)+'%',
        textposition='outside'
    ))
    fig_reg.add_trace(go.Bar(
        name='2026', x=region_t['region'], y=region_t['t26'],
        marker_color='#1D4ED8',
        text=region_t['t26'].round(1).astype(str)+'%',
        textposition='outside'
    ))
    fig_reg.update_layout(
        barmode='group', yaxis_range=[55,100],
        yaxis_title='Average Turnout (%)',
        legend=dict(orientation='h',y=1.12),
        height=380, plot_bgcolor='white',
        yaxis=dict(gridcolor='#F3F4F6'),
        margin=dict(t=10,b=10)
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with col2:
    st.subheader("Top 20 Constituencies: Largest Turnout Jump")
    top20 = (
        filtered[['constituency','region',
                   'turnout_2021','turnout_2026','turnout_delta']]
        .sort_values('turnout_delta', ascending=False)
        .head(20)
        .sort_values('turnout_delta', ascending=True)
    )
    fig_top = px.bar(
        top20, x='turnout_delta', y='constituency',
        orientation='h', color='region',
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={'turnout_delta':'Increase (pp)','constituency':''},
        text=top20['turnout_delta'].apply(lambda x: f'+{x:.1f}pp')
    )
    fig_top.update_traces(textposition='outside')
    fig_top.update_layout(
        height=420, plot_bgcolor='white',
        xaxis=dict(gridcolor='#F3F4F6'),
        legend=dict(orientation='h',y=-0.15),
        margin=dict(t=10,b=10)
    )
    st.plotly_chart(fig_top, use_container_width=True)

with st.expander("📋 Full Turnout Data Table"):
    tbl = (
        filtered[['constituency','region','reserved',
                   'turnout_2021','turnout_2026','turnout_delta']]
        .sort_values('turnout_delta', ascending=False)
        .reset_index(drop=True)
    )
    tbl.columns = ['Constituency','Region','Type',
                    'Turnout 2021%','Turnout 2026%','Change pp']
    st.dataframe(tbl, use_container_width=True, height=300)

st.markdown("---")

# ═════════════════════════════════════════════
# STORY 2 — SEAT FLIPS / SANKEY
# ═════════════════════════════════════════════
st.markdown("""
<div style='background:#F0FDF4;padding:16px 24px;
            border-left:5px solid #16A34A;border-radius:6px;'>
<h2 style='color:#14532D;margin:0;font-size:1.25rem;'>
🔄 The Flip story — 163 of 234 constituencies returned a different
winning party in 2026 — 7 in every 10 seats changed hands
</h2></div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns([1.3, 0.7])

PARTY_COLORS = {
    'DMK':'#0EA5E9','AIADMK':'#10B981','TVK':'#8B5CF6',
    'INC':'#F59E0B','BJP':'#F97316','PMK':'#06B6D4',
    'VCK':'#EC4899','CPI':'#84CC16','CPI(M)':'#14B8A6',
    'Others':'#CBD5E1'
}
DEFAULT_C = '#CBD5E1'
THRESHOLD = 3

with col3:
    st.subheader("Seat Flow: 2021 → 2026")

    net_c = pd.concat([
        filtered['winning_party_2021'].value_counts().rename('s21'),
        filtered['winning_party_2026'].value_counts().rename('s26')
    ], axis=1).fillna(0).astype(int)

    major = list(
        set(net_c[net_c['s21'] >= THRESHOLD].index) |
        set(net_c[net_c['s26'] >= THRESHOLD].index)
    )

    def remap(p): return p if p in major else 'Others'
    filtered['p21g'] = filtered['winning_party_2021'].apply(remap)
    filtered['p26g'] = filtered['winning_party_2026'].apply(remap)

    flow_g = (
        filtered.groupby(['p21g','p26g'])
        .size().reset_index(name='seats')
    )

    has_others = ('Others' in flow_g['p21g'].values or
                  'Others' in flow_g['p26g'].values)
    all_p     = major + (['Others'] if has_others else [])
    nl        = [f"{p} (2021)" for p in all_p]
    nr        = [f"{p} (2026)" for p in all_p]
    all_nodes = nl + nr
    ni        = {n:i for i,n in enumerate(all_nodes)}

    def hex_rgba(h, a=1.0):
        h = h.lstrip('#')
        r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
        return f'rgba({r},{g},{b},{a})'

    nc = (
        [hex_rgba(PARTY_COLORS.get(p,DEFAULT_C), 0.55) for p in all_p] +
        [hex_rgba(PARTY_COLORS.get(p,DEFAULT_C), 1.00) for p in all_p]
    )

    srcs,tgts,vals,lc = [],[],[],[]
    for _,row in flow_g.iterrows():
        sk = f"{row['p21g']} (2021)"
        tk = f"{row['p26g']} (2026)"
        if sk in ni and tk in ni:
            srcs.append(ni[sk]); tgts.append(ni[tk])
            vals.append(int(row['seats']))
            lc.append(hex_rgba(
                PARTY_COLORS.get(row['p21g'],DEFAULT_C), 0.25))

    fig_s = go.Figure(go.Sankey(
        arrangement='snap',
        textfont=dict(color="black", size=12),
        node=dict(pad=18, thickness=25,
                  label=all_nodes, color=nc,
                  line=dict(color='white', width=0.5)),
        link=dict(source=srcs, target=tgts,
                  value=vals, color=lc)
    ))
    fig_s.update_layout(
        title=dict(
            text=(f"{flipped_n} of {total_n} seats changed hands "
                  f"({flipped_n/total_n*100:.0f}%)"),
            font=dict(size=13)
        ),
        height=430,
        margin=dict(l=10,r=10,t=50,b=10)
    )
    st.plotly_chart(fig_s, use_container_width=True)

with col4:
    st.subheader("Seats Won: 2021 vs 2026")

    seat_tbl = pd.concat([
        filtered['winning_party_2021'].value_counts().rename('2021'),
        filtered['winning_party_2026'].value_counts().rename('2026')
    ], axis=1).fillna(0).astype(int)
    seat_tbl['Net'] = seat_tbl['2026'] - seat_tbl['2021']
    seat_tbl = (seat_tbl.sort_values('2026', ascending=False)
                .reset_index().rename(columns={'index':'Party'}))

    def net_arrow(val):
      if val > 0:   return f"▲ {val}"
      elif val < 0: return f"▼ {val}"
      return f"— {val}"

    seat_tbl['Net Change'] = seat_tbl['Net'].apply(net_arrow)
    seat_tbl_display = seat_tbl.drop(columns=['Net'])


    def style_net_change(val):
        if isinstance(val, str):
            if '▲' in val: return 'color: #16A34A; font-weight: bold;'
            elif '▼' in val: return 'color: #DC2626; font-weight: bold;'
        return 'color: #6B7280;'

    if hasattr(seat_tbl_display.style, 'map'):
        styled_df = seat_tbl_display.style.map(style_net_change, subset=['Net Change'])
    else:
        styled_df = seat_tbl_display.style.applymap(style_net_change, subset=['Net Change'])

    st.dataframe(styled_df, use_container_width=True, height=360)


    st.markdown(f"""
    <div style='background:#F9FAFB;padding:12px;
                border-radius:6px;margin-top:8px;
                font-size:0.9rem;'>
        <b>Seats changed:</b> {flipped_n}
        ({flipped_n/total_n*100:.1f}%)<br>
        <b>Seats held:</b> {total_n-flipped_n}
        ({(total_n-flipped_n)/total_n*100:.1f}%)
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═════════════════════════════════════════════
# STORY 3 — MARGINS
# ═════════════════════════════════════════════
st.markdown("""
<div style='background:#FFF7ED;padding:16px 24px;
            border-left:5px solid #EA580C;border-radius:6px;'>
<h2 style='color:#7C2D12;margin:0;font-size:1.25rem;'>
📊 The margin of victory story — The median winning vote share fell from 48% in 2021
to 37% in 2026 — winners won with less, not more
</h2></div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

above50_21 = int((filtered['winner_vote_share_2021'] > 50).sum())
above50_26 = int((filtered['winner_vote_share_2026'] > 50).sum())
below35_21 = int((filtered['winner_vote_share_2021'] < 35).sum())
below35_26 = int((filtered['winner_vote_share_2026'] < 35).sum())

col5, col6 = st.columns(2)

with col5:
    st.subheader("Winner Vote Share: 2021 vs 2026")
    fig_h = go.Figure()
    fig_h.add_trace(go.Histogram(
        x=filtered['winner_vote_share_2021'].dropna(),
        xbins=dict(start=20,end=80,size=3),
        name='2021', marker_color='#93C5FD', opacity=0.8
    ))
    fig_h.add_trace(go.Histogram(
        x=filtered['winner_vote_share_2026'].dropna(),
        xbins=dict(start=20,end=80,size=3),
        name='2026', marker_color='#1D4ED8', opacity=0.8
    ))
    fig_h.add_vline(x=50, line_dash='dash', line_color='#DC2626',
                    line_width=2, annotation_text='50%',
                    annotation_position='top right')
    fig_h.add_vline(x=35, line_dash='dash', line_color='#F59E0B',
                    line_width=2, annotation_text='35%',
                    annotation_position='top left')
    fig_h.update_layout(
        barmode='overlay',
        xaxis_title="Winner's % of Valid Votes",
        yaxis_title='Constituencies',
        height=370,
        legend=dict(orientation='h',y=1.12),
        plot_bgcolor='white',
        yaxis=dict(gridcolor='#F3F4F6'),
        margin=dict(t=10,b=10)
    )
    st.plotly_chart(fig_h, use_container_width=True)

with col6:
    st.subheader("Margin Summary Table")
    summary = pd.DataFrame({
        'Metric': [
            'Avg margin (votes)',
            'Median vote share',
            'Winners above 50%',
            'Winners 35–50%',
            'Winners below 35%',
            'Highest vote share',
            'Lowest vote share',
        ],
        '2021': [
            f"{filtered['margin_2021'].mean():,.0f}",
            f"{filtered['winner_vote_share_2021'].median():.1f}%",
            f"{above50_21} ({above50_21/total_n*100:.1f}%)",
            f"{total_n-above50_21-below35_21}",
            f"{below35_21} ({below35_21/total_n*100:.1f}%)",
            f"{filtered['winner_vote_share_2021'].max():.1f}%",
            f"{filtered['winner_vote_share_2021'].min():.1f}%",
        ],
        '2026': [
            f"{filtered['margin_2026'].mean():,.0f}",
            f"{filtered['winner_vote_share_2026'].median():.1f}%",
            f"{above50_26} ({above50_26/total_n*100:.1f}%)",
            f"{total_n-above50_26-below35_26}",
            f"{below35_26} ({below35_26/total_n*100:.1f}%)",
            f"{filtered['winner_vote_share_2026'].max():.1f}%",
            f"{filtered['winner_vote_share_2026'].min():.1f}%",
        ]
    })

    st.table(summary)

    st.markdown("**Top 10 Closest Races — 2026**")

    st.caption("Source: ECI results data. Party names as recorded by ECI.")

    closest = (
        filtered[['constituency','region',
                   'winning_party_2026','margin_2026']]
        .sort_values('margin_2026').head(10)
        .reset_index(drop=True)
    )

    closest.columns = ['Constituency','Region','Party','Margin']

    #st.dataframe() to enable the scrollbar
    st.dataframe(closest, use_container_width=True, height=210)

st.markdown("---")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='background:#F9FAFB;padding:16px 24px;
            border-radius:8px;text-align:center;'>
<p style='color:#6B7280;font-size:0.82rem;margin:0;'>
<b>Data Sources:</b>
Election Commission of India — results.eci.gov.in/ResultAcGenMay2026
&nbsp;|&nbsp; elections.tn.gov.in &nbsp;|&nbsp;
Codebasics Starter Pack<br>
<b>Limitations:</b> 2026 electors from April 2026 electoral roll.
ECI Form-20 final data not yet released at time of analysis.
No causal claims made. Non-partisan analysis.
</p></div>
""", unsafe_allow_html=True)
