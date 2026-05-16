import os
import urllib.request
import pandas as pd

def setup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dirs = [
        "modules",
        "templates",
        "static/css",
        "static/js",
        "uploads"
    ]
    
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    urls = {
        "static/css/bootstrap.min.css": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "static/js/bootstrap.bundle.min.js": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
    }

    for path, url in urls.items():
        full_path = os.path.join(base_dir, path)
        if not os.path.exists(full_path):
            try:
                urllib.request.urlretrieve(url, full_path)
                print(f"Downloaded {path}")
            except Exception as e:
                print(f"Error downloading {path}: {e}")

    # Generate sample Excel file
    sample_data = {
        'Plant': ['Pune', 'Pune', 'Jamshedpur', 'Jamshedpur'],
        'Workshop': ['TCF', 'Engine', 'TCF', 'Body Shop'],
        'Station_No': ['TCF-01', 'ENG-08', 'TCF-01', 'BODY-12'],
        'Process_Name': ['Wheel Assembly', 'Engine Mounting', 'Wheel Assembly', 'Panel Welding'],
        'Tool_Used': ['Torque Wrench', 'Torque Wrench', 'Pneumatic Gun', 'Welding Torch'],
        'Skill_Required': ['Level 2', 'Level 3', 'Level 2', 'Level 4'],
        'Theory_Module': ['Torque Calculation', 'Torque Calculation', 'Fastening Techniques', 'Welding Basics'],
        'Safety_Concept': ['Pinch Point Safety', 'Heavy Lifting', 'Noise Hazard', 'Eye Protection']
    }
    df = pd.DataFrame(sample_data)
    sample_path = os.path.join(base_dir, 'sample_mapping.xlsx')
    if not os.path.exists(sample_path):
        df.to_excel(sample_path, index=False)
        print(f"Sample Excel created at {sample_path}")

if __name__ == "__main__":
    setup()
