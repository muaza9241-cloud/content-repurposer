import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

st.set_page_config(page_title="Content Repurposing Engine", page_icon="⚡", layout="wide")

st.title("⚡ AI Content Repurposing Engine")
st.markdown("Turn any blog post, article, or video transcript into ready-to-post social media content in seconds.")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    api_key = os.getenv("GROQ_API_KEY") or st.text_input("Groq API Key", type="password")
    
    language = st.selectbox(
        "Output Language / Style",
        ["English (Professional)", "English (Casual & Viral)", "Roman Urdu (Pakistani Creator Style)", "Urdu Script"]
    )
    
    audience = st.text_input("Target Audience (Optional)", placeholder="e.g., Founders, Students, Tech enthusiasts")

# Main input
source_text = st.text_area(
    "Paste your blog post, article, or transcript here:",
    height=220,
    placeholder="Paste your long-form content here..."
)

if st.button("🚀 Repurpose Content", type="primary"):
    if not api_key or "yahan_apni_api_key" in api_key:
        st.error("Please add your valid GROQ_API_KEY in the .env file or sidebar.")
    elif not source_text.strip():
        st.warning("Please paste some content first!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            system_prompt = f"""You are an expert social media strategist and copywriter.
Repurpose the user's provided content into high-performing social media assets.
Language/Tone requirement: {language}.
Target Audience: {audience if audience else 'General engaged readers'}.

Format your response strictly with these exact Markdown sections:
### 1. LinkedIn Post
(Engaging hook, structured takeaways with bullet points, and a strong closing CTA)

### 2. X (Twitter) Thread (5 Tweets)
(Numbered 1/5 to 5/5. Tweet 1 must be a scroll-stopping hook. Keep each tweet concise and punchy.)

### 3. Instagram / Facebook Caption
(Conversational, relatable caption with 5 relevant hashtags)

### 4. 5 Viral Hooks & Key Quotes
(Short, punchy one-liners extracted or adapted from the content)
"""
            with st.spinner("Generating your social media kit..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": source_text}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                output = response.choices[0].message.content
                st.success("Done! Your content kit is ready.")
                st.markdown("---")
                st.markdown(output)
                
                st.download_button(
                    label="📥 Download as Markdown (.md)",
                    data=output,
                    file_name="repurposed_content.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")
