import time
import pandas as pd
import json
import csv
df=pd.read_excel("INPUT/VIT-AP_Final Mess Menu_September 2026.xlsx")
data=df.iloc[:]
s=2
n=15
step=13

food_data={
    "menu":{}
}
start=time.time()
while n<=184:
    data=df.iloc[s:n]
    try:
        dates=data.iloc[0,0].replace("\n", " ").split(" ")
    except Exception as e:
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


    for date in dates[1:]:
        food_data["menu"][date.strip(",")] = []
        food_data["menu"][date.strip(",")].append(
            {
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


    s=n
    n=n+step

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
print(end-start)

print("working")


