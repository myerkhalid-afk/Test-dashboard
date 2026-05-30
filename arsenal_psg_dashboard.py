from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Token & Usage Dashboard",
    page_icon="TOK",
    layout="wide",
    initial_sidebar_state="expanded",
)


COLORS = {
    "input": "#2563eb",
    "output": "#dc2626",
    "cached": "#16a34a",
    "reasoning": "#7c3aed",
    "neutral": "#64748b",
    "bg": "#f8fafc",
}


DEFAULT_DAILY = pd.DataFrame(
    [
        ["2026-05-24", 18000, 4200, 8000, 1200],
        ["2026-05-25", 26500, 6100, 14000, 2200],
        ["2026-05-26", 14200, 3500, 6000, 900],
        ["2026-05-27", 39000, 9200, 21000, 4100],
        ["2026-05-28", 22400, 5200, 11000, 1800],
        ["2026-05-29", 51500, 12800, 26000, 6000],
        ["2026-05-30", 31000, 7600, 15000, 3400],
    ],
    columns=["date", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens"],
)


def add_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.3rem;}
        .hero {
            border-radius: 10px;
            padding: 24px;
            background:
              linear-gradient(110deg, #0f172a 0%, #1d4ed8 50%, #7c3aed 100%);
            color: white;
            box-shadow: 0 12px 34px rgba(15,23,42,.22);
        }
        .hero h1 {font-size: 44px; margin: 0; letter-spacing: 0;}
        .hero p {margin: 8px 0 0 0; color: rgba(255,255,255,.82);}
        .pill {
            display:inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,.14);
            margin-right: 8px;
            font-size: 13px;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(15,23,42,.10);
            border-radius: 8px;
            padding: 13px 15px;
            background: rgba(255,255,255,.74);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def auto_refresh(enabled: bool, seconds: int) -> None:
    if enabled:
        components.html(
            f"""
            <script>
            setTimeout(function() {{
              window.parent.location.reload();
            }}, {seconds * 1000});
            </script>
            """,
            height=0,
        )


def sidebar() -> tuple[pd.DataFrame, dict]:
    st.sidebar.title("Usage Controls")
    refresh = st.sidebar.toggle("Auto-refresh", value=False)
    refresh_seconds = st.sidebar.slider("Refresh interval", 15, 300, 60, step=15)
    auto_refresh(refresh, refresh_seconds)

    st.sidebar.caption(f"Last render: {datetime.now().strftime('%H:%M:%S')}")
    st.sidebar.divider()

    uploaded = st.sidebar.file_uploader(
        "Upload usage CSV",
        type=["csv"],
        help="Expected columns: date,input_tokens,output_tokens,cached_tokens,reasoning_tokens",
    )
    if uploaded is not None:
        data = pd.read_csv(uploaded)
    else:
        data = DEFAULT_DAILY.copy()

    st.sidebar.subheader("Current Session")
    current_input = st.sidebar.number_input("Input tokens", min_value=0, value=12000, step=500)
    current_output = st.sidebar.number_input("Output tokens", min_value=0, value=2800, step=250)
    current_cached = st.sidebar.number_input("Cached tokens", min_value=0, value=4000, step=500)
    current_reasoning = st.sidebar.number_input("Reasoning tokens", min_value=0, value=1600, step=100)
    context_limit = st.sidebar.number_input("Context window", min_value=1000, value=128000, step=1000)

    st.sidebar.subheader("Pricing Assumptions")
    st.sidebar.caption("Edit these to match your model/account pricing.")
    input_rate = st.sidebar.number_input("Input $ / 1M tokens", min_value=0.0, value=1.25, step=0.25)
    output_rate = st.sidebar.number_input("Output $ / 1M tokens", min_value=0.0, value=10.00, step=0.50)
    cached_discount = st.sidebar.slider("Cached input discount", 0, 100, 75, step=5)

    settings = {
        "current_input": current_input,
        "current_output": current_output,
        "current_cached": current_cached,
        "current_reasoning": current_reasoning,
        "context_limit": context_limit,
        "input_rate": input_rate,
        "output_rate": output_rate,
        "cached_discount": cached_discount,
        "refresh": refresh,
    }
    return normalize_usage(data), settings


def normalize_usage(data: pd.DataFrame) -> pd.DataFrame:
    required = ["date", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens"]
    for col in required:
        if col not in data.columns:
            data[col] = 0
    data = data[required].copy()
    data["date"] = pd.to_datetime(data["date"]).dt.date
    numeric = required[1:]
    for col in numeric:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0).astype(int)
    data["total_tokens"] = data[numeric].sum(axis=1)
    return data.sort_values("date")


def estimate_cost(row_or_df, settings: dict):
    input_cost = (row_or_df["input_tokens"] / 1_000_000) * settings["input_rate"]
    cached_effective_rate = settings["input_rate"] * (1 - settings["cached_discount"] / 100)
    cached_cost = (row_or_df["cached_tokens"] / 1_000_000) * cached_effective_rate
    output_cost = (row_or_df["output_tokens"] / 1_000_000) * settings["output_rate"]
    return input_cost + cached_cost + output_cost


def hero(settings: dict) -> None:
    current_total = (
        settings["current_input"]
        + settings["current_output"]
        + settings["current_cached"]
        + settings["current_reasoning"]
    )
    context_pct = min(current_total / settings["context_limit"], 1.0)
    st.markdown(
        f"""
        <div class="hero">
          <span class="pill">Tokens</span>
          <span class="pill">Usage</span>
          <span class="pill">Cost Estimate</span>
          <h1>Personal AI Usage Dashboard</h1>
          <p>Track session tokens, context pressure, daily usage, cached-token savings, and estimated cost.</p>
          <p style="margin-top:14px;">Current session: <strong>{current_total:,}</strong> tokens |
          Context used: <strong>{context_pct:.1%}</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def current_session_frame(settings: dict) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Input", settings["current_input"], COLORS["input"]],
            ["Output", settings["current_output"], COLORS["output"]],
            ["Cached", settings["current_cached"], COLORS["cached"]],
            ["Reasoning", settings["current_reasoning"], COLORS["reasoning"]],
        ],
        columns=["type", "tokens", "color"],
    )


def metrics(data: pd.DataFrame, settings: dict) -> None:
    data = data.copy()
    data["estimated_cost"] = estimate_cost(data, settings)
    current = current_session_frame(settings)
    current_tokens = int(current["tokens"].sum())
    context_pct = current_tokens / settings["context_limit"]
    today = data.iloc[-1]
    week_tokens = int(data["total_tokens"].sum())
    week_cost = data["estimated_cost"].sum()

    cols = st.columns(5)
    cols[0].metric("Current Session", f"{current_tokens:,}", "tokens")
    cols[1].metric("Context Used", f"{context_pct:.1%}", f"{settings['context_limit']:,} limit")
    cols[2].metric("Today", f"{int(today['total_tokens']):,}", "tokens")
    cols[3].metric("7-Day Total", f"{week_tokens:,}", "tokens")
    cols[4].metric("Est. 7-Day Cost", f"${week_cost:,.2f}", "based on sidebar rates")


def token_mix_chart(settings: dict) -> None:
    df = current_session_frame(settings)
    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=72, outerRadius=128)
        .encode(
            theta="tokens:Q",
            color=alt.Color(
                "type:N",
                scale=alt.Scale(
                    domain=["Input", "Output", "Cached", "Reasoning"],
                    range=[COLORS["input"], COLORS["output"], COLORS["cached"], COLORS["reasoning"]],
                ),
                title=None,
            ),
            tooltip=["type", alt.Tooltip("tokens:Q", format=",")],
        )
        .properties(height=330)
    )
    st.altair_chart(chart, use_container_width=True)


def daily_usage_chart(data: pd.DataFrame) -> None:
    long = data.melt(
        ["date"],
        value_vars=["input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens"],
        var_name="token_type",
        value_name="tokens",
    )
    labels = {
        "input_tokens": "Input",
        "output_tokens": "Output",
        "cached_tokens": "Cached",
        "reasoning_tokens": "Reasoning",
    }
    long["token_type"] = long["token_type"].map(labels)
    chart = (
        alt.Chart(long)
        .mark_bar()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("tokens:Q", title="Tokens"),
            color=alt.Color(
                "token_type:N",
                scale=alt.Scale(
                    domain=["Input", "Output", "Cached", "Reasoning"],
                    range=[COLORS["input"], COLORS["output"], COLORS["cached"], COLORS["reasoning"]],
                ),
                title="Type",
            ),
            tooltip=["date:T", "token_type", alt.Tooltip("tokens:Q", format=",")],
        )
        .properties(height=330)
    )
    st.altair_chart(chart, use_container_width=True)


def cost_chart(data: pd.DataFrame, settings: dict) -> None:
    costed = data.copy()
    costed["estimated_cost"] = estimate_cost(costed, settings)
    chart = (
        alt.Chart(costed)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("estimated_cost:Q", title="Estimated cost ($)"),
            tooltip=["date:T", alt.Tooltip("estimated_cost:Q", format="$,.2f")],
            color=alt.value("#0f172a"),
        )
        .properties(height=290)
    )
    st.altair_chart(chart, use_container_width=True)


def context_gauge(settings: dict) -> None:
    total = sum(
        [
            settings["current_input"],
            settings["current_output"],
            settings["current_cached"],
            settings["current_reasoning"],
        ]
    )
    pct = min(total / settings["context_limit"], 1.0)
    gauge = pd.DataFrame(
        {
            "label": ["Used", "Remaining"],
            "value": [total, max(settings["context_limit"] - total, 0)],
        }
    )
    chart = (
        alt.Chart(gauge)
        .mark_arc(innerRadius=64, outerRadius=112)
        .encode(
            theta="value:Q",
            color=alt.Color("label:N", scale=alt.Scale(range=["#f97316", "#e2e8f0"]), legend=None),
            tooltip=["label", alt.Tooltip("value:Q", format=",")],
        )
        .properties(height=270)
    )
    st.altair_chart(chart, use_container_width=True)
    st.progress(pct, text=f"{total:,} / {settings['context_limit']:,} tokens")


def savings_panel(settings: dict) -> None:
    cached = settings["current_cached"]
    full_cost = cached / 1_000_000 * settings["input_rate"]
    discounted_rate = settings["input_rate"] * (1 - settings["cached_discount"] / 100)
    discounted_cost = cached / 1_000_000 * discounted_rate
    savings = full_cost - discounted_cost
    st.metric("Cached Token Savings", f"${savings:,.4f}", f"{settings['cached_discount']}% discount assumption")
    st.caption("This is an estimate. Match the sidebar rates to your actual provider/model pricing.")


add_css()
usage, settings = sidebar()
hero(settings)
st.write("")
metrics(usage, settings)

overview, trends, costs, data_tab, notes = st.tabs(
    ["Overview", "Trends", "Cost Model", "Usage Data", "Notes"]
)

with overview:
    left, mid, right = st.columns([1, 1.15, 0.95])
    with left:
        st.subheader("Current Token Mix")
        token_mix_chart(settings)
    with mid:
        st.subheader("Daily Usage")
        daily_usage_chart(usage)
    with right:
        st.subheader("Context Pressure")
        context_gauge(settings)
        savings_panel(settings)

with trends:
    st.subheader("Token Trend by Type")
    daily_usage_chart(usage)
    trend = usage.copy()
    trend["rolling_avg"] = trend["total_tokens"].rolling(3, min_periods=1).mean()
    line = (
        alt.Chart(trend)
        .mark_line(point=True)
        .encode(
            x="date:T",
            y=alt.Y("rolling_avg:Q", title="3-day average tokens"),
            tooltip=["date:T", alt.Tooltip("rolling_avg:Q", format=",")],
            color=alt.value("#7c3aed"),
        )
        .properties(height=280)
    )
    st.altair_chart(line, use_container_width=True)

with costs:
    st.subheader("Estimated Cost")
    cost_chart(usage, settings)
    st.info(
        "This is a calculator, not your official bill. It uses the pricing assumptions in the sidebar."
    )
    costed = usage.copy()
    costed["estimated_cost"] = estimate_cost(costed, settings)
    st.dataframe(costed, use_container_width=True, hide_index=True)

with data_tab:
    st.subheader("Underlying Usage Table")
    st.dataframe(usage, use_container_width=True, hide_index=True)
    csv = usage.to_csv(index=False).encode("utf-8")
    st.download_button("Download usage CSV", csv, "usage_dashboard_data.csv", "text/csv")
    st.code(
        "date,input_tokens,output_tokens,cached_tokens,reasoning_tokens\n"
        "2026-05-30,31000,7600,15000,3400",
        language="csv",
    )

with notes:
    st.subheader("How To Read This")
    st.markdown(
        """
        - **Input tokens**: what you send to the model, including context.
        - **Output tokens**: what the model writes back.
        - **Cached tokens**: reused context that may be cheaper, depending on the provider/model.
        - **Reasoning tokens**: internal thinking budget for models that expose or estimate it.
        - **Context pressure**: how much of the model window the current session may be using.

        This dashboard is set up for manual tracking or CSV upload because this app does not have direct access
        to your private provider billing/account telemetry.
        """
    )

st.caption(f"Dashboard refreshed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
