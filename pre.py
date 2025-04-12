import json
import csv
import sys

def json_to_csv(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare CSV headers
    headers = ['video_id', 'language', 
               'age_0_9', 'age_10s', 'age_20s', 'age_30s', 'age_40s', 'age_50plus',
               'gender_male', 'gender_female']
    
    # Write to CSV file
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Process each video entry
        for video_id, video_data in data.items():
            # Skip entries where language or predict is null
            if video_data.get('language') is None or video_data.get('predict') is None:
                continue
            row = [video_id, video_data.get('language', '')]
            
            # Extract age predictions
            age_predictions = video_data.get('predict', {}).get('predicted_ages', {})
            row.extend([
                age_predictions.get('0~9세', 0),
                age_predictions.get('10대', 0),
                age_predictions.get('20대', 0),
                age_predictions.get('30대', 0),
                age_predictions.get('40대', 0),
                age_predictions.get('50대 이상', 0)
            ])
            
            # Extract gender predictions
            gender_predictions = video_data.get('predict', {}).get('predicted_genders', {})
            row.extend([
                gender_predictions.get('남', 0),
                gender_predictions.get('여', 0)
            ])
            
            writer.writerow(row)
    
    print(f"CSV file created successfully at {csv_file_path}")

if __name__ == "__main__":
    json_to_csv("data/distribution.json", "data/distribution.csv")