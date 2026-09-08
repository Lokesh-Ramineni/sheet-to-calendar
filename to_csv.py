from datetime import datetime, timedelta
import csv
import json

data=None   
try:
    with open("output/food.json","r") as f:
        data = json.load(f)
except FileNotFoundError as e:
    print(f'File not found at the location: {e}')
    


start_date = datetime(2026, 9, 1)
meal_times = {
    'breakfast': ('07:00', '09:00'),
    'lunch': ('12:30', '14:15'),
    'snacks': ('16:30', '18:15'),
    'dinner': ('19:15', '21:00'),
    'special':('07:15','09:15')
}


rows = []
if data is not None:
    for day_num_str, day_data_list in data['menu'].items():
        day_num = int(day_num_str)
        current_date = start_date + timedelta(days=day_num - 1)
        date_str = current_date.strftime('%Y-%m-%d')

        day_data = day_data_list[0]
        for meal_type in ['breakfast', 'lunch', 'snacks', 'dinner']:
            if meal_type not in day_data:
                continue

            items = []
            day=day_data["day"]
            for key, value in day_data[meal_type].items():
                if isinstance(value, list):
                    items.extend(value)
                elif isinstance(value, str):
                    items.append(value)

            items_text = ' | '.join(item.strip() for item in items if item.strip())
            if((day == "Mon" or day =="Sun") and meal_type=='breakfast'):
                start_time, end_time = meal_times['special']
            else:
                start_time, end_time = meal_times[meal_type]

            rows.append({
                'Subject': f'{meal_type.capitalize()} - Day {day_num}',
                'Start Date': date_str,
                'Start Time': start_time,
                'End Date': date_str,
                'End Time': end_time,
                'Description': items_text,
                'Location': '',
                'All Day Event': 'False'
            })

    with open('output/CSV/september_menu_calendar.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date',
                    'End Time', 'Description', 'Location', 'All Day Event']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)  