import streamlit as st
import base64
import os
import uuid
from google import genai
from google.genai import types

# Set page configuration
st.set_page_config(
    page_title="Crochet Color Dreamer - LTK Cuties",
    page_icon="🧶",
    layout="centered"
)

# Custom CSS for an improved, cute pastel theme
st.markdown("""
<style>
    /* Main background with improved gradient */
    .stApp {
        background: linear-gradient(135deg, #FFD1DC, #E2B6FF, #D5AAFF);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content area */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 3px solid #FF85A2;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Comic Sans MS', 'Bubblegum Sans', cursive;
        color: #D6006B;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
        letter-spacing: 0.5px;
    }
    
    /* Normal text */
    p, div {
        color: #333333;
    }
    
    /* Transform button */
    .stButton button {
        background: linear-gradient(90deg, #FF85A2, #D16BA5);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(209, 107, 165, 0.4);
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, #FF6B8B, #C25A94);
        box-shadow: 0 6px 15px rgba(209, 107, 165, 0.6);
        transform: translateY(-2px);
    }
    
    /* Downloaded button styling */
    .stDownloadButton button {
        background: linear-gradient(90deg, #9F7AEA, #B17ACC);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s;
        margin-top: 10px;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(90deg, #8B5CF6, #9F5ABA);
        box-shadow: 0 4px 12px rgba(159, 122, 234, 0.4);
    }
    
    /* Image containers */
    .uploadedImage {
        border: 3px dashed #FF85A2;
        border-radius: 20px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.7);
        margin-bottom: 25px;
        transition: all 0.3s;
    }
    
    .uploadedImage:hover {
        border-color: #D16BA5;
        box-shadow: 0 5px 15px rgba(209, 107, 165, 0.3);
    }
    
    .generatedImage {
        border: 3px solid #9F7AEA;
        border-radius: 20px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.7);
        box-shadow: 0 5px 15px rgba(159, 122, 234, 0.3);
        transition: all 0.3s;
    }
    
    .generatedImage:hover {
        box-shadow: 0 8px 20px rgba(159, 122, 234, 0.5);
        transform: translateY(-3px);
    }
    
    /* Text input styling */
    .stTextInput input {
        border-radius: 15px;
        border: 2px solid #FF85A2 !important;
        background-color: #FFF5F7 !important; /* Subtle pink tint */
        color: #1A1A1A !important;           /* Darker text color for better contrast */
        font-size: 18px !important;
        padding: 15px 20px !important;       /* Increased padding */
        width: 100% !important;
        height: 60px !important;             /* Fixed height for larger appearance */
        transition: all 0.3s !important;
    }

    .stTextInput input:focus {
        border-color: #D6006B !important;
        box-shadow: 0 0 10px rgba(214, 0, 107, 0.3) !important;
        background-color: #FFFFFF !important; /* Pure white on focus */
    }
    
    /* File uploader styling - FIXED to match theme */
    .css-1dp5vir, .css-9ycgxx, .css-demzbm, [data-testid="stFileUploader"] {
        background-color: rgba(255, 235, 243, 0.8) !important;
        border-radius: 20px !important;
        border: 2px dashed #FF85A2 !important;
        color: #D6006B !important;
        padding: 15px !important;
        transition: all 0.3s !important;
    }
    
    /* File uploader inner elements */
    [data-testid="stFileUploader"] > section {
        background-color: rgba(255, 225, 235, 0.8) !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    
    /* Fix the dark background in the file uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 240, 245, 0.9) !important;
        border: 2px dashed #FF85A2 !important;
        color: #D6006B !important;
    }
    
    /* Style the uploads box text */
    [data-testid="stFileUploadDropzone"] p {
        color: #D6006B !important;
    }
    
    /* Fix the icon color */
    [data-testid="stFileUploadDropzone"] svg {
        color: #FF85A2 !important;
    }
    
    /* File limit text */
    [data-testid="stFileUploadDropzone"] small {
        color: #333 !important;
    }
    
    .css-1dp5vir:hover, .css-9ycgxx:hover, .css-demzbm:hover, [data-testid="stFileUploader"]:hover {
        background-color: #FFE6EE !important;
        border-color: #D6006B !important;
    }
    
    /* Hide the fullscreen option */
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* Upload text */
    [data-testid="stFileUploader"] label {
        color: #D6006B !important;
        font-weight: bold !important;
    }
    
    /* Image captions */
    .stImage img + div {
        text-align: center !important;
        font-weight: bold !important;
        color: #D6006B !important;
        font-size: 16px !important;
        margin-top: 10px !important;
    }
    
    /* Browse files button */
    .css-1offfwp p, [data-testid="stMarkdownContainer"] p {
        font-weight: 500 !important;
    }
    
    .st-bq, [data-testid="stFileUploadDropzone"] button {
        background-color: #FF85A2 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s !important;
    }
    
    .st-bq:hover, [data-testid="stFileUploadDropzone"] button:hover {
        background-color: #D6006B !important;
        box-shadow: 0 4px 8px rgba(214, 0, 107, 0.3) !important;
    }
    
    /* Spinner */
    .stSpinner {
        margin: 20px auto !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 133, 162, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* For footer */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, rgba(255, 133, 162, 0), rgba(255, 133, 162, 0.8), rgba(255, 133, 162, 0));
        margin: 30px 0;

    /* Hide the "View fullscreen" button on images */
    [data-testid="stImage"] button[title="View fullscreen"] {
    display: none !important;
}
    }
</style>
""", unsafe_allow_html=True)

# App title and description with better styling
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>✨ Crochet Color Dreamer ✨</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-top: 0px; margin-bottom: 20px;'>LTK Cuties</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #333333; background-color: rgba(255,255,255,0.7); padding: 12px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);'>Transform your crochet creations with magical color themes! 🧶✨</p>", unsafe_allow_html=True)

# Function to save binary file
def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    return file_name

# Function to generate recolored image
def generate_recolored_image(uploaded_file, color_prompt):
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API key not found. Please check your configuration.")
        return None, ""
    
    # Initialize client
    client = genai.Client(api_key=api_key)
    
    try:
        # Create a temporary file to store the uploaded content
        temp_filename = f"temp_upload_{uuid.uuid4()}.{uploaded_file.name.split('.')[-1]}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        with st.spinner("💫 Preparing your crochet item..."):
            # Upload the user's image using the file path
            files = [
                client.files.upload(file=temp_filename),
            ]
        
        # Set up the model
        model = "gemini-2.0-flash-exp"
        
        # Create a unique filename for the output
        output_filename = f"generated_{uuid.uuid4()}.png"
        
        # Create the contents for the API call
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=files[0].uri,
                        mime_type=files[0].mime_type,
                    ),
                    types.Part.from_text(text=f"Change the colors of this crochet item to look like: {color_prompt}. Maintain the same style and patterns, just transform the colors."),
                ],
            ),
        ]
        
        # Configure generation
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_modalities=["image", "text"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_CIVIC_INTEGRITY",
                    threshold="OFF",
                ),
            ],
            response_mime_type="text/plain",
        )
        
        # Generate content
        result = None
        text_response = ""
        
        with st.spinner("🎨 Working magic on your crochet creation..."):
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                
                for part in chunk.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Save image data
                        save_binary_file(output_filename, part.inline_data.data)
                        result = output_filename
                    elif hasattr(part, 'text'):
                        # Append text
                        text_response += part.text
        
        # Clean up the temporary file
        try:
            os.remove(temp_filename)
        except:
            pass
            
        return result, text_response
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Clean up the temporary file if it exists
        try:
            if 'temp_filename' in locals():
                os.remove(temp_filename)
        except:
            pass
        return None, str(e)

# Better styled file uploader - fixed with proper label
st.markdown("<p style='font-weight: bold; color: #D6006B; font-size: 20px; margin-bottom: 15px; text-align: center;'>Upload Your Crochet Creation 🧶</p>", unsafe_allow_html=True)


# Fixed file uploader with proper label
uploaded_file = st.file_uploader("Choose a clear photo of your crochet item with good lighting", type=["jpg", "jpeg", "png"])
st.markdown("</div>", unsafe_allow_html=True)

# Container for the form
with st.container():
    # Show the uploaded image
    if uploaded_file:
        # Create a custom container for the image
        st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
        st.image(uploaded_file, caption="Your Original Crochet Creation", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input for color/theme preferences with enhanced styling
        st.markdown("<p style='font-weight: bold; color: #D6006B; font-size: 18px; margin-bottom: 10px;'>Describe your dream colors or theme 🌈</p>", unsafe_allow_html=True)
        
        color_prompt = st.text_input(
            "Enter your color description",
            placeholder="e.g., pastel rainbow, ocean blues, autumn sunset, unicorn theme...",
            help="Be creative! Try themes like 'fairy garden' or 'winter wonderland'"
        )
        
        # Generate button with eye-catching styling
        transform_button = st.button("✨ Transform My Crochet ✨")
        
        if transform_button:
            if color_prompt:
                # Generate the recolored image
                result_file, text_response = generate_recolored_image(uploaded_file, color_prompt)
                
                if result_file and os.path.exists(result_file):
                    # Show success message
                    st.success("✨ Your crochet has been transformed successfully!")
                    
                    # Display the generated image with enhanced styling
                    st.markdown('<div class="generatedImage">', unsafe_allow_html=True)
                    st.image(result_file, caption=f"Your Crochet in {color_prompt.title()} Colors", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display any text response
                    if text_response:
                        with st.expander("Design Notes 📝"):
                            st.write(text_response)
                    
                    # Add download button with custom styling
                    col1, col2, col3 = st.columns([1,2,1])
                    with col2:
                        with open(result_file, "rb") as file:
                            st.download_button(
                                label="💾 Download Your New Design",
                                data=file,
                                file_name=f"LTK_Cuties_{color_prompt.replace(' ', '_')}.png",
                                mime="image/png"
                            )
                else:
                    st.error("Sorry, we couldn't transform your crochet. Please try a different prompt or image.")
            else:
                st.warning("Please enter color or theme preferences to transform your crochet.")
    else:
        # Placeholder when no image is uploaded with better styling
        st.markdown("""
        <div style="margin-top: 30px; background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 20px; border: 2px solid #9F7AEA;">
            <h3 style="text-align: center; margin-bottom: 15px;">✨ Theme Ideas ✨</h3>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <span style="background-color: #FFD1DC; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Pastel Rainbow</span>
                <span style="background-color: #AEC6CF; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Ocean Blues</span>
                <span style="background-color: #FDFD96; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Sunshine Yellow</span>
                <span style="background-color: #B39EB5; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Lavender Dreams</span>
                <span style="background-color: #FF6961; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Sunset Vibes</span>
                <span style="background-color: #77DD77; padding: 8px 15px; border-radius: 20px; font-size: 14px;">Mint Chocolate</span>
            </div>
            <p style="text-align: center; font-size: 14px; color: #666; margin-top: 10px;">
                Try descriptive themes like "galaxy colors," "vintage pastels," or "cottagecore palette"
            </p>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p style="color: #D6006B; font-weight: bold;">Made with 💕 for LTK Cuties</p>
    <p style="font-size: 14px; color: #666;">Transform your crochet projects with a click!</p>
</div>
""", unsafe_allow_html=True)
