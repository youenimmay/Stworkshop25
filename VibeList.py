import streamlit as st
from urllib.parse import quote
import random
from googleapiclient.discovery import build

st.set_page_config(page_title="VibeList 🎧", layout="wide")  # Set layout to wide

# Light, energetic, and eye-friendly background color
st.markdown("""
    <style>
    body {
        background-color: #f0faff;
    }
    .sticky-left {
        position: -webkit-sticky;
        position: sticky;
        top: 20px;
    }
    .button-row {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Emoji splashes for moods
mood_emojis = {
    "Chill": "🛋️", "Energetic": "⚡", "Focused": "🎯", "Romantic": "❤️",
    "Happy": "😊", "Sad": "😢", "Motivated": "🚀"
}

genre_emojis = {
    "Lo-fi": "🎧", "Jazz": "🎷", "Pop": "🎤", "Rock": "🎸",
    "Classical": "🎻", "EDM": "🎛️", "Instrumental": "🧘", "Hip-Hop": "🎶"
}

# Header
st.markdown(
    "<h1 style='text-align: center; font-size: 3em;'>🎶 VibeList</h1>"
    "<h3 style='text-align: center; font-weight: normal;'>Custom YouTube playlists for your current vibe</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

# Create two equal-width columns for preferences and video display
col1, col2 = st.columns([1, 1])  # Equal width for both columns

# Left Column: Mood, Genre, and Task Inputs (sticky)
with col1:
    st.markdown("<div class='sticky-left'>", unsafe_allow_html=True)
    st.markdown("### ✨ Customize Your Vibe")

    mood = st.selectbox("🧠 Mood", list(mood_emojis.keys()))
    genres = st.multiselect("🎵 Music Genre(s)", list(genre_emojis.keys()))
    task = st.text_input("💼 Task at Hand", placeholder="e.g. Studying, Cleaning, Coding...")

    # Button row with both buttons next to each other on the right
    st.markdown("<div class='button-row'>", unsafe_allow_html=True)
    generate_button = st.button("🚀 Generate My Playlist")
    clear_button = st.button("🧹 Clear Playlist")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# YouTube API setup using secrets
api_key = st.secrets["youtube_api_key"]
youtube = build("youtube", "v3", developerKey=api_key)

# Function to fetch YouTube videos based on search query
def get_youtube_videos(query, max_results=5):
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()

    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append((video_title, video_url))

    return video_urls

# Right Column: Video Results
with col2:
    if generate_button:
        if not genres:
            st.warning("🎯 Pick at least one genre to match your vibe!")
        else:
            search_query = f"{mood} {' '.join(genres)} music for {task}".strip()
            search_query_encoded = quote(search_query)

            st.markdown(
                f"<h3 style='text-align: center;'>🔥 Vibe: {mood_emojis[mood]} <br> 🎶 {' + '.join([genre_emojis[g] for g in genres])} for {task.capitalize()}</h3>",
                unsafe_allow_html=True
            )

            st.markdown("## 📺 Playlist Preview")

            # Fetch YouTube videos using the API
            video_urls = get_youtube_videos(search_query, max_results=5)

            for title, url in video_urls:
                # Embed the YouTube video with custom width using HTML
                video_embed_code = f'<iframe width="100%" height="394" src="https://www.youtube.com/embed/{url.split("v=")[1]}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                st.markdown(video_embed_code, unsafe_allow_html=True)

            search_url = f"https://www.youtube.com/results?search_query={search_query_encoded}"
            st.markdown(f"🔗 [View full playlist on YouTube ↗]({search_url})", unsafe_allow_html=True)

            st.success("🎉 Playlist ready. Enjoy the vibe!")

    if clear_button:
        st.empty()  # Clear the videos and the mood/genre/task selections
        st.markdown("## 🧹 Playlist Cleared!")
    else:
        st.info("👆 Set your mood, pick some genres, and click Generate!")
