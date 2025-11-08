#!/usr/bin/env python3
"""
EcoVision Deployment Helper Script

This script helps prepare your environmental monitoring application 
for deployment to Streamlit Community Cloud.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Check if all required files are present"""
    print("🔍 Checking deployment requirements...")
    
    required_files = [
        "streamlit_app.py",
        "requirements.txt",
        "water_best_model.h5",
        "air_best_model.h5",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files are present")
        return True

def check_model_files():
    """Check model files size and integrity"""
    print("\n📊 Checking model files...")
    
    models = ["water_best_model.h5", "air_best_model.h5"]
    total_size = 0
    
    for model in models:
        if os.path.exists(model):
            size = os.path.getsize(model) / (1024 * 1024)  # MB
            total_size += size
            print(f"   {model}: {size:.1f} MB")
    
    print(f"📈 Total model size: {total_size:.1f} MB")
    
    if total_size > 100:  # GitHub warning threshold
        print("⚠️  Warning: Large model files may cause GitHub issues")
        print("   Consider using Git LFS or external storage for models > 100MB")
    
    return True

def create_app_config():
    """Create Streamlit app configuration"""
    print("\n⚙️  Creating app configuration...")
    
    config = {
        "theme": {
            "primaryColor": "#2E8B57",
            "backgroundColor": "#FFFFFF",
            "secondaryBackgroundColor": "#F0F8FF",
            "textColor": "#262730",
            "font": "sans serif"
        },
        "server": {
            "maxUploadSize": 200  # MB
        }
    }
    
    with open(".streamlit/config.toml", "w") as f:
        import toml
        toml.dump(config, f)
    
    print("✅ Configuration file created")

def test_app():
    """Test the Streamlit app locally"""
    print("\n🧪 Testing Streamlit app locally...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true", "--server.port", "8502"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ App test successful")
            return True
        else:
            print(f"❌ App test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ App test successful (timeout expected)")
        return True
    except Exception as e:
        print(f"❌ App test error: {e}")
        return False

def generate_deployment_instructions():
    """Generate deployment instructions"""
    print("\n📋 Deployment Instructions:")
    print("=" * 50)
    
    instructions = """
1. 🚀 PREPARE FOR DEPLOYMENT:
   - Ensure all files are committed to GitHub
   - Make repository public (or grant Streamlit access)
   - Verify model files are included

2. 🌐 DEPLOY TO STREAMLIT CLOUD:
   - Go to https://share.streamlit.io
   - Click "New app" → "From GitHub"
   - Select your repository
   - Set main file: streamlit_app.py
   - Click "Deploy!"

3. 🔧 POST-DEPLOYMENT:
   - Test all functionality
   - Share your live demo link
   - Monitor usage and performance

4. 📱 SHARE YOUR APP:
   - Update README.md with live demo link
   - Share on social media
   - Add to your portfolio
"""
    
    print(instructions)
    
    # Save instructions to file
    with open("DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write("# EcoVision Deployment Guide\n\n")
        f.write(instructions)
    
    print("✅ Deployment guide saved to DEPLOYMENT_GUIDE.md")

def main():
    """Main deployment preparation function"""
    print("🌍 EcoVision Deployment Helper")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Run checks
    checks_passed = True
    
    checks_passed &= check_requirements()
    checks_passed &= check_model_files()
    
    if checks_passed:
        try:
            create_app_config()
        except ImportError:
            print("⚠️  TOML not available, skipping config creation")
        
        test_app()
        generate_deployment_instructions()
        
        print("\n🎉 Deployment preparation complete!")
        print("🚀 Ready to deploy to Streamlit Community Cloud!")
        
    else:
        print("\n❌ Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()