from datetime import date, datetime
from pathlib import Path
import random

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


APP_PASSWORD = "Paris"


st.set_page_config(
    page_title="Our Travel Log",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


COLORS = {
    "rose": "#be123c",
    "pink": "#fda4af",
    "peach": "#fcd34d",
    "sky": "#38bdf8",
    "lavender": "#818cf8",
    "ink": "#1f2937",
    "soft": "#fff7ed",
}

PHOTO_DIR = Path(__file__).parent / "assets" / "photos"
FIRST_MESSAGE_DATE = date(2025, 9, 30)
FIRST_MEETING_DATE = date(2025, 10, 17)
NEXT_TRIP_DATE = date(2026, 6, 19)
NEXT_TRIP_NAME = "London / Milan"


DEFAULT_MEMORIES = pd.DataFrame(
    [
        ["First iMessage", FIRST_MESSAGE_DATE.strftime("%b %d, %Y"), "You said hello.", 90],
        ["NYC", FIRST_MEETING_DATE.strftime("%b %d, %Y"), "First time meeting in person.", 96],
        ["Shared albums", "Ongoing", "Every trip gets a title and its own archive.", 88],
        ["Next possible visit", "Next week, maybe", "Still undecided.", 72],
        [NEXT_TRIP_NAME, NEXT_TRIP_DATE.strftime("%b %d, %Y"), "The next confirmed chapter.", 98],
    ],
    columns=["Moment", "Date", "Notes", "Weight"],
)


DATE_IDEAS = [
    "coffee, walk, no over-planning",
    "good dinner reservation",
    "museum or bookstore detour",
    "hotel lobby tea / late-night recap",
    "train ride playlist",
    "one proper photo together before leaving",
]

SHARED_ALBUMS = [
    ["I saw that! I saw the whole thing", "A caught-in-4K kind of memory", "Inside joke", "Her city / your city"],
    ["I believe in looking..looking again.. and lo...", "A gallery title with dramatic suspense", "Running bit", "Somewhere together"],
    ["I'm talking to u from the 75th floor", "Big city, ridiculous altitude", "Skyline trip", "Her city"],
    ["Stanley cups and massage chairs", "Peak comfort. Elite hydration. No notes.", "Cozy chaos", "Your city"],
    ["Slow down!!", "A trip title that sounds like someone had to be supervised", "Transit lore", "Somewhere else"],
    ["Private sale", "Exclusive access to whatever the bit was that day", "Shopping arc", "Her city"],
    ["The one where she skipflagged", "An album title that deserves its own documentary", "Legendary incident", "Somewhere else"],
    ["Ajeeb Dastaan Hai Yeh", "A Bollywood-title-level chapter of the story", "Soft dramatic", "Your city"],
    ["AI remixes", "Proof that even the machines got dragged into the bit", "Creative chaos", "Online / distance"],
    ["Mugga", "Short title. Strong lore. No outsiders allowed.", "Inside joke", "Her city"],
    ["Hair Abu? weather said no", "The forecast became a character in the relationship", "Weather drama", "Somewhere else"],
    ["Swingers.. and put me down for a 2", "A title that immediately raises questions", "Comedy file", "Your city"],
    ["Discovering London fog and beyond", "Soft weather, big feelings, excellent title", "Travel chapter", "Somewhere else"],
    ["Why are there suitcases here", "Long-distance relationship core memory", "Airport energy", "Transit"],
    ["The next one comes in 30 mins", "A public-transit cliffhanger", "Transit lore", "Somewhere else"],
    ["Quiet zone violation", "The quiet zone never stood a chance", "Chaos", "Transit"],
    ["She fed me eggs...then beat me", "Breakfast, betrayal, and probably laughter", "Food + games", "Her city"],
    ["ACE'd it", "A winning chapter, obviously", "Victory lap", "Somewhere together"],
]


def add_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.2rem; }
        .hero {
            border-radius: 18px;
            padding: 32px;
            background: linear-gradient(120deg, #f8fafc 0%, #dbeafe 52%, #ffe4e6 100%);
            color: #1f2937;
            box-shadow: 0 18px 42px rgba(15,23,42,.10);
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


def password_gate() -> None:
    if st.session_state.get("unlocked"):
        return

    add_css()
    st.markdown(
        """
        <div class="hero">
          <span class="tiny-pill">private</span>
          <span class="tiny-pill">travel log</span>
          <h1>Before you come in...</h1>
          <p>This is a private page for the two people it is about.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    guess = st.text_input("Secret word", type="password", placeholder="hint: city we spent valentine's in?")
    col_a, col_b = st.columns([0.25, 0.75])
    with col_a:
        unlock = st.button("Unlock", width="stretch")
    if unlock:
        if guess.strip() == APP_PASSWORD:
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Not quite.")
    st.stop()


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
    st.sidebar.title("Settings")
    your_name = st.sidebar.text_input("Your name", "Myer")
    her_name = st.sidebar.text_input("Her name", "Her")
    start_date = st.sidebar.date_input("First iMessage", value=FIRST_MESSAGE_DATE)
    anniversary = st.sidebar.date_input("Next confirmed trip", value=NEXT_TRIP_DATE)

    headline = st.sidebar.text_input(
        "Headline",
        "Our travel log",
    )
    note = st.sidebar.text_area(
        "Main note",
        "A private dashboard for the trips, albums, dates, and oddly specific titles "
        "that have been collecting since the first hello.",
        height=120,
    )
    show_confetti = st.sidebar.toggle("Subtle page animation", value=False)
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


def load_photos() -> list[Path]:
    if not PHOTO_DIR.exists():
        return []
    return sorted(
        [
            path
            for path in PHOTO_DIR.iterdir()
            if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]
    )


def days_between(start: date, end: date) -> int:
    return max((end - start).days, 0)


def hero(settings: dict) -> None:
    photos = load_photos()
    photo_count = len(photos)
    st.markdown(
        f"""
        <div class="hero">
          <span class="tiny-pill">for {settings['her_name']}</span>
          <span class="tiny-pill">from {settings['your_name']}</span>
          <span class="tiny-pill">{photo_count} photo{'s' if photo_count != 1 else ''} loaded</span>
          <h1>{settings['headline']}</h1>
          <p>{settings['note']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrics(settings: dict) -> None:
    since_first_message = days_between(settings["start_date"], date.today())
    since_nyc = days_between(FIRST_MEETING_DATE, date.today())
    countdown = days_between(date.today(), settings["anniversary"])
    cols = st.columns(4)
    cols[0].metric("Since First iMessage", f"{since_first_message:,}", "Sep 30, 2025")
    cols[1].metric("Since NYC", f"{since_nyc:,}", "Oct 17, 2025")
    cols[2].metric(f"Until {NEXT_TRIP_NAME}", f"{countdown:,}", "starts Jun 19, 2026")
    cols[3].metric("Shared Albums", f"{len(SHARED_ALBUMS)}", "and counting")


def milestone_card() -> None:
    milestones = [
        ("First message", "Sep 30, 2025", "The first hello on iMessage."),
        ("First time meeting", "Oct 17, 2025", "NYC. The online thing became real life."),
        ("Next possible visit", "Next week", "Still undecided, which is very on-brand for travel planning."),
        (NEXT_TRIP_NAME, "Jun 19, 2026", "She gets there. The next confirmed album starts."),
    ]
    labels = [item[0] for item in milestones]
    selected_label = st.selectbox("Open a milestone", labels)
    selected = next(item for item in milestones if item[0] == selected_label)
    st.markdown(
        f"""
        <div class="love-card">
          <div style="font-size:14px; font-weight:700; color:#e11d48;">{selected[1]}</div>
          <div style="font-size:28px; font-weight:750; margin-top:8px;">{selected[0]}</div>
          <div style="font-size:16px; margin-top:10px;">{selected[2]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def photo_wall() -> None:
    photos = load_photos()
    if not photos:
        st.info("Add photos to assets/photos to turn this into a personal scrapbook.")
        return

    st.subheader("Selected Photos")
    st.caption("These are pulled from the photos you added for the app.")
    cols = st.columns(min(len(photos), 3))
    captions = [
        "Saved for the archive.",
        "One of the better frames.",
        "Added to the record.",
    ]
    for idx, photo in enumerate(photos):
        with cols[idx % len(cols)]:
            st.image(str(photo), width="stretch")
            st.caption(captions[idx % len(captions)])


def featured_photo() -> None:
    photos = load_photos()
    if not photos:
        return
    if "featured_photo_index" not in st.session_state:
        st.session_state.featured_photo_index = 0
    if st.button("Switch featured photo", width="stretch"):
        st.session_state.featured_photo_index = (st.session_state.featured_photo_index + 1) % len(photos)
    st.image(str(photos[st.session_state.featured_photo_index]), width="stretch")
    st.caption("Current featured memory")


def memory_chart(memories: pd.DataFrame) -> None:
    chart = (
        alt.Chart(memories)
        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
        .encode(
            y=alt.Y("Moment:N", sort=None, title=None),
            x=alt.X("Weight:Q", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "Moment:N",
                legend=None,
                scale=alt.Scale(range=[COLORS["rose"], COLORS["pink"], COLORS["sky"], COLORS["lavender"], COLORS["peach"]]),
            ),
            tooltip=["Moment", "Date", "Notes", "Weight"],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, width="stretch")


def date_idea_picker() -> None:
    if "date_idea" not in st.session_state:
        st.session_state.date_idea = random.choice(DATE_IDEAS)
    if st.button("Pick a low-effort plan", width="stretch"):
        st.session_state.date_idea = random.choice(DATE_IDEAS)
    st.markdown(
        f"""
        <div class="love-card">
          <div style="font-size:14px; font-weight:700; color:#2563eb;">NEXT VISIT OPTION</div>
          <div style="font-size:24px; font-weight:750; margin-top:8px;">{st.session_state.date_idea}</div>
          <div style="font-size:13px; margin-top:10px; color:#64748b;">Simple plans tend to survive travel days.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def album_frame() -> pd.DataFrame:
    albums = pd.DataFrame(SHARED_ALBUMS, columns=["Album", "Meaning", "Vibe", "Place"])
    albums["Chapter"] = range(1, len(albums) + 1)
    albums["Distance score"] = albums["Place"].map(
        {
            "Her city": 78,
            "Your city": 70,
            "Somewhere else": 88,
            "Somewhere together": 92,
            "Transit": 96,
            "Online / distance": 65,
        }
    ).fillna(75)
    albums["Memory weight"] = [
        92, 86, 95, 90, 82, 79, 93, 88, 84, 91, 87, 89, 94, 83, 81, 90, 96, 92
    ]
    return albums


def album_explorer() -> None:
    albums = album_frame()
    st.subheader("Shared Album Index")
    st.caption(
        "Every trip gets an album. The titles are basically their own timeline."
    )

    top = st.columns([0.9, 1.1])
    with top[0]:
        vibe = st.selectbox("Filter by vibe", ["All"] + sorted(albums["Vibe"].unique().tolist()))
    with top[1]:
        place = st.selectbox("Filter by place", ["All"] + sorted(albums["Place"].unique().tolist()))

    filtered = albums.copy()
    if vibe != "All":
        filtered = filtered[filtered["Vibe"] == vibe]
    if place != "All":
        filtered = filtered[filtered["Place"] == place]

    selected_album = st.selectbox("Open an album title", filtered["Album"].tolist())
    selected = albums[albums["Album"] == selected_album].iloc[0]
    st.markdown(
        f"""
        <div class="love-card">
          <div style="font-size:14px; font-weight:700; color:#e11d48;">ALBUM #{int(selected['Chapter'])}</div>
          <div style="font-size:27px; font-weight:800; margin-top:8px;">{selected['Album']}</div>
          <div style="font-size:16px; margin-top:10px;">{selected['Meaning']}</div>
          <div style="font-size:13px; margin-top:12px; color:#64748b;">
            Vibe: {selected['Vibe']} | Place: {selected['Place']}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Shared albums", len(albums), "since you met")
    c2.metric("Transit Albums", int((albums["Place"] == "Transit").sum()), "airport/train/bus")
    c3.metric("Away Trips", int((albums["Place"] == "Somewhere else").sum()), "not your city, not hers")


def album_charts() -> None:
    albums = album_frame()
    left, right = st.columns([1.15, 0.85])
    with left:
        chart = (
            alt.Chart(albums)
            .mark_circle(size=260, opacity=0.85)
            .encode(
                x=alt.X("Chapter:Q", title="Album chapter"),
                y=alt.Y("Memory weight:Q", scale=alt.Scale(domain=[70, 100])),
                color=alt.Color(
                    "Place:N",
                    scale=alt.Scale(
                        range=[COLORS["rose"], COLORS["sky"], COLORS["lavender"], COLORS["peach"], "#86efac", "#facc15"]
                    ),
                ),
                tooltip=["Chapter", "Album", "Vibe", "Place", "Meaning"],
            )
            .properties(height=330)
        )
        st.altair_chart(chart, width="stretch")
    with right:
        place_counts = albums.groupby("Place").size().reset_index(name="Albums")
        donut = (
            alt.Chart(place_counts)
            .mark_arc(innerRadius=55, outerRadius=105)
            .encode(
                theta="Albums:Q",
                color=alt.Color("Place:N", legend=None),
                tooltip=["Place", "Albums"],
            )
            .properties(height=330)
        )
        st.altair_chart(donut, width="stretch")


def next_trip_chooser() -> None:
    st.subheader("Next Album Title Drafts")
    location = st.selectbox("Where is the next chapter?", ["my city", "her city", "somewhere else", "airport/train"])
    mood = st.selectbox("Likely tone", ["low-key", "messy travel day", "nice dinner", "food-focused", "sleepy", "good story"])
    seed = f"{location}-{mood}-{date.today()}"
    random.seed(seed)
    starters = {
        "low-key": ["No rush, just us", "A normal day, somehow not normal", "Coffee before logistics"],
        "messy travel day": ["We had one job", "Gate change behaviour", "Why are there suitcases here again"],
        "nice dinner": ["Reservation evidence", "Dressed properly for once", "This deserved better lighting"],
        "food-focused": ["She said one bite", "Fork custody battle", "The sauce deserved a title"],
        "sleepy": ["Five more minutes", "Jet lag negotiations", "The nap agenda"],
        "good story": ["This needs an album title", "Plot development", "The recap will be long"],
    }
    title = random.choice(starters[mood])
    st.success(f"Draft title: {title}")


def tiny_future_planner() -> None:
    st.subheader("Next Trip Planner")
    ideas = st.multiselect(
        "Keep track of what sounds worth doing",
        [
            "coffee",
            "dinner reservation",
            "walkable neighborhood",
            "museum",
            "bookstore",
            "good dessert",
            "train photo",
            "one proper picture together",
        ],
        default=["coffee", "dinner reservation"],
    )
    budget = st.slider("How much planning energy?", 1, 10, 4)
    if ideas:
        st.success(f"Plan seed: {', '.join(ideas)}. Planning energy: {budget}/10.")
    else:
        st.info("No forced itinerary. Keep it open.")


def message_builder(settings: dict) -> None:
    st.subheader("Short Note Draft")
    mood = st.selectbox("Tone", ["straightforward", "dry", "travel", "appreciative"])
    lines = {
        "straightforward": f"I made this as a private place for our trips, albums, and the titles only we understand.",
        "dry": "This is either thoughtful or a sign I should not be left alone with dashboard tools.",
        "travel": f"Next confirmed chapter: {NEXT_TRIP_NAME}, starting {NEXT_TRIP_DATE.strftime('%B %d, %Y')}.",
        "appreciative": "I like that we have a whole archive already. The names alone are worth keeping.",
    }
    st.text_area("Copyable note", lines[mood], height=110)


password_gate()
settings = sidebar()
add_css()
auto_confetti(settings["show_confetti"])

hero(settings)
st.write("")
metrics(settings)

overview, albums_tab, memories_tab, notes_tab, planner_tab = st.tabs(
    ["Overview", "Shared Albums", "Timeline", "Notes", "Next Trip"]
)

with overview:
    left, right = st.columns([1.05, 0.95])
    with left:
        featured_photo()
    with right:
        st.subheader("Milestones")
        milestone_card()

    st.divider()
    st.subheader("Where Things Stand")
    left_chart, right_note = st.columns([1, 0.9])
    with left_chart:
        progress = pd.DataFrame(
            [
                ["First iMessage", days_between(FIRST_MESSAGE_DATE, date.today())],
                ["First NYC meeting", days_between(FIRST_MEETING_DATE, date.today())],
                [f"Until {NEXT_TRIP_NAME}", days_between(date.today(), NEXT_TRIP_DATE)],
                ["Shared albums", len(SHARED_ALBUMS)],
            ],
            columns=["Metric", "Value"],
        )
        chart = (
            alt.Chart(progress)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                x=alt.X("Value:Q", title=None),
                y=alt.Y("Metric:N", sort=None, title=None),
                color=alt.Color(
                    "Metric:N",
                    legend=None,
                    scale=alt.Scale(range=[COLORS["rose"], COLORS["pink"], COLORS["sky"], COLORS["lavender"]]),
                ),
                tooltip=["Metric", "Value"],
            )
            .properties(height=310)
        )
        st.altair_chart(chart, width="stretch")
    with right_note:
        st.markdown(
            """
            <div class="love-card">
              <div style="font-size:14px; font-weight:700; color:#e11d48;">CURRENT FILE</div>
              <div style="font-size:25px; font-weight:750; margin-top:8px;">
                First hello: Sep 30, 2025. First meeting: Oct 17, 2025. Next confirmed trip: London / Milan.
              </div>
              <div style="font-size:14px; color:#64748b; margin-top:10px;">
                The shared albums are the better evidence.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with albums_tab:
    album_explorer()
    st.divider()
    album_charts()
    st.divider()
    next_trip_chooser()

with memories_tab:
    photo_wall()
    st.divider()
    st.subheader("Timeline")
    st.caption("Actual dates and trip markers.")
    st.dataframe(DEFAULT_MEMORIES, hide_index=True, width="stretch")
    memory_chart(DEFAULT_MEMORIES)

with notes_tab:
    left, right = st.columns(2)
    with left:
        message_builder(settings)
    with right:
        st.subheader("Low-Effort Plan")
        date_idea_picker()

with planner_tab:
    tiny_future_planner()
    st.divider()
    st.subheader("Confirmed Next Chapter")
    st.write(
        f"{NEXT_TRIP_NAME} starts on {NEXT_TRIP_DATE.strftime('%B %d, %Y')}. "
        "The album title can wait until the trip earns it."
    )

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
