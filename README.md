# 🌍 EcoVision - Environmental Monitoring System

An AI-powered environmental monitoring system that analyzes water and air quality from images using advanced machine learning models. Built with Streamlit for easy deployment and user-friendly interface.

## 🚀 Features

- **Water Quality Analysis**: Upload water images to detect pollution levels and get treatment recommendations
- **Air Quality Assessment**: Analyze air conditions from images with health safety guidelines  
- **AI-Powered Predictions**: Advanced ML models with high accuracy and confidence scores
- **RGB Analysis**: Comprehensive color-based analysis for additional insights
- **Interactive Visualizations**: Beautiful charts and graphs using Plotly
- **Real-time Results**: Instant analysis with actionable recommendations

## 🛠️ Technology Stack

- **Backend**: Python, TensorFlow, Streamlit
- **Machine Learning**: Transfer learning with MobileNetV2
- **Visualization**: Plotly for interactive charts
- **Deployment**: Streamlit Community Cloud

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ecovision.git
cd ecovision
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure model files are present:
- `water_best_model.h5` - Water quality model
- `air_best_model.h5` - Air quality model

## 🚀 Local Development

Run the Streamlit app locally:
```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

## 🌐 Deployment to Streamlit Community Cloud

### Prerequisites
- Streamlit Community Cloud account (https://streamlit.io/cloud)
- GitHub repository with your code

### Deployment Steps

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit - EcoVision Environmental Monitoring"
git branch -M main
git remote add origin https://github.com/yourusername/ecovision.git
git push -u origin main
```

2. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app" → "From GitHub"
   - Select your repository
   - Set the main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Environment Setup** (if needed):
   - The app will automatically install dependencies from `requirements.txt`
   - No additional environment variables required

### 📋 Deployment Checklist

- [ ] All model files (`*.h5`) are committed to the repository
- [ ] `requirements.txt` is up to date with all dependencies
- [ ] `streamlit_app.py` is the main entry point
- [ ] Repository is public or you've granted Streamlit access
- [ ] Test the app locally before deployment

## 🎯 Usage

1. **Home Page**: Overview of the system capabilities
2. **Water Quality**: Upload water images for pollution analysis
3. **Air Quality**: Upload air/sky images for air quality assessment

Each analysis provides:
- Pollution level classification (Clean/Little Polluted/Highly Polluted)
- Confidence scores with visual charts
- RGB color analysis
- Actionable recommendations
- Technical details

## 📊 Model Information

### Water Quality Model
- **Classes**: Clean, Little Polluted, Highly Polluted
- **Architecture**: Transfer learning with MobileNetV2
- **Input**: 224x224 RGB images
- **Output**: Classification probabilities

### Air Quality Model  
- **Classes**: Clean, Little Polluted, Highly Polluted
- **Architecture**: Transfer learning with MobileNetV2
- **Input**: 224x224 RGB images
- **Output**: Classification probabilities

## 🔧 Customization

### Adding New Models
1. Train your new model and save as `.h5` file
2. Add model path to `MODEL_PATHS` dictionary
3. Update class names if different
4. Add analysis functions if needed

### Modifying UI
- Edit the Streamlit components in `streamlit_app.py`
- Customize colors, layouts, and text
- Add new pages or features

## 🐛 Troubleshooting

### Common Issues

1. **Model not found**: Ensure `.h5` files are in the correct location
2. **Memory issues**: Large models may need optimization for cloud deployment
3. **Image upload fails**: Check file size limits and supported formats
4. **Slow predictions**: Consider model optimization or caching

### Performance Tips
- Use `@st.cache_resource` for model loading
- Implement image preprocessing optimization
- Consider using smaller model architectures
- Enable Streamlit's built-in caching

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review Streamlit documentation
- Ensure all dependencies are properly installed
- Test with different image types and sizes

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Streamlit for the amazing deployment platform
- TensorFlow for the ML framework
- The environmental monitoring community for inspiration

---

**Live Demo**: [Your Streamlit Cloud URL will appear here after deployment]

**Repository**: https://github.com/yourusername/ecovision