from asyncio import threads
import pandas as pd
import os

REQUIRED_COLUMNS = [
    'Plant / Workshop',
    'Station ID',
    'Task / Operation',
    'Core Industrial Process',
    'Primary Tools & Equipment',
    'Required Technical Skill',
    'Linked Academic / Syllabus Module',
    'Cross-Plant Similar Application (ID)'
]

def validate_and_read_excel(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return False, f"Failed to read file: {str(e)}", None

    if df.empty:
        return False, "The uploaded file is empty.", None

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}", None

    # Keep only required columns
    df = df[REQUIRED_COLUMNS]
    return True, "File valid", df
