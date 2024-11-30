import pandas, os
from datetime import date as dt

choice = 0

if os.path.exists('data.csv'):
    dataset = pandas.read_csv("data.csv")
else:
    dataset = pandas.DataFrame(columns=["date","category","amount","t_type"])

def merge(date,category,amount,t_type):
    if date == "":
        date = dt.today()
    if t_type == "in":
        t_type = "income"
    elif t_type == "out":
        t_type = "expense"
        amount = -amount
    
    return [date,category,amount,t_type]
   # new_dataset = pandas.DataFrame([[date,category,amount,t_type]], columns=["date","category","amount","t_type"])
   # dataset = pandas.concat([dataset, new_dataset], ignore_index=True)

def summary(dataset):
    total_amount = dataset["amount"].sum()    
    total_expense = dataset[dataset['amount'] < 0]["amount"].sum()
    total_income = dataset[dataset['amount'] > 0]["amount"].sum()
    maximum_expense = dataset["amount"].min()
    maximum_income = dataset["amount"].max() 
    print(f"----------------------------------------\n Total saving:{total_amount}\n Total income:{total_income}\n Total expense:{total_expense}\n Maximum income:{maximum_income}\n Maximum expense:{maximum_expense}")

while choice != 4:
    os.system('cls' if os.name == 'nt' else 'clear')
    choice = int(input("\n\nPlease type your action\n 1.import \n 2.delete \n 3.summary \n 4.exit and save\n 5.clear all data\n 6.edit\n\naction:"))
    
    if choice == 1:
        dataset.loc[len(dataset)] = merge(input("date(blank for today):"),input("category:"),int(input("amount:")),input("type(in/out):"))
    elif choice == 2:
        print(dataset)
        print("----------------------------------------")
        row = int(input("Row:"))
        sure = input(f"Are you sure to delete following data?(press enter to continue, press q -> enter to cancel) \n {dataset.iloc[row]} \n")
        if sure != "q":
            dataset.drop(row,inplace=True)
            dataset.reset_index(drop=True,inplace=True)
    elif choice == 3:
        print(dataset)
        summary(dataset)
        input()
    elif choice == 5:
        sure = input("Are you sure to delete ALL data?(press enter to continue, press q -> enter to cancel)\n")
        if sure != "q":
            sure = input("Are you REALLY sure to delete ALL data?(press enter to continue, press q -> enter to cancel)\n")
            if sure != "q":
                dataset = pandas.DataFrame(columns=["date","category","amount","t_type"])
    elif choice == 6:
        print(dataset)
        print("----------------------------------------")
        row = int(input("row:"))
        column = str(input("column:"))
        dataset.at[row,column]
dataset.to_csv('data.csv', index=False)