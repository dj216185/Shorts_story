import streamlit as st
import pyttsx3
from io import BytesIO
import google.generativeai as genai
import os

# Configure Gemini API (replace with your actual API key)
genai.configure(api_key="AIzaSyAnx0sPWszruFwbn4-yzwOCEQgR8-04ufQ")  # Replace with your Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to fetch a story from Gemini API
def fetch_story(genre="Write a 30-second horror story for YouTube Shorts. Start with a mysterious sound in the dead of night that draws the protagonist to investigate. As they get closer, build suspense with chilling details. Conclude with a shocking twist as they discover the sound came from a shadowy figure mimicking their every move."):
    gemini_prompt = genre
    try:
        # Call the Gemini API to generate content
        response = model.generate_content(gemini_prompt)
        raw_text = response.candidates[0].content.parts[0].text
        return raw_text
    except Exception as e:
        return f"Failed to fetch story from Gemini API: {e}"
    
# Function to convert text to speech
def text_to_speech_with_pyttsx3(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Set speech rate
    engine.setProperty("volume", 1.0)  # Set volume level (0.0 to 1.0)

    # Save audio to a buffer
    audio_path = "generated_audio.mp3"
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    # Load the audio file into a BytesIO buffer
    with open(audio_path, "rb") as audio_file:
        audio_buffer = BytesIO(audio_file.read())

    os.remove(audio_path)  # Clean up temporary file
    return audio_buffer

# Function to trim the video to match the length of the audio
def trim_video(uploaded_file, audio_duration):
    # Save the uploaded video to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(uploaded_file.read())
        temp_video_path = temp_video_file.name

    video = VideoFileClip(temp_video_path)
    trimmed_video = video.subclipped(0, min(video.duration, audio_duration))
    trimmed_path = "trimmed_video.mp4"
    trimmed_video.write_videofile(trimmed_path, codec="libx264", audio_codec="aac")

    with open(trimmed_path, "rb") as video_file:
        video_buffer = BytesIO(video_file.read())

    os.remove(temp_video_path)  # Clean up temporary input video file
    os.remove(trimmed_path)  # Clean up temporary trimmed video file
    return video_buffer

# Streamlit App
st.title("Horror/Thriller Story Generator with TTS")

st.sidebar.header("Settings")
horror = "Write a 30-second horror story for YouTube Shorts and only give the story without any descriptions. Create a suspenseful and chilling scenario that keeps the audience on edge, with an unexpected and terrifying twist at the end. Avoid using cliches and make the story unique. Start with a mysterious sound in the dead of night that draws the protagonist to investigate. As they get closer, build suspense with chilling details. Conclude with a shocking twist as they discover the sound came from a shadowy figure mimicking their every move."
thriller = "Write a 30-second thriller story for YouTube Shorts and only give the story without any descriptions. Focus on building intense suspense and a sense of danger, leading to a shocking and unpredictable conclusion. Let the story unfold in any setting, with complete creative freedom. Begin with a person answering a phone call from an unknown number. Build tension as the caller predicts the protagonist's every move in real-time. End with a shocking twist as the protagonist realizes they are being watched from their own home."
mystery = "Write a 30-second mystery story for YouTube Shorts and only give the story without any descriptions. Develop a puzzling and intriguing scenario where something unusual or unexplained occurs. Let the ending surprise and provoke thought, leaving room for interpretation. Start with a detective receiving an envelope containing a photo of themselves taken moments earlier. Build intrigue as they notice strange details in the photo, like a shadow that wasn’t there. Conclude with an eerie twist as the detective realizes the shadow belongs to the person now standing behind them."
sci_fi = "Write a 30-second sci-fi story for YouTube Shorts and only give the story without any descriptions. Imagine a futuristic or otherworldly setting where something extraordinary happens. Keep the plot fast-paced and let the ending deliver a surprising twist that feels fresh and innovative. Begin with a person downloading a new app that claims to predict the future. Build suspense as the app sends them a series of notifications describing their every move seconds before they make them. End with a mind-bending twist as the app predicts, ‘You will delete me,’ and their phone freezes as they try."
fantasy = "Write a 30-second fantasy story for YouTube Shorts and only give the story without any descriptions. Set in a magical world or an ordinary world where something extraordinary occurs. Allow the narrative to unfold unpredictably, with a memorable and imaginative conclusion. Start with a street musician playing a haunting melody on a violin. Build wonder as their audience realizes the notes bring the surrounding statues to life. End with an unforgettable twist as the musician stops playing, and the statues turn their gaze toward them in silent fury."

selected_genre = st.sidebar.selectbox("Select Genre", [horror, thriller, mystery, sci_fi, fantasy])

generate_button = st.button("Generate Story")

if generate_button:
    with st.spinner("Fetching story..."):
        story = fetch_story(selected_genre)

    st.subheader("Generated Story")
    st.write(story)

    if story:
        with st.spinner("Converting story to speech..."):
            audio_buffer = text_to_speech_with_pyttsx3(story)

        st.subheader("Download Audio")
        st.audio(audio_buffer, format="audio/mp3")
        st.download_button(
            label="Download Audio",
            data=audio_buffer,
            file_name="story_audio.mp3",
            mime="audio/mp3",
        )

