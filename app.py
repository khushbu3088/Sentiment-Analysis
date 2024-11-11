import streamlit as st
from textblob import TextBlob
import pandas as pd
import cleantext
import io

st.set_page_config(page_title="Text & CSV Analysis App", page_icon="📊", layout="centered")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Analyze Text", "Clean Text", "Analyze CSV"])

# Home page
if page == "Home":
    st.title("📊 Text & CSV Analysis App")
    st.write("Welcome to the Text & CSV Analysis App. Use the sidebar to navigate to different pages!")
    st.image(r"C:\Users\Durgesh Verma\Desktop\Sentiment Analysis\senti.jpg")

# Analyze Text Page
elif page == "Analyze Text":
    st.title("📈 Text Sentiment Analysis")
    text = st.text_area("Enter text to analyze:")

    if st.button("Analyze Sentiment"):
        if text:
            blob = TextBlob(text)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            st.write("*Polarity:*", polarity)
            st.write("*Subjectivity:*", subjectivity)
        else:
            st.warning("Please enter text to analyze.")

# Clean Text Page
elif page == "Clean Text":
    st.title("🧹 Text Cleaning Tool")
    pre = st.text_area("Enter text to clean:")

    if st.button("Clean Text"):
        if pre:
            cleaned_text = cleantext.clean(
                pre,
                clean_all=False,
                extra_spaces=True,
                stopwords=True,
                lowercase=True,
                numbers=True,
                punct=True,
            )
            st.write("*Cleaned Text:*")
            st.write(cleaned_text)
        else:
            st.warning("Please enter text to clean.")

# Analyze CSV Page
elif page == "Analyze CSV":
    st.title("📊 CSV Sentiment Analysis")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        # Load CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())

        if 'tweet' not in df.columns:
            st.warning("The CSV file must contain a 'tweet' column.")
        else:
            # Calculate polarity scores and sentiment labels
            df['score'] = df['tweet'].apply(lambda x: TextBlob(x).sentiment.polarity)
            df['analysis'] = df['score'].apply(lambda x: 'Positive' if x >= 0.5 else ('Negative' if x <= -0.5 else 'Neutral'))

            st.write("Analyzed Data:")
            st.write(df[['tweet', 'score', 'analysis']])

            # Download analyzed CSV file
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Analyzed Data as CSV",
                data=csv_data,
                file_name='analyzed_sentiment.csv',
                mime='text/csv',
            )