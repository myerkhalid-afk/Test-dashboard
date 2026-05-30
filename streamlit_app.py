from datetime import date, datetime
from pathlib import Path
import random

import altair as alt
import pandas as pd
import streamlit as st


APP_PASSWORD = "paris"
PHOTO_DIR = Path(__file__).parent / "assets" / "photos"

FIRST_MESSAGE_DATE = date(2025, 9, 30)
FIRST_MEETING_DATE = date(2025, 10, 17)
NEXT_TRIP_DATE = date(2026, 6, 19)
NEXT_TRIP_NAME = "London / Milan"

SHARED_ALBUMS = [
    ("I saw that! I saw the whole thing", "Inside joke", "Her city / your city"),
    ("I believe in looking..looking again.. and lo...", "Running bit", "Somewhere together"),
    ("I'm talking to u from the 75th floor", "Skyline trip", "Her city"),
    ("Stanley cups and massage chairs", "Comfort stop", "Your city"),
    ("Slow down!!", "Transit lore", "Somewhere else"),
    ("Private sale", "Shopping arc", "Her city"),
    ("The one where she skipflagged", "Incident report", "Somewhere else"),
    ("Ajeeb Dastaan Hai Yeh", "Soft dramatic", "Your city"),
    ("AI remixes", "Creative chaos", "Online / distance"),
    ("Mugga", "Inside joke", "Her city"),
    ("Hair Abu? weather said no", "Weather drama", "Somewhere else"),
    ("Swingers.. and put me down for a 2", "Comedy file", "Your city"),
    ("Discovering London fog and beyond", "Travel chapter", "Somewhere else"),
    ("Why are there suitcases here", "Airport energy", "Transit"),
    ("The next one comes in 30 mins", "Transit lore", "Somewhere else"),
    ("Quiet zone violation", "Transit lore", "Transit"),
    ("She fed me eggs...then beat me", "Food + games", "Her city"),
    ("ACE'd it", "Victory lap", "Somewhere together"),
]


st.set_page_config(page_title="Our Travel Log", page_icon=":airplane:", layout="wide")


def days_between(start: date, end: date) -> int:
    return max((end - start).days, 0)


def load_photos() -> list[Path]:
    if not PHOTO_DIR.exists():
        return []
    return sorted(
        photo
        for photo in PHOTO_DIR.iterdir()
        if photo.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )


def password_gate() -> None:
    if st.session_state.get("unlocked"):
        return

    st.title("Our Travel Log")
    st.caption("Private page.")
    guess = st.text_input("Secret word", type="password", placeholder="hint: city we spent valentine's in?")
    if st.button("Unlock"):
        if guess.strip().lower() == APP_PASSWORD.lower():
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Not quite.")
    st.stop()


def albums_frame() -> pd.DataFrame:
    albums = pd.DataFrame(SHARED_ALBUMS, columns=["Album", "Vibe", "Place"])
    albums["Chapter"] = range(1, len(albums) + 1)
    albums["Memory weight"] = [
        92, 86, 95, 90, 82, 79, 93, 88, 84, 91, 87, 89, 94, 83, 81, 90, 96, 92
    ]
    return albums


def header() -> None:
    st.title("Our Travel Log")
    st.write(
        "A private place for the trips, shared albums, dates, and oddly specific titles "
        "that have been collecting since the first hello."
    )

    since_first_message = days_between(FIRST_MESSAGE_DATE, date.today())
    since_nyc = days_between(FIRST_MEETING_DATE, date.today())
    until_trip = days_between(date.today(), NEXT_TRIP_DATE)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Since first iMessage", f"{since_first_message:,}", "Sep 30, 2025")
    c2.metric("Since NYC", f"{since_nyc:,}", "Oct 17, 2025")
    c3.metric(f"Until {NEXT_TRIP_NAME}", f"{until_trip:,}", "Jun 19, 2026")
    c4.metric("Shared albums", f"{len(SHARED_ALBUMS)}", "and counting")


def overview_tab() -> None:
    photos = load_photos()
    left, right = st.columns([1.05, 0.95])

    with left:
        if photos:
            st.image(str(photos[0]), caption="Selected photo", use_container_width=True)
        else:
            st.info("Photos can be added to assets/photos.")

    with right:
        st.subheader("Milestones")
        milestone = st.selectbox(
            "Open a milestone",
            ["First iMessage", "First time meeting", "Next possible visit", NEXT_TRIP_NAME],
        )
        notes = {
            "First iMessage": ("September 30, 2025", "The first hello on iMessage."),
            "First time meeting": ("October 17, 2025", "NYC. The online thing became real life."),
            "Next possible visit": ("Next week", "Still undecided."),
            NEXT_TRIP_NAME: ("June 19, 2026", "She gets there. The next confirmed album starts."),
        }
        when, detail = notes[milestone]
        st.info(f"{when} - {detail}")


def albums_tab() -> None:
    albums = albums_frame()
    st.subheader("Shared Album Index")
    st.write("Every trip gets an album. The titles are basically their own timeline.")

    c1, c2 = st.columns(2)
    with c1:
        vibe = st.selectbox("Filter by vibe", ["All"] + sorted(albums["Vibe"].unique()))
    with c2:
        place = st.selectbox("Filter by place", ["All"] + sorted(albums["Place"].unique()))

    filtered = albums.copy()
    if vibe != "All":
        filtered = filtered[filtered["Vibe"] == vibe]
    if place != "All":
        filtered = filtered[filtered["Place"] == place]

    selected_album = st.selectbox("Open an album", filtered["Album"].tolist())
    selected = albums[albums["Album"] == selected_album].iloc[0]
    st.success(f"Album #{selected['Chapter']}: {selected['Album']}")
    st.write(f"Vibe: {selected['Vibe']}")
    st.write(f"Place: {selected['Place']}")

    chart = (
        alt.Chart(albums)
        .mark_circle(size=220, opacity=0.85)
        .encode(
            x=alt.X("Chapter:Q", title="Album chapter"),
            y=alt.Y("Memory weight:Q", scale=alt.Scale(domain=[70, 100])),
            color="Place:N",
            tooltip=["Chapter", "Album", "Vibe", "Place", "Memory weight"],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


def timeline_tab() -> None:
    timeline = pd.DataFrame(
        [
            ("First iMessage", "Sep 30, 2025", "You said hello."),
            ("NYC", "Oct 17, 2025", "First time meeting in person."),
            ("Shared albums", "Ongoing", "Every trip gets a title and its own archive."),
            ("Next possible visit", "Next week, maybe", "Still undecided."),
            (NEXT_TRIP_NAME, "Jun 19, 2026", "The next confirmed chapter."),
        ],
        columns=["Moment", "Date", "Notes"],
    )
    st.subheader("Timeline")
    st.dataframe(timeline, hide_index=True, use_container_width=True)

    photos = load_photos()
    if photos:
        st.subheader("Photos")
        cols = st.columns(min(3, len(photos)))
        for idx, photo in enumerate(photos):
            with cols[idx % len(cols)]:
                st.image(str(photo), use_container_width=True)


def next_trip_tab() -> None:
    st.subheader("Next Trip")
    st.write(f"{NEXT_TRIP_NAME} starts on {NEXT_TRIP_DATE.strftime('%B %d, %Y')}.")

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

    if ideas:
        st.write("Plan seed:", ", ".join(ideas))

    draft_titles = [
        "No rush, just us",
        "Coffee before logistics",
        "Gate change behaviour",
        "Why are there suitcases here again",
        "This needs an album title",
        "The recap will be long",
    ]
    if st.button("Draft an album title"):
        st.session_state.next_title = random.choice(draft_titles)
    st.info(st.session_state.get("next_title", "Draft an album title when the trip earns one."))


password_gate()
header()

overview, albums, timeline, next_trip = st.tabs(["Overview", "Shared Albums", "Timeline", "Next Trip"])
with overview:
    overview_tab()
with albums:
    albums_tab()
with timeline:
    timeline_tab()
with next_trip:
    next_trip_tab()

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
