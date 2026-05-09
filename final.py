import sys
import json
import pickle


def bill_organizer(bills, name, amount, date, number):
    """
    number is a variable that'll be introduced within the Bills class it will refer
    to a counting up sequence that contains what is basically the bill's ID number
    """
    bills[number] = {"Company/Name":name, "Amount": amount, "Date Due" : date}
    """
    Number is assigned as the top level key. within that key is a nested dictionary with the values required by the function
    This prevents the key value combo being replaced if the user adds another bill from the same company
    """


    return bills




"""
bill_searcher is needed to be used within the Bills class as it sorts through all the keys and searches
for matches with the given values so far it should work well but I still need to test it within the class and call it
possibly might need some more refinement
"""
def bill_searcher(bills, name, amount, date):

    #This takes in the inputs and sorts them into a list. These will be used to crosscheck against the other list

    needed_values = [name, amount, date]

    #This turns the upper level dictionary keys into a list that can be crosschecked with the values that we're looking for
    bill_key_list = list(bills.keys())
    
    #A for loop to be able to look through the entire list of values in the dictionary
    for i in bill_key_list:
        

        #This makes a list of the values within the upper level key, it includes the name, amount, and date of each key
        checking_list = list(bills[bill_key_list[i-1]].values())
        
        """
        this if statement looks to see if the values match up with those that we're looking for
        If it matches up it returns the upper level key that was needed to obtain it
        If it doesn't it just passes

        
        Once it runs through the entire list and if there's still nothing found it will raise a value error due to 
        no bills being found
        """
        if all(x in checking_list for x in needed_values):
            number = bill_key_list[i-1]
            return number
        elif i >= len(checking_list):
            raise ValueError("Couldn't find the bill you were looking for")
        
        else:
            pass



"""
The bill class takes in an initial bill, this creates a single entry into the dictionary holding all the info.
Then the dictionary is used further along to do different functions that might be useful to the end user including
how much they owe in total, adding or paying off other bills(currently needs to be finished)

A few other layers of functionality should be added by the end but for right now everything that's fully completed should work
"""

class Bills():

    #This initializeds the class creating the universal variables needed later down the line. 

    def __init__(self, bill_name, date, amount):
        self.bill_name = bill_name
        self.date = date

        #This creates an empty list that will add in the number the user put in the amount variable.
        # If it's not a float it will be converted into one
        self.amount = []
        self.amount.append(float(amount))
       
       #running counter of all the bills helps keep track of how many there have been in total
        self.number = 1 

        #An empty dictionary that can be passed through to the function bill_organizer made earlier
        self.bills = {}
        self.bills = bill_organizer(self.bills, self.bill_name, self.amount[0], self.date, self.number)

        #Creates the variable here so it can be used later in multiple other functions
        #This will store how much has been paid.
        self.paid = 0

    """
    This method works to add a new bill. It will ask the user 3 questions in order to determine what
    information should be carried by the bill. It will the append this information to the dictionary creating
    a new key and value pair
    """
    def add(self):
        self.number += 1 
        self.bill_name = input("What is the name of the company the bill is for?: ")
        self.amount.append(float(input("How much is the bill?: ")))
        self.date = input("What's the date of the bill? ")
        self.bills = bill_organizer(self.bills, self.bill_name, self.amount[0-1], self.date, self.number)
        print(self.bills)

    #This method works to add all the values of the amount variable and subtract them from the paid variable.
    # It then rounds it to the nearest 2 decimal points
    def owed(self):
        total = sum(self.amount)
        total -= self.paid
        total = round(total, 2)
        print(f"Your outstanding amount is ${total}")
    
    #This method returns the amount of bills still owed in a simple numerical form
    def quantity(self):
        print(f"The total number of bills you currently owe are: {len(list(self.bills.keys()))}")
    
    """
    This function is how the bills are paid. It asks the user about the information regarding the bill
    This includes the date the name of the entity and the amount that was owed
    It then takes this information and asks the user if they'd want to pay a partial amount or all of the bill

    Using that information it passes it to the function made earlier bill_searcher
    """
    def pay(self):
        pay_date = input("What's the date that the bill you want to pay was due?: ")
        pay_name = input("What's the name of the company/person that you're paying?: ")
        pay_amount = float(input("How much was the bill for?: "))
        pay_total = input("Are you going to pay the entire bill? (Y/N): ")
        number = bill_searcher(self.bills, pay_name, pay_amount, pay_date)
        print(number)

        #This if statement looks at what the user selected and either subtracts the partial amount
        # or deletes the key value pair if it's been fully paid in one go.
        if pay_total == "Y" : 
            self.paid += pay_amount
            del self.bills[number]
            print(f"You've just paid {pay_name} a total of {pay_amount} \\ It's now been removed from the records")
            

            
        elif pay_total == "N" :
            partial_amount = float(input("How much would you like to pay for this bill?: "))
            if partial_amount >= self.bills[number]['Amount']:
                raise ValueError("You've paid more or the entire bill! rerun this and select (Y)")
            self.paid += partial_amount
            self.bills[number]['Amount'] -= partial_amount
            self.bills[number]['Amount'] = round(self.bills[number]['Amount'], 2)
            print(f"You've just paid {partial_amount}, your remaining balance is {self.bills[number]['Amount']}")
            

        else:
            raise ValueError("Please retry response and answer with (Y/N)")
    

    #This provides a list of all the bills, their names, amounts, and numbers
    #It gives information to the user that can be used to identify them later
    def list_bills(self):
        return (f" The list of currently owed bills is: {list(self.bills.values())}")
    
def main():
    user_choice = input("What would you like to do today (Input the letter corresponding to the action)\n"\
                         "A. Create a new dictionary \n B. Add to an existing dictionary \n" \
                        "C. Check current balance \nD. Pay outstanding bills \nE. Check how many bills are outstanding\n")
    if user_choice == "A":
        bill_name = input("WARNING THIS WILL OVERRIDE YOUR PREVIOUS DIRECTORY \n" \
        "What's the name of the company/person that the bill is to?: ")
        bill_date = input("What is the date that the bill is due?: ")
        bill_amount = input("How much is the bill?: ")
        current_bills =  Bills(bill_name, bill_date, bill_amount)
        with open('data.pickle', 'wb') as f:
            pickle.dump(current_bills, f, pickle.HIGHEST_PROTOCOL)
        return current_bills.list_bills()
    
    elif user_choice == "B":

        with open('data.pickle', 'rb') as f:
            current_bills = pickle.load(f)

        current_bills.add()
        
        with open('data.pickle', 'wb') as f:
            pickle.dump(current_bills, f, pickle.HIGHEST_PROTOCOL)

        return 

    elif user_choice == "C":

        with open('data.pickle', 'rb') as f:
            current_bills = pickle.load(f)
        
        current_bills.owed()

        return 
    
    elif user_choice == "D":

        with open('data.pickle', 'rb') as f:
            current_bills = pickle.load(f)
        
        current_bills.pay()

        with open('data.pickle', 'wb') as f:
            pickle.dump(current_bills, f, pickle.HIGHEST_PROTOCOL)

        return 
    
    elif user_choice == "E":

        with open('data.pickle', 'rb') as f:
            current_bills = pickle.load(f)

        return current_bills.list_bills()
    
    else:
        raise ValueError("No correct answer entered, please try again")


if __name__ == "__main__":


    main()