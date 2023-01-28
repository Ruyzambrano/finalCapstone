#========Import Librariess==========
from tabulate import tabulate
from termcolor import colored

#========The beginning of the class==========
class Shoe:

    #initialise the shoe class
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    #define the get_cost method to return cost
    def get_cost(self):
        return self.cost

    #define the get_quantity method to return quantity
    def get_quantity(self):
        return self.quantity

    #define the __str__ to return the details as a string
    def __str__(self):
        return f"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~
    {self.product}
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Country:    {self.country}
Code:       {self.code}
Cost:       {self.cost}
Quantity:   {self.quantity}
~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """


#=============Shoe list===========
#store a list of objects of shoes.
shoe_list = []

#==========Functions outside the class==============
#open, read and add each line as an object in the list
def read_shoes_data():

    #error handling
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                
                #ignore the first line
                if i == 0:
                    continue

                #split the data into a list
                country, code, product, cost, quantity = line.strip().split(",")

                #check if the numbers are numbers
                try:
                    #cast cost as a float
                    cost = float(cost)

                    #cast quantity as an integer
                    quantity = int(quantity)
                
                    #create an object using a single line of code
                    shoe = Shoe(country, code, product, cost, quantity)
                    
                    #add the object to the shoe_list
                    shoe_list.append(shoe)

                #if the cost or quantity are not numbers, tell the user
                except ValueError as e:
                    print(f"Error: {e}.There is an error in the product input, make sure it is formatted correctly")
                    print("Format must be: " + colored("country, code, product, cost, quantity with no spaces", "red"))
                    return

    #if there is an issue with the file            
    except Exception as e:
        print(f"Error reading file: {e}")

#define the capture shoes function
def capture_shoes():
    while True:    
        #ask the user to input the country of origin, and prompt an error if they do not enter anything
        country = input("\nEnter the country of origin: ")
        while country == "":
            country = input("\nYou have not entered anything.\nEnter the country of origin: ")
        
        #ask the user to input the code of the product and prompt an error for an empty string
        code = input("Enter the code of the shoe: ")
        while code == "":
            code = input("\nYou have not entered anything.\nEnter the code of the shoe: ")

        #as the user to input the name of the shoe and prompt an error for an empty string
        product = input("Enter the name of the product: ")
        while product == "":
            input("\nYou have not entered anything.\nEnter the name of the product")
            product = input("Enter the name of the product: ")

        #check if the product already exists
        for shoe in shoe_list:
            if product in shoe.product:
                print("Product already exists.")
                return

        #check if the code already is being used
        for shoe in shoe_list:
            if code in shoe.code:
                print("Code already in use. Would you like to try again? Y/N")
                code_choice = input(": ").capitalize()

                #error handling
                while code_choice != "Y" and code_choice != "N":
                    print("Incorrect input. Would you like to try again? Y/N")
                    code_choice = input(": ")
            
                #if the user chooses Y, use a while loop until the user either exits or inputs a new code
                while code_choice == "Y":
                    code = input("Enter the code of the shoe: ")

                    #create a variable to track if the code is used
                    is_code_unique = True

                    #iterate through the objects in the list
                    for shoe in shoe_list:

                        #if the code is used, update the is_code_unique variable and stop the iteration
                        if code == shoe.code:
                            is_code_unique = False
                            break
                    #if the code is not used, exit the loop    
                    if is_code_unique:
                        break

                    #if the code is used, ask the user if they would like to try again
                    else:
                        print("Code already in use. Would you like to try again? Y/N")
                        code_choice = input(": ").capitalize()
            
                #if the user chooses N, go back to the menu
                if code_choice == "N":
                    return 
                
                #error handling
                while code_choice != "Y" and code_choice != "N":
                    print("Incorrect input. Would you like to try again? Y/N")
                    code_choice = input(": ")
        
        #use a while block to let the user reenter their numbers
        while True:
            try:
                #ask the user to enter the cost of the shoes
                cost = float(input("Enter the cost of the shoe: "))
                
                #prompt an error if they enter an empty string
                while cost == "":
                    print("\nYou have not entered anything, try again.")
                    cost = float(input("Enter the cost of the shoe: "))
                while cost <= 0:
                    print(f"\nYou cannot charge {cost} for these shoes. Enter a higher number.")
                    cost = float(input("Enter the cost of the shoe: "))
                quantity = int(input("Enter the quantity of the shoe: "))
                while quantity == "":
                    print("\nYou have not entered anything, try again.")
                    quantity = int(input("Enter the quantity of the shoe: "))
                while quantity < 0:
                    print("\nYou cannot enter a negative number.")
                    quantity = int(input("Enter the quantity of the shoe: "))
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
                break
            
            #return an error if the input is not a number
            except ValueError as e:
                print(f"Error: {e}. You have not entered a number, try again.")
            
        #write the data to the file
        try:
            with open("inventory.txt", "w") as file:
                file.write("country,code,product,cost,quantity\n")
                for shoe in shoe_list:
                    file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
            print(f"\n" + colored(f"{product}", "blue") + " has been added.")
            add_more = input("Would you like to add another? Y/N\n: ").capitalize()

        #alert the user to errors in the file name
        except Exception as e:
            print(f"Error writing to file: {e}")

        if add_more == "N":
                return
    
#define the view_all function
def view_all():

    #create an empty list
    data= []

    #set the data into an array
    for shoe in shoe_list:
        data.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])
    
    #set the headers for the table
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    
    #display the data
    print(tabulate(data, headers, tablefmt="fancy_grid"))


def re_stock():

    #define a variable that will keep the lowest quantity, set to infinity
    lowest_quantity = float("inf")
    
    #define a variable to hold the lowest quantity shoe object
    lowest_shoe = None

    #iterate through the shoe list
    for shoe in shoe_list:

        #if the shoe is lower than the previous, place it in the lowest_shoe variable
        if shoe.quantity < lowest_quantity:
            lowest_quantity = shoe.quantity
            lowest_shoe = shoe
    
    #if all the shoes are the same quantity, it must be fully stocked
    if lowest_shoe is None:
        print("\nAll shoes are fully stocked.")
        return

    #alert the user and ask if they would like to restock
    add_query = input(f"\n{lowest_shoe.product} is running low.\nDo you want to re-stock? Y/N\n: ").capitalize()
    
    #make sure the user has put in the correct input
    while add_query not in ["Y", "N"]:
        add_query = input("Invalid input. Please enter Y or N: ").capitalize()

    #if yes
    if add_query == "Y":
        #I assumed that 90 is a good amount of stock for each shoe
        lowest_shoe.quantity = 90
        
        #open the inventory file and update the inventory
        try:
            with open("inventory.txt", "w") as file:
                file.write("country,code,product,cost,quantity\n")
                for shoe in shoe_list:
                    file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
            print("\n" + colored(f"{lowest_shoe.product}", "blue") + " has been restocked.")
        #alert the user to errors in the file name
        except Exception as e:
            print(f"Error writing to file: {e}")

#define the search_shoe method
def search_shoe():

    #ask the user to enter the code they want to find
    code = input("\nEnter the code of the shoe you want to search for: ")
    
    #iterate through the list and return the correct shoe
    for shoe in shoe_list:
        if shoe.code == code:
            print(shoe)
            return
            
    #if the code is incorrect, let the user know 
    print("Shoe not found.")

#define the value_per_item method
def value_per_item():

    #create a table to display
    table = []

    #iterate through the shoe_list to find the value per item
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity

        #add the item to the table
        table.append([shoe.code, shoe.product, value])
    
    #display the results
    print(tabulate(table, headers=["Code", "Product", "Value in £"], tablefmt="fancy_grid"))

#define the highest_qty method
def highest_qty():
    #search the shoe_list for the largest quantity
    highest_qty = max(shoe.quantity for shoe in shoe_list)
    
    #create a list for tabulate
    shoes = []

    #iterate through the shoe_list to find the shoes with the highest quantity (if there are multiple)
    for shoe in shoe_list:
        if shoe.quantity == highest_qty:
            shoes.append(shoe)

    #present the results in a table        
    print(tabulate([shoe.__dict__ for shoe in shoes], headers='keys', tablefmt="fancy_grid"))

#==========Main Menu=============
def main():

    #read the data and create a list
    read_shoes_data()
    
    while True:
        
        print(colored("\n\t\tNike Warehouse", "red", None, ["bold", "underline"]))
        print("\nChoose an option - ")
        print(colored("1 - View all shoes", "green"))
        print(colored("2 - Search for a shoe", "blue"))
        print(colored("3 - Restock shoes", "magenta"))
        print(colored("4 - Check value per item", "yellow"))
        print(colored("5 - Find the highest quantity", "cyan"))
        print(colored("6 - Add a new product", "white"))
        print(colored("quit - Quit\n", "dark_grey"))
        choice = input(":").lower()

        if choice == "1":
            view_all()
        elif choice == "2":
            search_shoe()
        elif choice == "3":
            re_stock()
        elif choice == "4":
            value_per_item()
        elif choice == "5":
            highest_qty()
        elif choice == "6":
            capture_shoes()
        elif choice == "quit":
            print(colored("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "yellow"))
            print(colored("\n\t\tLogging Off\n", "yellow"))
            print(colored("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "yellow"))
            exit()
        else:
            print(colored("\nIncorrect input, try again\n", "red"))

main()