import streamlit as st
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Specify the directory where the model and encoders are saved
save_directory = os.getenv('SAVE_DIRECTORY', '.')

# Load the model and encoders from the saved location
model_path = f"{save_directory}/random_forest_model.joblib"
encoders_path = f"{save_directory}/label_encoders.joblib"

model = joblib.load(model_path)
label_encoders = joblib.load(encoders_path)

# Title for the Streamlit app
st.title('Depression Prediction')

# Header for input section
st.header('Enter the details below:')

# Take user input for the features
gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
age = st.number_input('Age', min_value=0, max_value=100, value=30)
work_pressure = st.slider('Work Pressure (1-10)', min_value=1, max_value=10, value=5)
job_satisfaction = st.slider('Job Satisfaction (1-10)', min_value=1, max_value=10, value=5)
sleep_duration = st.selectbox('Sleep Duration', ['5-6 hours', '7-8 hours', 'Less than 5 hours','More than 8 hours'])
dietary_habits = st.selectbox('Dietary Habits', ['Moderate', 'Unhealthy', 'Healthy'])
suicidal_thoughts = st.selectbox('Suicidal Thoughts', ['Yes', 'No'])
work_hours = st.number_input('Work Hours per week', min_value=0, max_value=168, value=40)
financial_stress = st.slider('Financial Stress (1-10)', min_value=1, max_value=10, value=5)
family_history_of_mental_illness = st.selectbox('Family History of Mental Illness', ['Yes', 'No'])

# Prepare input data for prediction
input_data = pd.DataFrame([{
    'Gender': gender,
    'Age': age,
    'Work_Pressure': work_pressure,
    'Job_Satisfaction': job_satisfaction,
    'Sleep_Duration': sleep_duration,
    'Dietary_Habits': dietary_habits,
    'Suicidal_thoughts': suicidal_thoughts,
    'Work_Hours': work_hours,
    'Financial_Stress': financial_stress,
    'Family_History_of_Mental_Illness': family_history_of_mental_illness
}])

# Encode categorical features using the saved encoders
for column, encoder in label_encoders.items():
    input_data[column] = encoder.transform(input_data[column])

# Button to make prediction
if st.button('Predict Depression'):
    # Make prediction
    prediction = model.predict(input_data)
    result = 'Depressed' if prediction[0] == 'Yes' else 'Not Depressed'
    
    # Display result
    st.write(f'Prediction: {result}')
    if result == 'Depressed':
        import smtplib
        from email.mime.text import MIMEText
        sender_email = os.getenv("SMTP_SENDER_EMAIL")
        sender_password = os.getenv("SMTP_SENDER_PASSWORD")  # Use App Password if 2FA is enabled
        recipient_email = os.getenv("SMTP_RECIPIENT_EMAIL")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))

        message = MIMEText('''The persion is depressed and is having mental health issues.''')
        message['Subject'] = "Depression alert "
        message['From'] = sender_email
        message['To'] = recipient_email

        # Use SMTP_SSL for port 465 or starttls for port 587
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()  # Can be omitted, but good practice
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())