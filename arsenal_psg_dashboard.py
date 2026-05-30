from datetime import date, datetime
import random

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="A Little Dashboard For Us",
    page_icon="heart",
    layout="wide",
    initial_sidebar_state="expanded",
)


COLORS = {
    "rose": "#e11d48",
    "pink": "#f9a8d4",
    "peach": "#fed7aa",
    "sky": "#7dd3fc",
    "lavender": "#c4b5fd",
    "ink": "#1f2937",
    "soft": "#fff7ed",
}


DEFAULT_REASONS = [
    "You make ordinary days feel lighter.",
    "Your laugh has this unfair ability to reset my whole mood.",
    "I love how we can be silly and serious in the same conversation.",
    "You make places feel warmer just by being there.",
    "You are my favorite person to tell tiny updates to.",
    "You make me want to notice more beautiful things.",
    "Being around you feels like coming home and starting an adventure at the same time.",
]


DEFAULT_MEMORIES = pd.DataFrame(
    [
        ["First spark", "That moment I realized I wanted more time with you.", 95],
        ["Our comfort era", "The small routines, inside jokes, and easy togetherness.", 88],
        ["The random laugh", "One of those laughs that made the whole day better.", 92],
        ["Future plans", "The trips, food spots, and little dreams still waiting for us.", 84],
        ["Right now", "This exact moment: a tiny web app made just to make you smile.", 100],
    ],
    columns=["Chapter", "What it means", "Smile score"],
)


DEFAULT_COUPONS = [
    "One coffee or dessert run, no questions asked",
    "One movie night where you pick everything",
    "One long walk with phones mostly away",
    "One homemade dinner attempt, bravery included",
    "One full day of extra compliments",
    "One emergency hug, redeemable anytime",
]


def add_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.2rem; }
        .hero {
            border-radius: 18px;
            padding: 32px;
            background:
                radial-gradient(circle at 15% 20%, rgba(255,255,255,.52), transparent 20%),
                linear-gradient(120deg, #fb7185 0%, #f9a8d4 38%, #93c5fd 100%);
            color: #1f2937;
            box-shadow: 0 18px 42px rgba(225,29,72,.22);
        }
        .hero h1 {
            font-size: 54px;
            line-height: 1.02;
            margin: 0;
            letter-spacing: 0;
        }
        .hero p {
            font-size: 18px;
            margin: 10px 0 0 0;
            max-width: 760px;
        }
        .tiny-pill {
            display: inline-block;
            padding: 6px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,.56);
            margin-right: 8px;
            margin-bottom: 10px;
            font-weight: 650;
        }
        .love-card {
            border: 1px solid rgba(225,29,72,.12);
            border-radius: 14px;
            padding: 18px;
            background: rgba(255,255,255,.74);
            box-shadow: 0 10px 24px rgba(31,41,55,.06);
            min-height: 128px;
        }
        .big-number {
            font-size: 44px;
            font-weight: 800;
            color: #e11d48;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(225,29,72,.12);
            border-radius: 14px;
            padding: 14px 16px;
            background: rgba(255,255,255,.70);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def auto_confetti(enabled: bool) -> None:
    if enabled:
        components.html(
            """
            <script>
            const colors = ["#fb7185", "#f9a8d4", "#93c5fd", "#c4b5fd", "#fed7aa"];
            function burst() {
              for (let i = 0; i < 36; i++) {
                const dot = document.createElement("div");
                dot.style.position = "fixed";
                dot.style.left = Math.random() * 100 + "vw";
                dot.style.top = "-12px";
                dot.style.width = "8px";
                dot.style.height = "8px";
                dot.style.borderRadius = "50%";
                dot.style.background = colors[Math.floor(Math.random() * colors.length)];
                dot.style.zIndex = 999999;
                dot.style.opacity = 0.85;
                dot.style.transition = "transform 2.8s ease-out, opacity 2.8s ease-out";
                document.body.appendChild(dot);
                setTimeout(() => {
                  dot.style.transform = `translateY(${90 + Math.random() * 20}vh) rotate(${Math.random() * 360}deg)`;
                  dot.style.opacity = 0;
                }, 30);
                setTimeout(() => dot.remove(), 3100);
              }
            }
            burst();
            </script>
            """,
            height=0,
        )


def sidebar() -> dict:
    st.sidebar.title("Make It Yours")
    your_name = st.sidebar.text_input("Your name", "Me")
    her_name = st.sidebar.text_input("Her name", "My favorite person")
    start_date = st.sidebar.date_input("A meaningful date", value=date(2024, 1, 1))
    anniversary = st.sidebar.date_input("Next date to count down to", value=date(date.today().year, 12, 31))
    if anniversary < date.today():
        anniversary = anniversary.replace(year=date.today().year + 1)

    headline = st.sidebar.text_input(
        "Headline",
        "A tiny corner of the internet made just for you",
    )
    note = st.sidebar.text_area(
        "Main note",
        "I made this because I wanted something cute, a little nerdy, and very us. "
        "If this makes you smile, it worked.",
        height=120,
    )
    show_confetti = st.sidebar.toggle("Confetti on refresh", value=True)
    auto_refresh = st.sidebar.toggle("Gentle auto-refresh", value=False)
    refresh_seconds = st.sidebar.slider("Refresh every", 20, 180, 60, step=10)
    if auto_refresh:
        components.html(
            f"<script>setTimeout(() => window.parent.location.reload(), {refresh_seconds * 1000});</script>",
            height=0,
        )

    return {
        "your_name": your_name,
        "her_name": her_name,
        "start_date": start_date,
        "anniversary": anniversary,
        "headline": headline,
        "note": note,
        "show_confetti": show_confetti,
    }


def days_between(start: date, end: date) -> int:
    return max((end - start).days, 0)


def hero(settings: dict) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <span class="tiny-pill">for {settings['her_name']}</span>
          <span class="tiny-pill">from {settings['your_name']}</span>
          <span class="tiny-pill">made with very serious dashboard science</span>
          <h1>{settings['headline']}</h1>
          <p>{settings['note']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrics(settings: dict) -> None:
    together_days = days_between(settings["start_date"], date.today())
    countdown = days_between(date.today(), settings["anniversary"])
    cols = st.columns(4)
    cols[0].metric("Days Since That Date", f"{together_days:,}", "and counting")
    cols[1].metric("Next Countdown", f"{countdown:,}", "days away")
    cols[2].metric("Smile Probability", "99.9%", "conservative estimate")
    cols[3].metric("Cute Dashboard Status", "Fully operational", "friendship-threateningly adorable")


def reason_machine(settings: dict) -> None:
    if "reason_index" not in st.session_state:
        st.session_state.reason_index = random.randrange(len(DEFAULT_REASONS))
    if st.button("Show me another reason", use_container_width=True):
        st.session_state.reason_index = (st.session_state.reason_index + 1) % len(DEFAULT_REASONS)
    reason = DEFAULT_REASONS[st.session_state.reason_index]
    st.markdown(
        f"""
        <div class="love-card">
          <div style="font-size:14px; font-weight:700; color:#e11d48;">REASON #{st.session_state.reason_index + 1}</div>
          <div style="font-size:25px; font-weight:750; margin-top:8px;">{reason}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def memory_chart(memories: pd.DataFrame) -> None:
    chart = (
        alt.Chart(memories)
        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
        .encode(
            y=alt.Y("Chapter:N", sort=None, title=None),
            x=alt.X("Smile score:Q", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "Chapter:N",
                legend=None,
                scale=alt.Scale(range=[COLORS["rose"], COLORS["pink"], COLORS["sky"], COLORS["lavender"], COLORS["peach"]]),
            ),
            tooltip=["Chapter", "What it means", "Smile score"],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)


def love_coupon() -> None:
    if "coupon" not in st.session_state:
        st.session_state.coupon = random.choice(DEFAULT_COUPONS)
    if st.button("Generate a tiny coupon", use_container_width=True):
        st.session_state.coupon = random.choice(DEFAULT_COUPONS)
    st.markdown(
        f"""
        <div class="love-card">
          <div style="font-size:14px; font-weight:700; color:#2563eb;">REDEEMABLE COUPON</div>
          <div style="font-size:24px; font-weight:750; margin-top:8px;">{st.session_state.coupon}</div>
          <div style="font-size:13px; margin-top:10px; color:#64748b;">Terms: valid whenever you need it. Expiry: absolutely never.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tiny_future_planner() -> None:
    st.subheader("Tiny Future Planner")
    ideas = st.multiselect(
        "Pick a vibe for our next plan",
        [
            "cozy dinner",
            "sunset walk",
            "dessert mission",
            "movie night",
            "day trip",
            "bookstore wander",
            "dress-up date",
            "lazy Sunday",
        ],
        default=["dessert mission", "sunset walk"],
    )
    budget = st.slider("Energy level required", 1, 10, 4)
    if ideas:
        st.success(f"Plan seed: {', '.join(ideas)}. Energy level: {budget}/10. Very doable. Very cute.")
    else:
        st.info("No pressure. Sometimes the best plan is just being together.")


def message_builder(settings: dict) -> None:
    st.subheader("A Little Note Generator")
    mood = st.selectbox("What kind of note?", ["soft", "silly", "romantic", "encouraging"])
    lines = {
        "soft": f"Hi {settings['her_name']}. I hope this little page feels like a warm hand squeeze.",
        "silly": f"Official dashboard finding: {settings['her_name']} remains dangerously cute. Further study required.",
        "romantic": f"Somehow, out of all the timelines, I got the one where I get to know you. Lucky me.",
        "encouraging": f"Whatever today feels like, I am in your corner. Always.",
    }
    st.text_area("Copyable note", lines[mood], height=110)


settings = sidebar()
add_css()
auto_confetti(settings["show_confetti"])

hero(settings)
st.write("")
metrics(settings)

overview, memories_tab, notes_tab, planner_tab = st.tabs(
    ["Smile Dashboard", "Our Little Timeline", "Notes & Coupons", "Next Date Idea"]
)

with overview:
    left, right = st.columns([1.05, 0.95])
    with left:
        st.subheader("Reason Machine")
        reason_machine(settings)
    with right:
        st.subheader("Today, Scientifically")
        mood = pd.DataFrame(
            [
                ["Missing you", 82],
                ["Thinking about you", 96],
                ["Wanting snacks together", 88],
                ["General fondness", 100],
            ],
            columns=["Metric", "Score"],
        )
        chart = (
            alt.Chart(mood)
            .mark_arc(innerRadius=55)
            .encode(
                theta="Score:Q",
                color=alt.Color(
                    "Metric:N",
                    scale=alt.Scale(range=[COLORS["rose"], COLORS["pink"], COLORS["sky"], COLORS["lavender"]]),
                ),
                tooltip=["Metric", "Score"],
            )
            .properties(height=310)
        )
        st.altair_chart(chart, use_container_width=True)

with memories_tab:
    st.subheader("Our Little Timeline")
    st.caption("Edit the memories in the code later to make this extremely specific.")
    st.dataframe(DEFAULT_MEMORIES, hide_index=True, use_container_width=True)
    memory_chart(DEFAULT_MEMORIES)

with notes_tab:
    left, right = st.columns(2)
    with left:
        message_builder(settings)
    with right:
        st.subheader("Tiny Coupon")
        love_coupon()

with planner_tab:
    tiny_future_planner()
    st.divider()
    st.subheader("A Small Promise")
    st.write(
        "This page can change over time. New memories, new jokes, new plans, new reasons. "
        "The point is not the dashboard. The point is you."
    )

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
