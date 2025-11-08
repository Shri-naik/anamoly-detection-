# setup.py
import os

folders = [
    "data/air",
    "data/water",
    "data_processed/air",
    "data_processed/water",
    "notebooks",
    "src/utils",
    "experiments",
]

readme_text = """# Anomaly Detection in Air and Water Quality using Deep Learning

Structure created by setup.py.

Next steps:
1. Put dataset images into `data/air` and `data/water` (organized into subfolders per class if classification).
2. Run preprocessing script to resize/augment images -> `data_processed/`.
3. Train the CNN model with `src/train.py`.
"""

def create_structure():
    for f in folders:
        os.makedirs(f, exist_ok=True)
        print(f"Ensured: {f}")
    with open("README.md", "w") as f:
        f.write(readme_text)
    print("README.md created. Project skeleton ready.")

if __name__ == "__main__":
    create_structure()
