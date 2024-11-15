import os
import pandas as pd
import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client using the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Define the get_completion function using the client.chat.completions.create format
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an environmental specialist. Provide personalized water-saving advice based on the user's input."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content


# Function to analyze uploaded faucet data
def analyze_faucet_data(df):
    st.write("Uploaded Water Usage Data:")
    st.dataframe(df)
    
    # Check required columns
    if 'timestamp' in df.columns and 'faucet_id' in df.columns and 'usage_liters' in df.columns:
        # Convert timestamp column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Calculate total water usage per faucet
        total_usage = df.groupby("faucet_id")["usage_liters"].sum()
        st.write("Total water usage (liters) per faucet:")
        st.write(total_usage)

        # Calculate daily water usage for each faucet
        daily_usage = df.groupby(["date", "faucet_id"])["usage_liters"].sum().unstack()
        st.write("Daily water usage (liters) per faucet:")
        st.write(daily_usage)
        
        # Generate conservation advice based on analysis
        advice = []
        high_usage_faucet = total_usage.idxmax()
        advice.append(f"The faucet with the highest usage is {high_usage_faucet}. Consider checking for leaks or inefficiencies.")
        
        st.subheader("Water Conservation Advice Based on Faucet Data")
        st.write("\n".join(advice))
    else:
        st.error("The uploaded file must contain 'timestamp', 'faucet_id', and 'usage_liters' columns.")

# Streamlit App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Questionnaire & AI Advice", "Upload & Analyze Faucet Data"])

    if page == "Questionnaire & AI Advice":
        st.title("Water Usage Questionnaire - San Jose, CA")
        
        # Questionnaire
        household_size = st.selectbox("How many people live in your household?", ["1", "2", "3", "4", "5+"])
        water_intensive_activities = st.selectbox("How often do you do water-intensive activities (e.g., laundry, car washing, gardening)?", ["Daily", "Several times a week", "Weekly", "Rarely"])
        water_saving_practices = st.multiselect("Do you already follow any water-saving practices?", ["Low-flow showerheads", "Faucet aerators", "Reusing water", "Reducing shower time", "None"])

        # Generate prompt based on questionnaire responses
        prompt = f"""
        The user has provided the following details:
        - Household Size: {household_size}
        - Frequency of Water-Intensive Activities: {water_intensive_activities}
        - Existing Water-Saving Practices: {', '.join(water_saving_practices)}
        
        Provide personalized advice on how to reduce water usage based on these details.
        """
        
        # When user submits, generate AI advice
        if st.button("Get Water-Saving Advice"):
            advice = get_completion(prompt)
            st.subheader("Personalized Water-Saving Advice")
            st.write(advice)
    
    elif page == "Upload & Analyze Faucet Data":
        st.title("Smart Faucet Water Usage Analytics - Upload Data")

        # File upload
        uploaded_file = st.file_uploader("Upload a CSV file with your water usage data", type="csv")
        
        if uploaded_file is not None:
            # Load the uploaded data
            df = pd.read_csv(uploaded_file)
            analyze_faucet_data(df)

if __name__ == "__main__":
    main()
