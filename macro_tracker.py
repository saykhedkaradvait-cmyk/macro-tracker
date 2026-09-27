import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Add your Google AI Studio API key here
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use the fast, multimodal model
model = genai.GenerativeModel('gemini-3.5-flash-lite')

st.title("📸 AI Macro & Calorie Scanner")
st.write("Scan your meal, enter the total weight, and the AI will calculate the macros.")

# 2. Camera Input and Weight Input
picture = picture = st.file_uploader("Take a picture or upload one", type=["jpg", "jpeg", "png"])
weight = st.number_input("Enter the total weight of the meal (in grams):", min_value=1, value=250)

# 3. Process the Image and Calculate
if picture and weight:
    # Convert camera input to an image format the API can read
    img = Image.open(picture)
    
    # Instruct the AI to act as the calculator based on the specific weight
    prompt = f"""
    Analyze this food image and identify the items. 
    The total weight of the food shown is {weight} grams. 
    Act as a nutritionist and calculate the precise nutritional breakdown for exactly {weight} grams of this food.
    
    Provide the data in a clean list:
    - Total Calories: 
    - Protein (g): 
    - Carbohydrates (g): 
    - Fats (g): 
    
    Briefly explain how you estimated the density/ratios to get these numbers.
    """
    
    with st.spinner("Analyzing food and calculating macros..."):
        try:
            # Send the prompt and the image to the Vision AI
            response = model.generate_content([prompt, img])
            st.success("Analysis Complete!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")