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
            {"role": "system", "content": "You are an environmental specialist. Provide personalized water-saving advice based on the user's input and data."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Function to analyze uploaded faucet data and generate a summary
def summarize_faucet_data(df):
    # Ensure timestamp is datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate total and daily usage
    total_usage = df.groupby("faucet_id")["usage_liters"].sum()
    daily_usage = df.groupby([df['timestamp'].dt.date, "faucet_id"])["usage_liters"].sum().unstack()

    # Average daily usage
    avg_daily_usage = daily_usage.mean()

    # Peak usage times
    peak_usage = df.groupby(df['timestamp'].dt.hour)["usage_liters"].sum().idxmax()

    # Create a summary for the prompt
    summary = f"Total usage per faucet:\n{total_usage}\n\n"
    summary += f"Average daily usage per faucet:\n{avg_daily_usage}\n\n"
    summary += f"Peak usage hour across all faucets: {peak_usage}:00\n\n"
    return summary

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
        
        # Additional questions
        household_type = st.selectbox("What type of home do you live in?", ["Apartment", "House", "Townhouse", "Other"])
        awareness_level = st.radio("How would you rate your awareness of water usage?", ["Low", "Medium", "High"])
        motivation = st.selectbox("Why are you interested in saving water?", ["Environmental concern", "Reducing bills", "Water scarcity", "Other"])

        # Generate prompt based on questionnaire responses
        prompt = f"""
        The user has provided the following details:
        - Household Size: {household_size}
        - Frequency of Water-Intensive Activities: {water_intensive_activities}
        - Existing Water-Saving Practices: {', '.join(water_saving_practices)}
        - Household Type: {household_type}
        - Awareness Level: {awareness_level}
        - Motivation for Saving Water: {motivation}
        
        Based on this information and any available data from the smart faucet, provide personalized advice on how the user can reduce water usage effectively.
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
            
            # Summarize the faucet data and generate prompt
            data_summary = summarize_faucet_data(df)
            st.write("Data Summary:")
            st.text(data_summary)  # Display the summary for transparency
            
            # Combine data summary with the advice prompt
            combined_prompt = f"""
            Here is the faucet usage data summary:
            {data_summary}
            
            Based on this data and the user's questionnaire responses, provide detailed and practical water-saving advice tailored to their usage patterns and household details.
            """

            # Get advice based on the faucet data and display it
            advice = get_completion(combined_prompt)
            st.subheader("Water Conservation Advice Based on Faucet Data")
            st.write(advice)

if __name__ == "__main__":
    main()
