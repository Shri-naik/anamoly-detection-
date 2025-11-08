#!/usr/bin/env python3
"""
EcoVision Final Validation Script
"""

import os
import sys
import importlib.util

def validate_imports():
    """Validate all required imports"""
    print("🔍 Validating imports...")
    
    required_packages = [
        'streamlit',
        'tensorflow',
        'numpy', 
        'PIL',
        'plotly'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    return len(missing) == 0

def validate_files():
    """Validate required files"""
    print("\n📁 Validating files...")
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'water_best_model.h5',
        'air_best_model.h5',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing.append(file)
            print(f"❌ {file}")
    
    return len(missing) == 0

def validate_models():
    """Basic model validation"""
    print("\n🤖 Validating models...")
    
    try:
        import tensorflow as tf
        
        # Test water model
        if os.path.exists('water_best_model.h5'):
            model = tf.keras.models.load_model('water_best_model.h5')
            print(f"✅ Water model loaded: {model.input_shape} → {model.output_shape}")
        
        # Test air model  
        if os.path.exists('air_best_model.h5'):
            model = tf.keras.models.load_model('air_best_model.h5')
            print(f"✅ Air model loaded: {model.input_shape} → {model.output_shape}")
            
        return True
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

def main():
    """Main validation function"""
    print("🌍 EcoVision Validation")
    print("=" * 30)
    
    all_passed = True
    
    all_passed &= validate_imports()
    all_passed &= validate_files()
    all_passed &= validate_models()
    
    print("\n" + "=" * 30)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("🚀 Ready for Streamlit deployment!")
        print("\nNext steps:")
        print("1. Deploy to Streamlit Community Cloud")
        print("2. Test the deployed app")
        print("3. Share your live demo!")
    else:
        print("❌ Some validations failed")
        print("Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()