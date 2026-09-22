import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ====================================================
# PAGE CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="Maharashtra Smart Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================================
# CUSTOM CSS — THEME / BEAUTIFICATION
# ====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App background */
.stApp {
    background: linear-gradient(180deg, #f4f9f4 0%, #eef6ef 100%);
}

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero banner */
.hero-banner {
    background: linear-gradient(120deg, #1b5e20 0%, #2e7d32 45%, #66bb6a 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    box-shadow: 0 10px 30px rgba(27, 94, 32, 0.25);
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    font-size: 1.02rem;
    color: rgba(255,255,255,0.9);
    margin-top: 0.4rem;
}
.hero-tags span {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: white;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    margin-right: 8px;
    margin-top: 12px;
    backdrop-filter: blur(4px);
}

/* Section headers */
.section-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: #1b5e20;
    margin-top: 0.4rem;
    margin-bottom: 0.8rem;
    padding-left: 12px;
    border-left: 5px solid #66bb6a;
}

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 4px 18px rgba(27, 94, 32, 0.08);
    border: 1px solid #e3f0e4;
    text-align: left;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(27, 94, 32, 0.15);
}
.kpi-label {
    font-size: 0.82rem;
    color: #5a7a5c;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.kpi-value {
    font-family: 'Poppins', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #1b5e20;
    margin-top: 4px;
}
.kpi-icon {
    font-size: 1.6rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%);
}
section[data-testid="stSidebar"] * {
    color: #f1f8f1 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #66bb6a !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: #e3f0e4;
    padding: 6px;
    border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    color: #1b5e20;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background-color: #2e7d32 !important;
    color: white !important;
}

.chart-card {
    background: white;
    border-radius: 16px;
    padding: 1rem 1.2rem 0.4rem 1.2rem;
    box-shadow: 0 4px 16px rgba(27,94,32,0.07);
    border: 1px solid #e3f0e4;
    margin-bottom: 1.2rem;
}

hr {
    border-top: 1px solid #d7e8d8;
}
</style>
""", unsafe_allow_html=True)


# ====================================================
# REAL GEOGRAPHICAL COORDINATES LOOKUP
# ====================================================

MAHARASHTRA_COORDINATES = {
    "ahmednagar": (19.0952, 74.7496),
    "ahilyanagar": (19.0952, 74.7496),
    "akola": (20.7002, 77.0082),
    "amravati": (20.9374, 77.7796),
    "aurangabad": (19.8762, 75.3433),
    "chhatrapati sambhajinagar": (19.8762, 75.3433),
    "beed": (18.9891, 75.7601),
    "bhandara": (21.1663, 79.6519),
    "buldhana": (20.5293, 76.1809),
    "chandrapur": (19.9615, 79.2961),
    "dhule": (20.9042, 74.7749),
    "gadchiroli": (20.1809, 80.0021),
    "gondia": (21.4602, 80.1922),
    "hingoli": (19.7147, 77.1497),
    "jalgaon": (21.0077, 75.5626),
    "jalna": (19.8410, 75.8864),
    "kolhapur": (16.7050, 74.2433),
    "latur": (18.4088, 76.5604),
    "mumbai city": (18.9388, 72.8354),
    "mumbai suburban": (19.1176, 72.8697),
    "mumbai": (19.0760, 72.8777),
    "nagpur": (21.1458, 79.0882),
    "nanded": (19.1383, 77.3210),
    "nandurbar": (21.3667, 74.2500),
    "nashik": (20.0059, 73.7910),
    "osmanabad": (18.1818, 76.0419),
    "dharashiv": (18.1818, 76.0419),
    "palghar": (19.6970, 72.7650),
    "parbhani": (19.2704, 76.7601),
    "pune": (18.5204, 73.8567),
    "raigad": (18.5158, 73.1822),
    "ratnagiri": (16.9902, 73.3120),
    "sangli": (16.8524, 74.5815),
    "satara": (17.6805, 74.0183),
    "sindhudurg": (16.3616, 73.6103),
    "solapur": (17.6599, 75.9064),
    "thane": (19.2183, 72.9781),
    "wardha": (20.7453, 78.6022),
    "washim": (20.1097, 77.1333),
    "yavatmal": (20.3888, 78.1204),
}

MAHARASHTRA_CENTER = {"lat": 19.5, "lon": 76.0}

# Distinct, high-contrast palette for all crops
VIBRANT_CROP_COLORS = [
    "#E63946", "#2A9D8F", "#E76F51", "#457B9D", "#F4A261", 
    "#9B5DE5", "#00BBF9", "#00F5D4", "#F15BB5", "#FEE440",
    "#3A86FF", "#8338EC", "#FF006E", "#FB5607", "#06D6A0"
]


def attach_geo(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Attach latitude and longitude coordinates based on dataset district name."""
    d = dataframe.copy()
    key = d["district"].astype(str).str.strip().str.lower()
    coords = key.map(MAHARASHTRA_COORDINATES)
    d["_lat"] = coords.map(lambda c: c[0] if isinstance(c, tuple) else None)
    d["_lon"] = coords.map(lambda c: c[1] if isinstance(c, tuple) else None)
    return d


# ====================================================
# LOAD DATA
# ====================================================

DATA_PATH = "data/raw/agriculture_data.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in data.columns:
        data = data.drop(columns=["Unnamed: 0"])
    return attach_geo(data)


df = load_data()


# ====================================================
# HERO HEADER
# ====================================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🌾 Maharashtra Smart Agriculture Analytics</div>
    <div class="hero-subtitle">Big Data Analytics using Hadoop, PySpark and Machine Learning</div>
    <div class="hero-tags">
        <span>🗺️ Region-wise Crop Map</span>
        <span>📊 Live Filters</span>
        <span>🌧️ Rainfall Insights</span>
        <span>🌱 Soil Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ====================================================
# SIDEBAR FILTERS
# ====================================================

ALL_CROPS = sorted(df["crop"].unique())
ALL_REGIONS = sorted(df["region"].unique())

if "crop_filter" not in st.session_state:
    st.session_state["crop_filter"] = ALL_CROPS
if "region_filter" not in st.session_state:
    st.session_state["region_filter"] = ALL_REGIONS

st.sidebar.markdown("## 🔎 Filters")
st.sidebar.markdown("Filter all charts and maps across the dataset.")
st.sidebar.markdown("---")

qc1, qc2 = st.sidebar.columns(2)
with qc1:
    if st.button("✅ All Crops", use_container_width=True):
        st.session_state["crop_filter"] = ALL_CROPS
with qc2:
    if st.button("♻️ Reset All", use_container_width=True):
        st.session_state["crop_filter"] = ALL_CROPS
        st.session_state["region_filter"] = ALL_REGIONS

selected_crop = st.sidebar.multiselect(
    "🌾 Select Crop",
    options=ALL_CROPS,
    key="crop_filter"
)

selected_region = st.sidebar.multiselect(
    "🗺️ Select Region",
    options=ALL_REGIONS,
    key="region_filter"
)

if "year" in df.columns:
    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    selected_years = st.sidebar.slider(
        "📅 Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max)
    )
else:
    selected_years = None

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit, Plotly, PySpark & Hadoop")

if not selected_crop or not selected_region:
    st.sidebar.warning("Select at least one crop and one region to see results.")

filtered_df = df[
    (df["crop"].isin(selected_crop)) &
    (df["region"].isin(selected_region))
]

if selected_years is not None:
    filtered_df = filtered_df[
        (filtered_df["year"] >= selected_years[0]) &
        (filtered_df["year"] <= selected_years[1])
    ]


# ====================================================
# KPI SECTION
# ====================================================

def kpi_card(label, value, icon, delta=None):
    delta_html = ""
    if delta is not None:
        arrow = "▲" if delta >= 0 else "▼"
        color = "#2e7d32" if delta >= 0 else "#c62828"
        delta_html = f'<div style="color:{color}; font-size:0.78rem; font-weight:600; margin-top:2px;">{arrow} {abs(delta):.1f}% vs previous year</div>'
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


prod_delta = None
if "year" in df.columns and selected_years is not None and selected_crop and selected_region:
    base_df = df[df["crop"].isin(selected_crop) & df["region"].isin(selected_region)]
    latest_year = selected_years[1]
    curr = base_df.loc[base_df["year"] == latest_year, "production_tonnes"].sum()
    prev = base_df.loc[base_df["year"] == latest_year - 1, "production_tonnes"].sum()
    if prev > 0:
        prod_delta = (curr - prev) / prev * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Records", f"{len(filtered_df):,}", "📊")

with col2:
    kpi_card("Crops Tracked", f"{filtered_df['crop'].nunique()}", "🌾")

with col3:
    avg_yield = filtered_df['yield_tonnes_ha'].mean() if len(filtered_df) else 0
    kpi_card("Avg Yield", f"{avg_yield:.2f} t/ha", "📈")

with col4:
    total_prod = filtered_df['production_tonnes'].sum() if len(filtered_df) else 0
    kpi_card("Total Production", f"{total_prod:,.0f} t", "🏭", delta=prod_delta)

st.markdown("<br>", unsafe_allow_html=True)


# ====================================================
# TABBED LAYOUT
# ====================================================

tab_map, tab_overview, tab_regional, tab_environment, tab_data = st.tabs(
    ["🗺️ Crop Map", "🌾 Crop Overview", "📍 Regional Breakdown", "🌧️ Environment & Soil", "📋 Raw Data"]
)


# ----------------------------------------------------
# TAB 1 — INTERACTIVE MAHARASHTRA CROP MAP
# ----------------------------------------------------
with tab_map:
    st.markdown('<div class="section-header">🗺️ Which Crop Grows Where in Maharashtra</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ Map Navigation Guide", expanded=False):
        st.markdown(
            "- **District-level Relative Bubble Scaling**: Inside each district, higher-producing crops render as larger bubbles, while lesser crops proportionally decrease step-by-step.\n"
            "- Colored dots in the legend indicate the specific shade for each crop.\n"
            "- Switch **map style** between bubble view, smooth density heatmap, or year-by-year animation."
        )

    map_df = filtered_df.dropna(subset=["_lat", "_lon"]).copy()

    if map_df.empty:
        st.warning("No matching geographic data found for the current filter selections.")
    else:
        ctrl1, ctrl2 = st.columns([1.3, 1])

        with ctrl1:
            view_mode = st.radio(
                "🎨 Map style",
                ["🔵 Crop Bubbles", "🔥 Density Heatmap", "▶️ Animate by Year"],
                horizontal=True,
                key="map_view_mode"
            )

        district_options = ["🌍 Full Maharashtra"] + sorted(map_df["district"].dropna().unique().tolist())
        with ctrl2:
            focus_choice = st.selectbox("🎯 Focus on", district_options, key="map_focus")

        if focus_choice == "🌍 Full Maharashtra":
            map_center, map_zoom = MAHARASHTRA_CENTER, 5.6
        else:
            coords = MAHARASHTRA_COORDINATES.get(focus_choice.strip().lower())
            if coords:
                map_center, map_zoom = {"lat": coords[0], "lon": coords[1]}, 9.2
            else:
                map_center, map_zoom = MAHARASHTRA_CENTER, 5.6

        group_cols = ["district", "region", "_lat", "_lon", "crop"]
        if "year" in map_df.columns:
            group_cols.append("year")

        map_agg = (
            map_df
            .groupby(group_cols, as_index=False)
            .agg(
                production=("production_tonnes", "sum"),
                avg_yield=("yield_tonnes_ha", "mean")
            )
        )
        map_agg["avg_yield"] = map_agg["avg_yield"].round(2)

        # Scale bubbles proportionally within each district and disperse them around coordinates
        def process_district_crop_bubbles(df_in, lat_col="_lat", lon_col="_lon", group_by="district"):
            df_out = df_in.copy()
            # Sort each district by production descending so larger bubbles are calculated sequentially
            df_out = df_out.sort_values([group_by, "production"], ascending=[True, False]).reset_index(drop=True)
            
            df_out["crop_idx"] = df_out.groupby(group_by).cumcount()
            df_out["crop_count"] = df_out.groupby(group_by)[lat_col].transform("count")
            
            # Position dots evenly in an orbit around district centroid
            angle = (2 * np.pi * df_out["crop_idx"]) / df_out["crop_count"]
            radius = np.where(df_out["crop_count"] > 1, 0.088, 0.0)
            
            df_out["plot_lat"] = df_out[lat_col] + radius * np.sin(angle)
            df_out["plot_lon"] = df_out[lon_col] + radius * np.cos(angle)
            
            # Incremental size calculation: highest crop in district gets top size (~34px), others scale down
            d_max = df_out.groupby(group_by)["production"].transform("max")
            d_min = df_out.groupby(group_by)["production"].transform("min")
            
            local_ratio = np.where(
                d_max > d_min,
                (df_out["production"] - d_min) / (d_max - d_min),
                1.0
            )
            
            # Min bubble size: 14px, Max bubble size: 36px in each region
            df_out["display_size"] = np.where(
                df_out["crop_count"] > 1,
                14 + 22 * (local_ratio ** 0.5),
                24
            )
            return df_out

        common_layout = dict(
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(
                title=dict(text="<b>🌾 Crops (Color Key)</b>", font=dict(size=12, color="#1b5e20")),
                itemsizing="constant",
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="#c8e6c9",
                borderwidth=1.5,
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="right",
                x=0.98
            ),
            font=dict(family="Inter, sans-serif"),
            mapbox=dict(center=map_center, zoom=map_zoom),
            uirevision=f"view-{focus_choice}-{view_mode}",
        )

        if view_mode == "🔵 Crop Bubbles":
            plot_df = map_agg.groupby(["district", "region", "_lat", "_lon", "crop"], as_index=False).agg(
                production=("production", "sum"), avg_yield=("avg_yield", "mean")
            )
            plot_df["avg_yield"] = plot_df["avg_yield"].round(2)
            plot_df = process_district_crop_bubbles(plot_df)

            fig_map = px.scatter_mapbox(
                plot_df, 
                lat="plot_lat", 
                lon="plot_lon", 
                color="crop", 
                size="display_size", 
                size_max=36,
                opacity=0.92,
                hover_name="district",
                hover_data={"plot_lat": False, "plot_lon": False, "display_size": False, "region": True, "crop": True,
                            "production": ":,.0f", "avg_yield": True},
                labels={"region": "Region", "production": "Production (t)", "avg_yield": "Avg Yield (t/ha)", "crop": "Crop"},
                color_discrete_sequence=VIBRANT_CROP_COLORS,
                mapbox_style="carto-positron", 
                height=620
            )

        elif view_mode == "🔥 Density Heatmap":
            plot_df = map_agg.groupby(["district", "region", "_lat", "_lon"], as_index=False).agg(
                production=("production", "sum")
            )
            fig_map = px.density_mapbox(
                plot_df, lat="_lat", lon="_lon", z="production", radius=40,
                hover_name="district",
                hover_data={"_lat": False, "_lon": False, "region": True, "production": ":,.0f"},
                labels={"region": "Region", "production": "Production (t)"},
                color_continuous_scale="YlGnBu", mapbox_style="carto-positron", height=620
            )

        else:
            if "year" not in map_agg.columns:
                st.info("No `year` column found in dataset — showing static bubble map.")
                plot_df = map_agg.groupby(["district", "region", "_lat", "_lon", "crop"], as_index=False).agg(
                    production=("production", "sum"), avg_yield=("avg_yield", "mean")
                )
                plot_df = process_district_crop_bubbles(plot_df)
                fig_map = px.scatter_mapbox(
                    plot_df, lat="plot_lat", lon="plot_lon", color="crop", size="display_size", size_max=36,
                    opacity=0.92, hover_name="district",
                    hover_data={"plot_lat": False, "plot_lon": False, "display_size": False, "region": True, "crop": True,
                                "production": ":,.0f", "avg_yield": True},
                    color_discrete_sequence=VIBRANT_CROP_COLORS,
                    mapbox_style="carto-positron", height=620
                )
            else:
                plot_df = map_agg.sort_values("year")
                plot_df = process_district_crop_bubbles(plot_df, group_by="district")
                fig_map = px.scatter_mapbox(
                    plot_df, lat="plot_lat", lon="plot_lon", color="crop", size="display_size", size_max=36,
                    opacity=0.92,
                    hover_name="district", animation_frame="year",
                    hover_data={"plot_lat": False, "plot_lon": False, "display_size": False, "region": True, "crop": True,
                                "production": ":,.0f", "avg_yield": True},
                    labels={"region": "Region", "production": "Production (t)", "avg_yield": "Avg Yield (t/ha)", "crop": "Crop"},
                    color_discrete_sequence=VIBRANT_CROP_COLORS,
                    mapbox_style="carto-positron", height=620
                )
                fig_map.layout.updatemenus[0].buttons[0].label = "▶️ Play"
                fig_map.layout.updatemenus[0].buttons[1].label = "⏸️ Pause"

        fig_map.update_layout(**common_layout)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(
            fig_map,
            use_container_width=True,
            config={
                "scrollZoom": True,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["zoomInMapbox", "zoomOutMapbox", "resetViewMapbox"],
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

        region_totals = map_df.groupby("region")["production_tonnes"].sum().sort_values(ascending=False)
        crop_totals = map_df.groupby("crop")["production_tonnes"].sum().sort_values(ascending=False)
        if len(region_totals) and len(crop_totals):
            top_region, top_region_val = region_totals.index[0], region_totals.iloc[0]
            top_crop, top_crop_val = crop_totals.index[0], crop_totals.iloc[0]
            st.markdown(f"""
            <div style="background:#e8f5e9; border-left:5px solid #2e7d32; padding:0.9rem 1.2rem;
                        border-radius:10px; margin-top:0.6rem; font-size:0.92rem; color:#1b5e20;">
                💡 <b>{top_region}</b> leads with <b>{top_region_val:,.0f} t</b> total production,
                and <b>{top_crop}</b> is the leading crop overall at <b>{top_crop_val:,.0f} t</b>
                under active filters.
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">🏆 Dominant Crop per Region</div>', unsafe_allow_html=True)
        dominant = (
            map_df.groupby(["region", "crop"], as_index=False)["production_tonnes"]
            .sum()
            .sort_values("production_tonnes", ascending=False)
            .drop_duplicates("region")
            .rename(columns={"region": "Region", "crop": "Top Crop", "production_tonnes": "Production (t)"})
        )
        dominant["Production (t)"] = dominant["Production (t)"].map(lambda x: f"{x:,.0f}")
        st.dataframe(dominant, use_container_width=True, hide_index=True)


# ----------------------------------------------------
# TAB 2 — CROP OVERVIEW
# ----------------------------------------------------
with tab_overview:
    st.markdown('<div class="section-header">🌾 Crop-wise Production</div>', unsafe_allow_html=True)

    crop_data = (
        filtered_df
        .groupby("crop", as_index=False)
        .agg(
            average_yield=("yield_tonnes_ha", "mean"),
            total_production=("production_tonnes", "sum")
        )
    )
    crop_data["average_yield"] = crop_data["average_yield"].round(2)

    fig_crop = px.bar(
        crop_data,
        x="crop",
        y="total_production",
        color="crop",
        title="Total Production by Crop",
        labels={"total_production": "Production (tonnes)", "crop": "Crop"},
        color_discrete_sequence=VIBRANT_CROP_COLORS
    )
    fig_crop.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        showlegend=False
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_crop, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "year" in filtered_df.columns:
        st.markdown('<div class="section-header">📅 Year-wise Production Trend</div>', unsafe_allow_html=True)
        year_data = (
            filtered_df
            .groupby("year", as_index=False)
            .agg(production=("production_tonnes", "sum"))
        )
        fig_year = px.line(
            year_data,
            x="year",
            y="production",
            markers=True,
            title="Agricultural Production Trend",
            color_discrete_sequence=["#2e7d32"]
        )
        fig_year.update_traces(line=dict(width=3), marker=dict(size=8))
        fig_year.update_layout(
            plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Inter, sans-serif"),
            xaxis=dict(rangeslider=dict(visible=True), title="Year")
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_year, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">⚖️ Compare Crops Side-by-Side</div>', unsafe_allow_html=True)
    st.caption("Pick up to 5 crops to compare on yield, rainfall need, soil pH and nutrients.")

    compare_crops = st.multiselect(
        "Crops to compare",
        options=sorted(filtered_df["crop"].unique()),
        default=sorted(filtered_df["crop"].unique())[:3],
        max_selections=5,
        key="compare_crops"
    )

    radar_metrics = [c for c in ["yield_tonnes_ha", "rainfall_mm", "soil_ph",
                                  "nitrogen_kg_ha", "phosphorus_kg_ha", "potassium_kg_ha"]
                      if c in filtered_df.columns]

    if compare_crops and radar_metrics:
        radar_df = (
            filtered_df[filtered_df["crop"].isin(compare_crops)]
            .groupby("crop", as_index=False)[radar_metrics]
            .mean()
        )
        norm_df = radar_df.copy()
        for m in radar_metrics:
            lo, hi = filtered_df[m].min(), filtered_df[m].max()
            norm_df[m] = 0.5 if hi == lo else (radar_df[m] - lo) / (hi - lo)

        label_map = {
            "yield_tonnes_ha": "Yield", "rainfall_mm": "Rainfall",
            "soil_ph": "Soil pH", "nitrogen_kg_ha": "Nitrogen",
            "phosphorus_kg_ha": "Phosphorus", "potassium_kg_ha": "Potassium"
        }
        theta = [label_map.get(m, m) for m in radar_metrics]

        fig_radar = go.Figure()
        palette = VIBRANT_CROP_COLORS
        for i, row in norm_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=row[radar_metrics].tolist() + [row[radar_metrics].tolist()[0]],
                theta=theta + [theta[0]],
                fill="toself",
                name=row["crop"],
                line=dict(color=palette[i % len(palette)])
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
            showlegend=True,
            font=dict(family="Inter, sans-serif"),
            height=480,
            margin=dict(t=30, b=10)
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select at least one crop above to see the comparison chart.")


# ----------------------------------------------------
# TAB 3 — REGIONAL BREAKDOWN
# ----------------------------------------------------
with tab_regional:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📍 Top Districts</div>', unsafe_allow_html=True)
        district_data = (
            filtered_df
            .groupby("district", as_index=False)
            .agg(production=("production_tonnes", "sum"))
            .sort_values("production", ascending=False)
            .head(10)
        )
        fig_district = px.bar(
            district_data,
            x="production",
            y="district",
            orientation="h",
            color="production",
            title="Top 10 Producing Districts",
            color_continuous_scale="Greens"
        )
        fig_district.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
            yaxis=dict(categoryorder="total ascending")
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_district, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">🗺️ Region Analysis</div>', unsafe_allow_html=True)
        region_data = (
            filtered_df
            .groupby("region", as_index=False)
            .agg(
                production=("production_tonnes", "sum"),
                yield_avg=("yield_tonnes_ha", "mean")
            )
        )
        fig_region = px.pie(
            region_data,
            names="region",
            values="production",
            title="Production by Region",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig_region.update_layout(font=dict(family="Inter, sans-serif"))
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_region, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------
# TAB 4 — ENVIRONMENT & SOIL
# ----------------------------------------------------
with tab_environment:
    st.markdown('<div class="section-header">🌧️ Rainfall vs Crop Yield</div>', unsafe_allow_html=True)
    fig_rainfall = px.scatter(
        filtered_df.sample(min(5000, len(filtered_df)), random_state=42) if len(filtered_df) else filtered_df,
        x="rainfall_mm",
        y="yield_tonnes_ha",
        color="crop",
        hover_data=["district", "region", "soil_ph"],
        title="Relationship Between Rainfall and Yield",
        color_discrete_sequence=VIBRANT_CROP_COLORS
    )
    fig_rainfall.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Inter, sans-serif"))
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_rainfall, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🌱 Soil & Nutrient Analysis</div>', unsafe_allow_html=True)
    soil_data = (
        filtered_df
        .groupby("crop", as_index=False)
        .agg(
            soil_ph=("soil_ph", "mean"),
            nitrogen=("nitrogen_kg_ha", "mean"),
            phosphorus=("phosphorus_kg_ha", "mean"),
            potassium=("potassium_kg_ha", "mean")
        )
    )
    soil_data = soil_data.round(2)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(soil_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------
# TAB 5 — RAW DATA
# ----------------------------------------------------
with tab_data:
    st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)

    search_term = st.text_input("🔍 Search across all columns", placeholder="e.g. Aurangabad, Maize, 2017...")

    display_df = filtered_df.drop(columns=["_lat", "_lon", "plot_lat", "plot_lon", "display_size"], errors="ignore")
    if search_term:
        mask = display_df.astype(str).apply(
            lambda col: col.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]

    st.caption(f"Showing {min(len(display_df), 200):,} of {len(display_df):,} matching rows")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(display_df.head(200), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=csv,
        file_name="maharashtra_agriculture_filtered.csv",
        mime="text/csv"
    )


# ====================================================
# FOOTER
# ====================================================

st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.caption(
    "🌾 Smart Agriculture Big Data Analytics | Hadoop + HDFS + PySpark + Spark MLlib + Streamlit + Plotly"
)