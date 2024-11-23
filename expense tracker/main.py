import pandas, os
choice = 0
if os.path.exists('data.csv'):
    dataset = pandas.read_csv("data.csv").to_dict()
else:
    dataset = pandas.DataFrame(columns=["date","category","amount","type"]).to_dict()
for u in dataset:
    n = dataset[u]
    w = []
    for o in n:
        w.append(n[o])
    dataset[u] = w
print(dataset)

while choice != 3:
    choice = int(input("\n\nchoice \n 1.import \n 2. summary \n 3.exit and save\n"))
    
    if choice == 1:
        dataset["date"].append(input("date:"))
        dataset["category"].append(input("category:"))
        dataset["amount"].append(int(input("amount:")))
        dataset["type"].append(input("type(out/in):"))
        input("")
    if choice == 2:
        print(pandas.DataFrame(dataset))
        total = 0
        for i in range(len(dataset["amount"])):
            if dataset["type"][i] == "in":
                total += dataset["amount"][i]
            if dataset["type"][i] == "out":
                total -= dataset["amount"][i]
        print(f"\n\n---total expense:{total}")
        input("")

dataset = pandas.DataFrame(dataset)
dataset.to_csv('data.csv', index=False) 

        