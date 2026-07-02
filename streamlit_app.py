import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Global Oil Supply Chain", layout="wide")

DATA_DIR = Path(__file__).parent / "data" / "exports"

@st.cache_data
def load_data():
    df_balance = pd.read_csv(DATA_DIR / "fct_supply_balance.csv", parse_dates=["PERIOD_DATE"])
    df_balance = df_balance.sort_values("PERIOD_DATE")

    df_prod = pd.read_csv(DATA_DIR / "fct_global_production.csv")

    df_cushing_all = pd.read_csv(DATA_DIR / "fct_storage_cushing.csv", parse_dates=["PERIOD_DATE"])
    df_cushing = df_cushing_all[df_cushing_all["DUOAREA"] == "YCUOK"].sort_values("PERIOD_DATE")

    df_grade = pd.read_csv(DATA_DIR / "fct_crude_imports_by_grade.csv", parse_dates=["PERIOD_DATE"])

    df_moves = pd.read_csv(DATA_DIR / "fct_interregional_movements.csv", parse_dates=["PERIOD_DATE"])

    return df_balance, df_prod, df_cushing, df_grade, df_moves

df_balance, df_prod, df_cushing, df_grade, df_moves = load_data()

PADD_NAMES = {
    "R10": "PADD 1 - East Coast", "R20": "PADD 2 - Midwest",
    "R30": "PADD 3 - Gulf Coast", "R40": "PADD 4 - Rocky Mtn",
    "R50": "PADD 5 - West Coast",
}

def style_heatmap(df, low_color=(255, 255, 204), high_color=(189, 0, 38)):
    numeric = df.astype(float)
    vmin, vmax = numeric.min().min(), numeric.max().max()

    def cell_style(v):
        if pd.isna(v):
            return ""
        frac = 0.0 if vmax == vmin else (v - vmin) / (vmax - vmin)
        frac = min(max(frac, 0.0), 1.0)
        r = int(low_color[0] + frac * (high_color[0] - low_color[0]))
        g = int(low_color[1] + frac * (high_color[1] - low_color[1]))
        b = int(low_color[2] + frac * (high_color[2] - low_color[2]))
        return f"background-color: rgb({r},{g},{b})"

    return numeric.apply(lambda col: col.map(cell_style))

def latest_and_delta(df, date_col, value_col):
    d = df.dropna(subset=[value_col]).sort_values(date_col)
    if len(d) < 2:
        return None, None
    latest, prior = d[value_col].iloc[-1], d[value_col].iloc[-2]
    return latest, latest - prior

st.title("Global Oil Supply Chain & Infrastructure Dashboard")
st.caption("Data source: U.S. Energy Information Administration (EIA) Open Data API")

k1, k2, k3, k4 = st.columns(4)

v, d = latest_and_delta(df_cushing, "PERIOD_DATE", "STOCKS_MBBL")
k1.metric("Cushing, OK Stocks (MBBL)", f"{v:,.0f}" if v else "N/A", f"{d:+,.0f}" if d else None)

v, d = latest_and_delta(df_balance, "PERIOD_DATE", "ENDING_STOCKS_MBBL")
k2.metric("US Ending Stocks (MBBL)", f"{v:,.0f}" if v else "N/A", f"{d:+,.0f}" if d else None)

v, d = latest_and_delta(df_balance, "PERIOD_DATE", "FIELD_PRODUCTION_MBBL")
k3.metric("US Field Production (MBBL)", f"{v:,.0f}" if v else "N/A", f"{d:+,.0f}" if d else None)

df_world = df_prod[df_prod["COUNTRY_REGION_ID"] == "WORL"].sort_values("PERIOD_YEAR")
v, d = latest_and_delta(df_world, "PERIOD_YEAR", "PRODUCTION_TBPD")
k4.metric("World Production (TBPD)", f"{v:,.0f}" if v else "N/A", f"{d:+,.0f}" if d else None)

st.divider()

st.sidebar.header("Filters")
min_year = int(df_balance["PERIOD_DATE"].dt.year.min())
max_year = int(df_balance["PERIOD_DATE"].dt.year.max())
year_range = st.sidebar.slider("Supply balance year range", min_year, max_year, (max(min_year, max_year - 15), max_year))

countries_available = sorted(df_prod[df_prod["COUNTRY_REGION_ID"] != "WORL"]["COUNTRY_REGION_NAME"].unique())
default_countries = [c for c in ["Saudi Arabia", "United States", "Russia", "China"] if c in countries_available]
selected_countries = st.sidebar.multiselect("Compare countries (Production tab)", countries_available, default=default_countries)

tab1, tab2, tab3, tab4 = st.tabs([
    "National Supply Balance", "Global Production", "Storage", "Trade Flows"
])

with tab1:
    st.subheader("U.S. Crude Oil Supply & Disposition Balance")
    mask = (df_balance["PERIOD_DATE"].dt.year >= year_range[0]) & (df_balance["PERIOD_DATE"].dt.year <= year_range[1])
    df_b = df_balance[mask]

    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df_b.set_index("PERIOD_DATE")[["FIELD_PRODUCTION_MBBL", "REFINERY_NET_INPUT_MBBL"]])
    with col2:
        st.line_chart(df_b.set_index("PERIOD_DATE")[["ENDING_STOCKS_MBBL"]])
    st.dataframe(df_b.tail(12), use_container_width=True)

with tab2:
    st.subheader("Crude Oil Production by Country (Top 10, Most Recent Year)")
    df_prod_c = df_prod[df_prod["COUNTRY_REGION_ID"] != "WORL"]
    latest_year = df_prod_c["PERIOD_YEAR"].max()
    df_latest = df_prod_c[df_prod_c["PERIOD_YEAR"] == latest_year].sort_values("PRODUCTION_TBPD", ascending=False).head(10)
    st.bar_chart(df_latest.set_index("COUNTRY_REGION_NAME")["PRODUCTION_TBPD"])
    st.dataframe(df_latest, use_container_width=True)

    st.subheader("Production Trend Comparison")
    if selected_countries:
        df_sel = df_prod_c[df_prod_c["COUNTRY_REGION_NAME"].isin(selected_countries)]
        pivot = df_sel.pivot_table(index="PERIOD_YEAR", columns="COUNTRY_REGION_NAME", values="PRODUCTION_TBPD")
        st.line_chart(pivot)
    else:
        st.info("Select one or more countries in the sidebar to compare production trends.")

    st.subheader("Production Intensity Heatmap (Top 10 Countries, Last 10 Years)")
    top10 = df_latest["COUNTRY_REGION_NAME"].tolist()
    recent_years = sorted(df_prod_c["PERIOD_YEAR"].unique())[-10:]
    heat_df = df_prod_c[df_prod_c["COUNTRY_REGION_NAME"].isin(top10) & df_prod_c["PERIOD_YEAR"].isin(recent_years)]
    heat_pivot = heat_df.pivot_table(index="COUNTRY_REGION_NAME", columns="PERIOD_YEAR", values="PRODUCTION_TBPD")
    styled = heat_pivot.style.apply(lambda _: style_heatmap(heat_pivot, low_color=(255, 255, 204), high_color=(189, 0, 38)), axis=None).format("{:,.0f}")
    st.dataframe(styled, use_container_width=True)

with tab3:
    st.subheader("Cushing, OK Crude Oil Storage (WTI Delivery Point)")
    st.line_chart(df_cushing.set_index("PERIOD_DATE")["STOCKS_MBBL"])

with tab4:
    st.subheader("U.S. Crude Oil Imports by Origin Country & Grade (Latest 12 Months)")
    df_grade_cty = df_grade[df_grade["ORIGIN_TYPE"] == "CTY"]
    cutoff = df_grade_cty["PERIOD_DATE"].max() - pd.DateOffset(months=12)
    df_recent = df_grade_cty[df_grade_cty["PERIOD_DATE"] > cutoff]
    grouped = df_recent.groupby(["ORIGIN_NAME", "GRADE_NAME"], as_index=False)["QUANTITY_MBBL"].sum()
    grouped = grouped[grouped["QUANTITY_MBBL"] > 0]
    top_origins = grouped.groupby("ORIGIN_NAME")["QUANTITY_MBBL"].sum().sort_values(ascending=False).head(10).index
    grouped_top = grouped[grouped["ORIGIN_NAME"].isin(top_origins)]
    pivot_grade = grouped_top.pivot_table(index="ORIGIN_NAME", columns="GRADE_NAME", values="QUANTITY_MBBL", fill_value=0)
    st.bar_chart(pivot_grade)

    st.subheader("Interregional Crude Oil Movements (Most Recent Year)")
    df_moves_clean = df_moves.dropna(subset=["MOVEMENT_MBBL"])
    latest_move_year = df_moves_clean["PERIOD_DATE"].dt.year.max()
    df_moves_recent = df_moves_clean[df_moves_clean["PERIOD_DATE"].dt.year == latest_move_year]
    flow = df_moves_recent.groupby(["ORIGIN_PADD", "DESTINATION_PADD"], as_index=False)["MOVEMENT_MBBL"].sum()
    flow = flow[flow["ORIGIN_PADD"] != flow["DESTINATION_PADD"]]
    flow["origin_label"] = flow["ORIGIN_PADD"].map(PADD_NAMES).fillna(flow["ORIGIN_PADD"])
    flow["dest_label"] = flow["DESTINATION_PADD"].map(PADD_NAMES).fillna(flow["DESTINATION_PADD"])
    flow_matrix = flow.pivot_table(index="origin_label", columns="dest_label", values="MOVEMENT_MBBL", fill_value=0)
    styled_flow = flow_matrix.style.apply(lambda _: style_heatmap(flow_matrix, low_color=(239, 243, 255), high_color=(8, 48, 107)), axis=None).format("{:,.0f}")
    st.dataframe(styled_flow, use_container_width=True)
