import streamlit as st
from urllib.parse import quote
from googleapiclient.discovery import build

st.set_page_config(page_title="VibeList 🎧", layout="wide")

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
        justify-content: space-between;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Emojis
mood_emojis = {
    "Chill": "🛋️", "Energetic": "⚡", "Focused": "🎯", "Romantic": "❤️",
    "Happy": "😊", "Sad": "😢", "Motivated": "🚀"
}
genre_emojis = {
    "Lo-fi": "🎧", "Jazz": "🎷", "Pop": "🎤", "Rock": "🎸",
    "Classical": "🎻", "EDM": "🎛️", "Instrumental": "🧘", "Hip-Hop": "🎶"
}

# Title
st.markdown(
    "<h1 style='text-align: center; font-size: 3em;'>🎶 VibeList</h1>"
    "<h3 style='text-align: center; font-weight: normal;'>Custom YouTube playlists for your current vibe</h3>",
    unsafe_allow_html=True
)
st.markdown("---")

# Two equal columns
col1, col2 = st.columns([1, 1])

# Left Column: Preferences (Sticky)
with col1:
    st.markdown("<div class='sticky-left'>", unsafe_allow_html=True)
    st.markdown("### ✨ Customize Your Vibe")

    mood = st.selectbox("🧠 Mood", list(mood_emojis.keys()))
    genres = st.multiselect("🎵 Music Genre(s)", list(genre_emojis.keys()))
    task = st.text_input("💼 Task at Hand", placeholder="e.g. Studying, Cleaning, Coding...")

    st.markdown("<div class='button-row'>", unsafe_allow_html=True)
    generate_button = st.button("🚀 Generate My Playlist")
    clear_button = st.button("🧹 Clear Playlist")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column: YouTube Results
with col2:
    if generate_button:
        if not genres:
            st.warning("🎯 Pick at least one genre to match your vibe!")
        else:
            query = f"{mood} {' '.join(genres)} music for {task}".strip()
            query_encoded = quote(query)

            st.markdown(
                f"<h3 style='text-align: center;'>🔥 Vibe: {mood_emojis[mood]} <br> 🎶 {' + '.join([genre_emojis[g] for g in genres])} for {task.capitalize()}</h3>",
                unsafe_allow_html=True
            )
            st.markdown("## 📺 Playlist Preview")

            # YouTube API
             # Replace with your actual key
            youtube = build("youtube", "v3", developerKey=api_key)

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
                    vid = item['id']['videoId']
                    url = f"https://www.youtube.com/watch?v={vid}"
                    video_urls.append((item['snippet']['title'], url))
                return video_urls

            videos = get_youtube_videos(query, 5)

            for title, url in videos:
                embed = f'<iframe width="100%" height="394" src="https://www.youtube.com/embed/{url.split("v=")[1]}" frameborder="0" allowfullscreen></iframe>'
                st.markdown(embed, unsafe_allow_html=True)

            st.markdown(f"🔗 [View full playlist on YouTube ↗](https://www.youtube.com/results?search_query={query_encoded})", unsafe_allow_html=True)
            st.success("🎉 Playlist ready. Enjoy the vibe!")

    elif clear_button:
        st.empty()
        st.markdown("## 🧹 Playlist Cleared!")
    else:
        st.info("👆 Set your mood, pick some genres, and click Generate!")
