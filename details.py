import time
import json
import pandas as pd

from iCalendar import to_iCalendar
from to_csv import convert_into_csv

df=pd.read_excel("INPUT/VIT-AP_Final_Mess Menu_October 2026.xlsx")
data=df.iloc[:]

food_data={
    "menu":{}
}

# Date check
# for i in range(0, 190):
#     if repr(df.iloc[i, 0]) !="nan":
#         print(i, repr(df.iloc[i, 0]))
date_rows = []

#Date start
for i, value in df.iloc[:, 0].items():
    if isinstance(value, str) and "\n" in value:
        date_rows.append(i)


start=time.time()
for index,s in enumerate(date_rows):
    if index + 1 < len(date_rows):
        n = date_rows[index + 1]
    else:
        n = len(df)
    data=df.iloc[s:n]
    try:
        dates=data.iloc[0,0].replace("\n", " ").split(" ")
    except Exception as e:
        print("Value:", repr(data.iloc[0, 0]))
        print("Type:", type(data.iloc[0, 0]))
        print(f"Error occured: {e}")

    #BreakFast
    breakfast=data.iloc[:,1].replace("\n", " ")
    breakfast_main=list(breakfast.iloc[:6])
    breakfast_beverages=breakfast.iloc[6].split('/')
    breakfast_side=breakfast.iloc[9]

    #Lunch
    lunch=[x for x in list(data.iloc[:,2]) if pd.notna(x)]

    #Snacks
    snacks=data.iloc[:,3]
    nan_count = snacks.isna().sum()
    snacks_main=snacks.iloc[0]

    if len(snacks) - nan_count> 2 and pd.notna(snacks.iloc[2]):
        snacks_side=snacks.iloc[1]
        snacks_beverages = snacks.iloc[2].split("/")
    else:
        snacks_side=snacks.iloc[1]
        snacks_beverages = []

    #Dinner
    dinner=data.iloc[:,4]
    dinner_main=[x for x in list(dinner.iloc[:]) if pd.notna(x)]
    dinner_beverages=dinner_main[-1]
    dinner_main.pop(-1)

    day=dates[0]

    for date in dates[1:]:
        
        date = int(date.strip(","))
                
        food_data["menu"][f'{date}'] = []
        food_data["menu"][f'{date}'].append(
            {
                "day":day,
                "breakfast":{
                    "breakfast_main":breakfast_main,
                    "breakfast_side":breakfast_side,
                    "breakfast_beverages":breakfast_beverages
                },
                "lunch": {
                    "lunch_main": lunch,
                },
                "snacks": {
                    "snacks_main": snacks_main,
                    "snacks_side": snacks_side,
                    "snacks_beverages": snacks_beverages
                },
                "dinner": {
                    "dinner_main": dinner_main,
                    "dinner_beverages": dinner_beverages
                },
            }
        )

sorted_menu = dict(
    sorted(
        food_data["menu"].items(),
        key=lambda item: int(item[0])
    )
)
food_data["menu"] = sorted_menu
with open("output/food.json",'w') as f:
    json.dump(food_data,f,indent=4)
end=time.time()
print(f'Time Taken: {(end-start):.4f} seconds')

print("Menu Saved Successfully")

convert_into_csv()

to_iCalendar()