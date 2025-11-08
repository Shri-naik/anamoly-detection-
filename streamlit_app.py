import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import uuid
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="EcoVision - Environmental Monitoring",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Model Configuration
# ---------------------------
MODEL_PATHS = {
    "water": "water_best_model.h5",
    "air": "air_best_model.h5"
}

CLASS_NAMES = ["Clean", "Little Polluted", "Highly Polluted"]

# ---------------------------
# Helper Functions
# ---------------------------
@st.cache_resource
def load_model(model_path):
    """Load and cache the model"""
    if not os.path.exists(model_path):
        return None
    return tf.keras.models.load_model(model_path)

def preprocess_image(image, img_size=(224, 224)):
    """Preprocess image for model prediction"""
    img = image.resize(img_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def analyze_water_rgb(image):
    """Analyze water quality based on RGB values"""
    img = np.array(image)
    avg_rgb = np.mean(img, axis=(0, 1))  
    r, g, b = avg_rgb
    analysis = []

    if g > r and g > b and g > 100:
        analysis.append("🟢 High green: Possible algae growth. If harmful algae → remove with UV/chemical treatment. If harmless → can be used as biofertilizer or biofuel.")
    if r > g and r > b and r > 100:
        analysis.append("🔴 High red/brown: Possible iron or suspended solids. Treat with filtration/sedimentation.")
    if b > r and b > g and b > 120:
        analysis.append("🔵 Strong blue: Likely clean water, suitable for use.")
    if np.mean(avg_rgb) < 60:
        analysis.append("⚫ Very dark: Possible industrial waste / oil contamination. Requires chemical treatment before safe use.")
    if not analysis:
        analysis.append("No major harmful constituents detected visually.")
    return avg_rgb, analysis

def analyze_air_rgb(image):
    """Analyze air quality based on RGB values"""
    img = np.array(image)
    avg_rgb = np.mean(img, axis=(0, 1))  
    r, g, b = avg_rgb
    analysis = []

    if np.mean(avg_rgb) < 80:
        analysis.append("🌫️ Dark/gray tones: Possible smog or soot. Avoid exposure, use masks/air filters.")
    if r > 120 and r > g and r > b:
        analysis.append("🟤 Brown haze: Possible dust or industrial emissions. Reduce outdoor activity.")
    if g > 120 and g > r and g > b:
        analysis.append("🟢 Greenish tint: Could indicate chemical pollutants. Ventilation and monitoring advised.")
    if b > 130 and b > r and b > g:
        analysis.append("🔵 Clear sky with strong blue: Clean air likely.")
    if not analysis:
        analysis.append("No major harmful air constituents detected visually.")
    return avg_rgb, analysis

def create_confidence_chart(probs):
    """Create a confidence chart"""
    categories = list(probs.keys())
    values = list(probs.values())
    
    colors = ['#28a745', '#ffc107', '#dc3545']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Prediction Confidence Scores",
        xaxis_title="Pollution Level",
        yaxis_title="Confidence (%)",
        height=300,
        showlegend=False
    )
    
    return fig

def create_rgb_analysis_chart(avg_rgb, pollution_type):
    """Create RGB analysis visualization"""
    colors = ['Red', 'Green', 'Blue']
    values = avg_rgb
    
    fig = go.Figure(data=[
        go.Bar(
            x=colors,
            y=values,
            marker_color=['#ff4444', '#44ff44', '#4444ff'],
            text=[f"{v:.1f}" for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f"Average RGB Values - {pollution_type.title()} Analysis",
        xaxis_title="Color Channel",
        yaxis_title="Intensity",
        height=300,
        showlegend=False
    )
    
    return fig

# ---------------------------
# UI Components
# ---------------------------
def show_landing_page():
    """Display the landing page"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;'>🌍 EcoVision</h1>
        <h2 style='color: #4682B4; font-size: 1.5rem; margin-bottom: 2rem;'>AI-Powered Environmental Monitoring</h2>
        <p style='font-size: 1.2rem; color: #555; max-width: 600px; margin: 0 auto;'>
            Upload images of water or air to get instant AI-powered analysis of pollution levels. 
            Our advanced machine learning models provide accurate assessments with actionable recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: #f0f8ff; border-radius: 10px;'>
            <h3>💧 Water Quality</h3>
            <p>Analyze water pollution levels and get treatment recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: #f0fff0; border-radius: 10px;'>
            <h3>🌫️ Air Quality</h3>
            <p>Assess air pollution and receive health safety guidelines</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: #fff8dc; border-radius: 10px;'>
            <h3>🤖 AI Analysis</h3>
            <p>Advanced ML models with RGB analysis for comprehensive assessment</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------
# Main App Logic
# ---------------------------
def main():
    # Sidebar for navigation
    st.sidebar.title("🌍 EcoVision")
    st.sidebar.markdown("Environmental Monitoring System")
    
    page = st.sidebar.radio("Navigate", ["Home", "Water Quality Analysis", "Air Quality Analysis"])
    
    if page == "Home":
        show_landing_page()
        
    elif page in ["Water Quality Analysis", "Air Quality Analysis"]:
        pollution_type = "water" if "Water" in page else "air"
        
        st.title(f"💧 Water Quality Analysis" if pollution_type == "water" else "🌫️ Air Quality Analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            f"Upload an image for {pollution_type} quality analysis",
            type=['png', 'jpg', 'jpeg'],
            help=f"Upload a clear image showing {pollution_type} conditions for accurate analysis"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Uploaded Image")
                image = Image.open(uploaded_file).convert("RGB")
                st.image(image, caption=f"Uploaded {pollution_type} image", use_column_width=True)
            
            # Load model and make prediction
            with st.spinner(f"Loading {pollution_type} quality model..."):
                model = load_model(MODEL_PATHS[pollution_type])
                
            if model is None:
                st.error(f"❌ {pollution_type.title()} quality model not found. Please ensure the model file exists.")
                return
                
            # Make prediction
            with st.spinner("Analyzing image..."):
                img_array = preprocess_image(image)
                pred = model.predict(img_array)
                confidence = np.max(pred)
                label_index = np.argmax(pred)
                prediction = CLASS_NAMES[label_index]
                
                # Get all probabilities
                probs = {CLASS_NAMES[i]: float(pred[0][i] * 100) for i in range(len(CLASS_NAMES))}
            
            with col2:
                st.subheader("Analysis Results")
                
                # Determine severity class and color
                if label_index == 0:
                    class_name = "Low"
                    color = "🟢"
                elif label_index == 1:
                    class_name = "Medium"
                    color = "🟡"
                else:
                    class_name = "High"
                    color = "🔴"
                
                st.metric(
                    label=f"Pollution Level",
                    value=f"{color} {prediction}",
                    delta=f"{confidence*100:.1f}% confidence"
                )
                
                # RGB Analysis
                if pollution_type == "water":
                    avg_rgb, analysis = analyze_water_rgb(image)
                else:
                    avg_rgb, analysis = analyze_air_rgb(image)
                
                st.subheader("🔍 Detailed Analysis")
                for item in analysis:
                    st.write(f"• {item}")
            
            # Visualizations
            st.subheader("📊 Analysis Visualizations")
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Confidence chart
                fig_conf = create_confidence_chart(probs)
                st.plotly_chart(fig_conf, use_container_width=True)
            
            with col4:
                # RGB analysis chart
                fig_rgb = create_rgb_analysis_chart(avg_rgb, pollution_type)
                st.plotly_chart(fig_rgb, use_container_width=True)
            
            # Additional insights
            st.subheader("💡 Recommendations")
            
            if prediction == "Clean":
                st.success("✅ The environmental conditions appear to be within safe parameters.")
            elif prediction == "Little Polluted":
                st.warning("⚠️ Moderate pollution detected. Consider implementing monitoring and preventive measures.")
            else:
                st.error("🚨 High pollution levels detected! Immediate action and professional assessment recommended.")
            
            # Technical details expander
            with st.expander("🔧 Technical Details"):
                st.write(f"**Model Used:** {pollution_type.title()} Quality Assessment Model")
                st.write(f"**Prediction Confidence:** {confidence*100:.2f}%")
                st.write(f"**Average RGB Values:** R={avg_rgb[0]:.1f}, G={avg_rgb[1]:.1f}, B={avg_rgb[2]:.1f}")
                st.write(f"**Image Preprocessing:** MobileNetV2 preprocessing applied")
                st.write(f"**Model Architecture:** Transfer learning with fine-tuned classification head")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 About")
    st.sidebar.info(
        "EcoVision uses advanced AI models to analyze environmental images "
        "and provide real-time pollution assessments with actionable recommendations."
    )

if __name__ == "__main__":
    main()