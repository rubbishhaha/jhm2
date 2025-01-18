want_snacks = input("Do you want some snacks? (yes/no):")                   #Input yes or no to enter next stage.

if want_snacks == "no":                                                         #Situation for no   -> play games
    print("Good! Let's play games instead.")

elif want_snacks == "yes":                                                      #Situation for yes  -> choose snacks

    choice = input("Enter your choice(ice-cream / cookies / candies):")             #Input which snacks is needed

    if choice == "ice-cream":                                                       #Snacks and respective dialogues
        print("Remember to wash your hands.")
    elif choice == "cookies":
        print("Can you share with your friends?")
    elif choice == "candies":
        print("Don't eat too much.")
