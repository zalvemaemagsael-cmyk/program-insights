import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Program Insights – DOST SETUP 4.0 iFund",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #f7f7f3; }
header, footer, [data-testid="stDecoration"], #MainMenu { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem 2rem; max-width: 1200px; }

.page-title { font-size: 22px; font-weight: 700; color: #111; margin-bottom: 2px; }
.page-sub   { font-size: 13px; color: #999; margin-bottom: 24px; }

.section-title {
    font-size: 11px; font-weight: 700; color: #888;
    text-transform: uppercase; letter-spacing: .1em;
    margin: 32px 0 14px 0;
    padding-bottom: 6px;
    border-bottom: 1.5px solid #e5e7eb;
}

.kpi-row { display: flex; gap: 12px; margin-bottom: 8px; flex-wrap: wrap; }
.kpi { flex:1; min-width:130px; background:#fff; border-radius:12px; border:1.5px solid #ececec; padding:14px 16px; }
.kpi-label { font-size:10px; color:#aaa; font-weight:600; text-transform:uppercase; letter-spacing:.06em; margin-bottom:5px; }
.kpi-value { font-size:26px; font-weight:700; line-height:1; margin-bottom:3px; }
.kpi-sub   { font-size:11px; color:#aaa; }
.c-blue   { color:#2563eb; }
.c-green  { color:#16a34a; }
.c-orange { color:#d97706; }
.c-red    { color:#dc2626; }
.c-purple { color:#7c3aed; }
.c-gray   { color:#374151; }

.insight-box {
    background:#fff; border-radius:12px; border:1.5px solid #e5e7eb;
    padding:16px 18px; margin-bottom:10px;
}
.insight-box h4 { font-size:13px; font-weight:700; color:#111; margin:0 0 4px 0; }
.insight-box p  { font-size:12px; color:#666; margin:0; line-height:1.5; }

.flag-card {
    background:#fff3f3; border:1.5px solid #fca5a5;
    border-radius:12px; padding:14px 16px; margin-bottom:10px;
}
.flag-card h4 { font-size:13px; font-weight:700; color:#b91c1c; margin:0 0 4px 0; }
.flag-card p  { font-size:12px; color:#666; margin:0; line-height:1.5; }

.badge { display:inline-block; font-size:10px; font-weight:700; padding:2px 9px; border-radius:20px; margin-left:6px; }
.badge-high     { background:#fee2e2; color:#b91c1c; }
.badge-medium   { background:#fef9c3; color:#a16207; }
.badge-low      { background:#dcfce7; color:#15803d; }
.badge-critical { background:#4c1d95; color:#fff; }
.badge-acc      { background:#dcfce7; color:#15803d; }
.badge-part     { background:#fef9c3; color:#a16207; }
.badge-not      { background:#fee2e2; color:#b91c1c; }

.divider { border:none; border-top:1.5px solid #f0f0f0; margin:28px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

msmes = pd.DataFrame([
    {"name":"Han Jim Marketing Corporation", "province":"Iloilo",  "sector":"Manufacturing","org_type":"Corporation",          "msme_type":"Small",  "education":"College Graduate","year_est":2007,"assistance":1843245,"sales_s1_2024":4536000, "sales_s2_2024":4900500, "emp_latest":19, "lat":10.6866,       "lon":122.5151,      "refund_total":1843245,"refund_paid":230405.63},
    {"name":"SJL Corporation",               "province":"Iloilo",  "sector":"Services",    "org_type":"Corporation",          "msme_type":"Medium", "education":"College Graduate","year_est":2019,"assistance":4881600,"sales_s1_2024":1625000, "sales_s2_2024":2080000, "emp_latest":36, "lat":10.6932,       "lon":122.5467,      "refund_total":4881600,"refund_paid":610200},
    {"name":"Filbake Food Corporation",      "province":"Aklan",   "sector":"Manufacturing","org_type":"Corporation",          "msme_type":"Medium", "education":"College Graduate","year_est":1986,"assistance":1253933,"sales_s1_2024":32400000,"sales_s2_2024":34500000,"emp_latest":200,"lat":11.67844349,    "lon":122.3604815,   "refund_total":1253933,"refund_paid":156741.63},
    {"name":"Honore Cafe",                   "province":"Aklan",   "sector":"Manufacturing","org_type":"Single Proprietorship","msme_type":"Micro",  "education":"N/A",            "year_est":2010,"assistance":517000, "sales_s1_2024":3207600, "sales_s2_2024":3384500, "emp_latest":3,  "lat":11.69602189,   "lon":122.3705478,   "refund_total":517000, "refund_paid":459552},
    {"name":"Queen's Bakeshop",              "province":"Antique", "sector":"Manufacturing","org_type":"Single Proprietorship","msme_type":"Micro",  "education":"N/A",            "year_est":2005,"assistance":315000, "sales_s1_2024":324000,  "sales_s2_2024":366500,  "emp_latest":7,  "lat":10.786694529808,"lon":122.017570565924,"refund_total":315000, "refund_paid":39375},
])

# Refund metrics
msmes["refund_balance"] = msmes["refund_total"] - msmes["refund_paid"]
msmes["refund_pct"]     = (msmes["refund_paid"] / msmes["refund_total"] * 100).round(1)

# Sales growth
msmes["sales_growth_pct"] = ((msmes["sales_s2_2024"] - msmes["sales_s1_2024"]) / msmes["sales_s1_2024"] * 100).round(1)
msmes["sales_latest"]     = msmes["sales_s2_2024"]

# Project completion risk scoring
def score(row):
    s = 0
    if row["refund_pct"] < 15:  s += 4
    elif row["refund_pct"] < 40: s += 2
    else:                         s += 1
    if row["msme_type"] == "Micro":  s += 3
    elif row["msme_type"] == "Small": s += 1
    if row["sales_latest"] < 500000:   s += 3
    elif row["sales_latest"] < 3000000: s += 1
    return s

msmes["d_score"] = msmes.apply(score, axis=1)
def risk_label(s):
    if s >= 7: return "Critical"
    if s >= 5: return "High"
    if s >= 3: return "Medium"
    return "Low"
msmes["risk"] = msmes["d_score"].apply(risk_label)

# Impact assessment data (quantifiable verdicts per MSME per semester)
impact = pd.DataFrame([
    # Honore Cafe S2 2021
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2021","verdict":"Accomplished"},
    # Honore Cafe S1 2024
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S1 2024","verdict":"Accomplished"},
    # Honore Cafe S2 2024
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Not accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Honore Cafe","semester":"S2 2024","verdict":"Accomplished"},
    # Han Jim S1 2024
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    # Han Jim S2 2024
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Partially accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Han Jim Marketing Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # SJL S1 2024
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S1 2024","verdict":"Accomplished"},
    # SJL S2 2024
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"SJL Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # Filbake S1 2023
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2023","verdict":"Accomplished"},
    # Filbake S2 2023
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2023","verdict":"Accomplished"},
    # Filbake S1 2024
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S1 2024","verdict":"Accomplished"},
    # Filbake S2 2024
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Filbake Food Corporation","semester":"S2 2024","verdict":"Accomplished"},
    # Queen's S1 2024
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Partially accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S1 2024","verdict":"Accomplished"},
    # Queen's S2 2024
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
    {"msme":"Queen's Bakeshop","semester":"S2 2024","verdict":"Accomplished"},
])

# Merge risk into impact
impact = impact.merge(msmes[["name","province","sector","org_type","msme_type","risk"]], left_on="msme", right_on="name", how="left").drop(columns="name")

# Semester order for charts
SEM_ORDER = ["S2 2021","S1 2023","S2 2023","S1 2024","S2 2024"]

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTED METRICS
# ══════════════════════════════════════════════════════════════════════════════

total_msmes   = len(msmes)
total_outputs = len(impact)
acc_count     = (impact["verdict"] == "Accomplished").sum()
part_count    = (impact["verdict"] == "Partially accomplished").sum()
not_count     = (impact["verdict"] == "Not accomplished").sum()
acc_pct       = round(acc_count / total_outputs * 100, 1)
at_risk       = msmes[msmes["risk"].isin(["High","Critical"])]["name"].tolist()
compliant     = msmes[~msmes["risk"].isin(["High","Critical"])]["name"].tolist()

# MSMEs underperforming in impact AND flagged high risk
msme_acc_rate = impact.groupby("msme").apply(lambda x: (x["verdict"]=="Accomplished").sum()/len(x)*100).reset_index()
msme_acc_rate.columns = ["msme","acc_rate"]
msme_acc_rate = msme_acc_rate.merge(msmes[["name","risk","sector","province","org_type"]], left_on="msme", right_on="name", how="left")
dual_flag = msme_acc_rate[(msme_acc_rate["acc_rate"] < 60) & (msme_acc_rate["risk"].isin(["High","Critical"]))]

# Semester trend
sem_trend = impact.groupby("semester").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
sem_trend.columns = ["semester","acc_pct"]
sem_trend["semester"] = pd.Categorical(sem_trend["semester"], categories=SEM_ORDER, ordered=True)
sem_trend = sem_trend.sort_values("semester")

# Province avg risk score
prov_risk = msmes.groupby("province").agg(avg_score=("d_score","mean"), count=("name","count")).reset_index()

# Sector comparison
sector_impact = impact.groupby("sector").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
sector_impact.columns = ["sector","acc_rate"]
sector_risk = msmes.groupby("sector")["d_score"].mean().reset_index()
sector_risk.columns = ["sector","avg_risk_score"]
sector_combined = sector_impact.merge(sector_risk, on="sector")

# ══════════════════════════════════════════════════════════════════════════════
# EXTRA COMPUTED METRICS FOR NEW LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# Priority cases = MSMEs both underperforming (accomplishment) AND flagged High/Critical risk
priority_df   = msme_acc_rate[(msme_acc_rate["acc_rate"] < 60) & (msme_acc_rate["risk"].isin(["High","Critical"]))]
priority_ct   = len(priority_df)

# If nothing meets the strict dual-flag rule, fall back to High/Critical risk MSMEs so the
# "requires immediate intervention" table is never empty when there ARE risky MSMEs.
if priority_ct == 0:
    priority_df = msme_acc_rate[msme_acc_rate["risk"].isin(["High","Critical"])]
    priority_ct = len(priority_df)

# Areas Requiring Attention: combine Province + Sector rankings into one "top 10" list,
# ranked by average completion risk score (highest risk first).
prov_area = msmes.groupby("province").agg(
    avg_risk_score=("d_score","mean"),
    msme_count=("name","count"),
    high_risk_count=("risk", lambda x: x.isin(["High","Critical"]).sum()),
).reset_index().rename(columns={"province":"area"})
prov_area["area_type"] = "Province"

# Accomplishment rate by province / sector, computed straight from `impact` for accuracy
prov_acc = impact.groupby("province").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
prov_acc.columns = ["area","acc_rate"]
prov_area = prov_area.merge(prov_acc, on="area", how="left")

sect_area = msmes.groupby("sector").agg(
    avg_risk_score=("d_score","mean"),
    msme_count=("name","count"),
    high_risk_count=("risk", lambda x: x.isin(["High","Critical"]).sum()),
).reset_index().rename(columns={"sector":"area"})
sect_area["area_type"] = "Sector"
sect_acc = impact.groupby("sector").apply(lambda x: round((x["verdict"]=="Accomplished").sum()/len(x)*100,1)).reset_index()
sect_acc.columns = ["area","acc_rate"]
sect_area = sect_area.merge(sect_acc, on="area", how="left")

areas_attention = pd.concat([prov_area, sect_area], ignore_index=True)
areas_attention = areas_attention.sort_values("avg_risk_score", ascending=False).head(10).reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="page-title">Program Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">DOST SETUP 4.0 iFund Program — Region VI &nbsp;·&nbsp; Aggregate view across all enrolled MSMEs</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════

risk_counts = msmes["risk"].value_counts()
high_ct     = risk_counts.get("High", 0) + risk_counts.get("Critical", 0)

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-label">Total MSMEs</div>
    <div class="kpi-value c-blue">{total_msmes}</div>
    <div class="kpi-sub">Enrolled · Region VI</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">High Risk</div>
    <div class="kpi-value c-red">{high_ct}</div>
    <div class="kpi-sub">High or Critical completion risk</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Accomplishment</div>
    <div class="kpi-value c-green">{acc_pct}%</div>
    <div class="kpi-sub">{acc_count} of {total_outputs} outputs</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Priority Cases</div>
    <div class="kpi-value c-orange">{priority_ct}</div>
    <div class="kpi-sub">Needing immediate intervention</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — RISK DISTRIBUTION (DONUT)  +  PROGRAM PERFORMANCE (STACKED BAR)
# ══════════════════════════════════════════════════════════════════════════════

col_donut, col_stack = st.columns([1, 1.4])

with col_donut:
    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
    risk_df = msmes["risk"].value_counts().reset_index()
    risk_df.columns = ["Risk Tier", "Count"]
    risk_order = ["Critical","High","Medium","Low"]
    risk_df["Risk Tier"] = pd.Categorical(risk_df["Risk Tier"], categories=risk_order, ordered=True)
    risk_df = risk_df.sort_values("Risk Tier")

    fig_donut = px.pie(
        risk_df, names="Risk Tier", values="Count",
        hole=0.6,
        color="Risk Tier",
        color_discrete_map={"Critical":"#4c1d95","High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"},
    )
    fig_donut.update_traces(
        textinfo="label+percent",
        textfont_size=11,
        marker=dict(line=dict(color="#fff", width=2)),
    )
    fig_donut.update_layout(
        height=300,
        margin=dict(t=10,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font_size=10),
        annotations=[dict(text=f"{total_msmes}<br>MSMEs", x=0.5, y=0.5, font_size=14, showarrow=False)],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_stack:
    st.markdown('<div class="section-title">Program Performance</div>', unsafe_allow_html=True)
    msme_rates = impact.groupby("msme")["verdict"].value_counts(normalize=True).mul(100).round(1).unstack(fill_value=0).reset_index()
    for col in ["Accomplished","Partially accomplished","Not accomplished"]:
        if col not in msme_rates.columns:
            msme_rates[col] = 0
    msme_rates = msme_rates.sort_values("Accomplished", ascending=True)

    fig_stack = go.Figure()
    fig_stack.add_trace(go.Bar(name="Accomplished",           y=msme_rates["msme"], x=msme_rates["Accomplished"],           orientation="h", marker_color="#22c55e"))
    fig_stack.add_trace(go.Bar(name="Partially accomplished", y=msme_rates["msme"], x=msme_rates["Partially accomplished"], orientation="h", marker_color="#f59e0b"))
    fig_stack.add_trace(go.Bar(name="Not accomplished",       y=msme_rates["msme"], x=msme_rates["Not accomplished"],       orientation="h", marker_color="#ef4444"))
    fig_stack.update_layout(
        barmode="stack",
        height=300,
        margin=dict(t=10,b=10,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
        xaxis=dict(ticksuffix="%", range=[0,100]),
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=10),
    )
    st.plotly_chart(fig_stack, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — AREAS REQUIRING ATTENTION (TOP 10 PROVINCES / SECTORS)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Areas Requiring Attention — Top Provinces &amp; Sectors</div>', unsafe_allow_html=True)

fig_areas = px.bar(
    areas_attention.sort_values("avg_risk_score", ascending=True),
    x="avg_risk_score", y="area", orientation="h",
    color="area_type",
    color_discrete_map={"Province":"#6366f1","Sector":"#f59e0b"},
    text="avg_risk_score",
    hover_data={"msme_count":True, "high_risk_count":True, "acc_rate":":.1f", "area_type":True},
    labels={"avg_risk_score":"Avg Completion Risk Score","area":"","area_type":"Type"},
)
fig_areas.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig_areas.update_layout(
    height=320,
    margin=dict(t=20,b=10,l=0,r=20),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafafa",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=10),
)
st.plotly_chart(fig_areas, use_container_width=True)
st.caption("💡 Ranked by average completion risk score, highest first · combines both province-level and sector-level views.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — MSMEs REQUIRING IMMEDIATE INTERVENTION (INTERACTIVE TABLE)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">MSMEs Requiring Immediate Intervention</div>', unsafe_allow_html=True)

intervention_df = priority_df.merge(
    msmes[["name","refund_pct","sales_growth_pct","assistance"]],
    left_on="msme", right_on="name", how="left"
)[["msme","province","sector","org_type","risk","acc_rate","refund_pct","sales_growth_pct","assistance"]]
intervention_df = intervention_df.rename(columns={
    "msme":"MSME", "province":"Province", "sector":"Sector", "org_type":"Org Type",
    "risk":"Risk", "acc_rate":"Accomplishment %", "refund_pct":"Refund Paid %",
    "sales_growth_pct":"Sales Growth %", "assistance":"Assistance (PHP)",
}).sort_values("Accomplishment %", ascending=True).reset_index(drop=True)

if len(intervention_df) > 0:
    st.dataframe(
        intervention_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk": st.column_config.TextColumn("Risk"),
            "Accomplishment %": st.column_config.ProgressColumn(
                "Accomplishment %", min_value=0, max_value=100, format="%.1f%%"
            ),
            "Refund Paid %": st.column_config.ProgressColumn(
                "Refund Paid %", min_value=0, max_value=100, format="%.1f%%"
            ),
            "Sales Growth %": st.column_config.NumberColumn("Sales Growth %", format="%.1f%%"),
            "Assistance (PHP)": st.column_config.NumberColumn("Assistance (PHP)", format="₱%d"),
        },
    )
    st.caption(f"⚠️ {len(intervention_df)} MSME(s) flagged — underperforming in outputs and/or classified High/Critical risk of not completing the project. Table is sortable by clicking any column header.")
else:
    st.markdown("""
<div class="insight-box">
  <h4>✅ No MSMEs currently require immediate intervention</h4>
  <p>No MSME is simultaneously underperforming in outputs and classified as High/Critical risk of not completing the project.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;font-size:11px;color:#ccc;">DOST-VI SETUP 4.0 iFund Program · Region VI · ASENXO Program Insights</div>', unsafe_allow_html=True)
