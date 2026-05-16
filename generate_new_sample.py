import pandas as pd
import os

def create_sample():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_data = {
        'Plant / Workshop': ['Pune - TCF', 'Pune - Engine', 'Jamshedpur - TCF', 'Jamshedpur - Body Shop'],
        'Station ID': ['TCF-01', 'ENG-08', 'TCF-01', 'BODY-12'],
        'Task / Operation': ['Wheel Assembly', 'Engine Mounting', 'Wheel Assembly', 'Panel Welding'],
        'Core Industrial Process': ['Fastening', 'Assembly', 'Fastening', 'Welding'],
        'Primary Tools & Equipment': ['Torque Wrench', 'Torque Wrench', 'Pneumatic Gun', 'Welding Torch'],
        'Required Technical Skill': ['Level 2', 'Level 3', 'Level 2', 'Level 4'],
        'Linked Academic / Syllabus Module': ['Torque Calculation', 'Torque Calculation', 'Fastening Techniques', 'Welding Basics'],
        'Cross-Plant Similar Application (ID)': ['Pinch Point Safety', 'Heavy Lifting', 'Noise Hazard', 'Eye Protection']
    }
    
    df = pd.DataFrame(sample_data)
    sample_path = os.path.join(base_dir, 'dample.xlsx')
    
    df.to_excel(sample_path, index=False)
    print(f"Sample Excel created at {sample_path}")

if __name__ == "__main__":
    create_sample()
