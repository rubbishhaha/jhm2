import pandas, os
from datetime import date as dt
import plotext as plt

choice = 0
sort = "default"
rerun = False

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

def plot(dataset):
    plot_data = dataset.sort_values(by=["category"]).loc[:,["category","amount"]].to_dict("split")["data"]
    a=1
    for i in range(len(plot_data)):
        if plot_data[i+1-a][0] == plot_data[i-a][0]:
            plot_data[i+1-a][1] += plot_data[i-a][1]
            plot_data.pop(i-a)
            a+=1
    column,row = [],[]
    for i in plot_data:
        column.append(i[0])
        row.append(i[1])
    plt.theme("window")
    plt.bar(column,row,orientation = "horizontal",width = 0.3)
    plt.title("amount in each category")
    plt.show()




while choice != 4:
    os.system('cls' if os.name == 'nt' else 'clear')
    if rerun == False:
        choice = int(input("\n\nPlease type your action\n 1.import \n 2.delete \n 3.summary \n 4.exit and save\n 5.clear all data\n 6.edit\n 7.plot graph\n\naction:"))
    else:
        rerun = False
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
        print("sort by",sort)
        print(dataset)
        summary(dataset)
        if input("press space -> enter edit sort\n") == " ":
            rerun = True
            sort = input("sort(column):")
            dataset.sort_values(by=[str(sort)],inplace=True)
            dataset.reset_index(drop=True,inplace=True)
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
        if column == "date" or "category":
            value = input(f"New {column}:") 
        if column == "amount":
            value = int(input(f"New {column}:"))
        if column == "type":
            if input(f"New {column}(in/out):") == "in":
                value = "income"
            elif input(f"New {column}(in/out):") == "in":
                value = "expense"
        dataset.at[row,column] = value
    elif choice == 7:
        plot(dataset)
        input()
dataset.to_csv('data.csv', index=False)