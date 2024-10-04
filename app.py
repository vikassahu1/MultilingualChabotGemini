import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech

# Custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
            .stTextArea label {
                font-size: 1.2em;
                font-weight: bold;
                color: #333333;
            }
            .stAudio label {
                font-size: 1.2em;
                font-weight: bold;
                color: #333333;
            }
            .stDownloadButton {
                margin-top: 20px;
            }
            .css-18e3th9 {
                padding-top: 2rem;
                padding-bottom: 2rem;
                background-color: #F0F2F6;
            }
        </style>
        """, unsafe_allow_html=True
    )

# Main function to build the app
def main():
    add_custom_css()

    # Title with an emoji icon
    st.title("🌍 Multilingual AI Assistant 🤖")

    # Add some description and instructions
    st.subheader("Ask me anything, in any language! 🌐")
    st.markdown("### Speak your question and receive an answer in real-time.")

    # Button for user input
    if st.button("🎤 Ask me anything"):
        with st.spinner("Listening... 🎧"):
            # Voice input and response
            text = voice_input()
            response = llm_model_object(text)
            
            # Convert response to speech
            text_to_speech(response)
            
            # Reading audio file for playback
            audio_file = open("speech.mp3", "rb")
            audio_bytes = audio_file.read()

            # Display the AI response in a text area
            st.text_area(label="💬 AI Response:", value=response, height=200)

            # Audio playback
            st.audio(audio_bytes)

            # Download button for the speech
            st.download_button(label="⬇️ Download Speech", 
                               data=audio_bytes, 
                               file_name="speech.mp3", 
                               mime="audio/mp3")

    # Additional aesthetic elements (spacing)
    st.markdown("<br><br>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
