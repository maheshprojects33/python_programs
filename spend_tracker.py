import json


def menu():
    print("""
    ########## Welcome To Spend Tracker App ##########
    1. Create an Account
    2. Login with your Account
    3. Reset your Password
    4. About Spend Tracker
    5. Exit
    """)


def user_menu(email, name):
    print(f"""
    ########## Welcome To Spend Tracker '{name}' ##########
    1. Add Your Budget
    2. Edit Your Budget
    3. View Your Budget
    4. Add Your Expenses
    5. Edit Your Expenses
    6. View Your Expenses
    7. View Your Balance
    8. Log Out
    """)


def about():
    print("* " * 55)
    print("""*                        - - - - - - - - - - About SpendTracker - - - - - - - - - -                         *
*                                                                                                           *                                                      
*   'SpendTracker' is a user-friendly application that helps users to easily track their expenses and       *
*   manage their budget. With 'SpendTracker', you can easily enter your expenses as you make them, and      *
*   categorize them for easy tracking. Whether you are trying to save money, pay off debt, or simply        *
*   gain a better understanding of your spending habits, This is the perfect app to help you reach your     * 
*   financial goals. With SpendTracker, you can take control of your finances and make informed decisions   *
*   about your money.                                                                                       *
*                                                                                                           *""")
    print("* " * 55)



def go_back_to_menu():
    input("Press Enter to go back to Main Menu")
    menu()


def go_back_to_user_menu():
    input("Press Enter to go back to User Menu")



class Account:
    def __init__(self, name, email, password1, password2):
        self.name = name
        self.email = email
        self.password1 = password1
        self.password2 = password2

    def create_user(self):
        if "@" not in self.email:
            print("*** ERROR!!! Please Enter Valid Email ID ***\n")
            return
        if self.password1 != self.password2:
            print("*** ERROR!!! Password Doesn't Matched ***\n")
            return

        try:
            with open("accounts.json", 'r') as f:
                data = json.load(f)

                if self.email in data:
                    print("*** ERROR!!! User Already Exists ***\n")
                    return
        except FileNotFoundError:
            data = {}

        data[self.email] = {
            "name": self.name,
            "password": self.password1
        }

        with open("accounts.json", 'w') as f:
            json.dump(data, f, indent=4)
            print("*** SUCCESS!!! Account created ***\n")

    def login_user(self):
        with open("accounts.json", 'r') as f:
            data = json.load(f)

        if self.email in data:
            if data[self.email]["password"] == self.password1:
                name = data[self.email]["name"]
                user_menu(self.email, name)
                return True, name
            else:
                print("*** ERROR!!! Incorrect password ***\n")
                return False
        else:
            print("*** ERROR!!! No Account Found With That Email ***\n")
            return False

    def reset_password(self):
        with open("accounts.json", 'r') as f:
            data = json.load(f)

        if self.email in data:
            while True:
                if data[self.email]["password"] == self.password1:
                    new_password1 = input("Enter Your New Password: ")
                    new_password2 = input("Confirm Your New Password: ")
                    if new_password1 != new_password2:
                        print("*** ERROR!!! New Password Doesn't Matched, Try Again *** \n")
                    else:
                        with open("accounts.json", 'w') as f:
                            data[self.email]['password'] = new_password1
                            json.dump(data, f, indent=4)
                            print(f"*** SUCCESS!!! Your Password Has Been Successfully Changed *** \n")
                            break
                else:
                    print("*** ERROR!!! Old Password Doesn't Matched, Try Again ***\n")
                    self.password1 = input("Enter Your Old Password: ")
                    continue
        else:
            print("*** ERROR!!! Email ID Not Found To Reset Your Password ***\n")


class Calculation:
    def __init__(self, email):
        self.email = email
        self.total_budget = 0
        self.budget = 0
        self.budget_remark = ""
        self.expense = 0
        self.expense_remark = ""

    def add_budget(self, budget, budget_remark):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # add or update user budget
        user_data = data.get(self.email, {})
        user_budget = user_data.get("total_budget", {})
        user_expenses = user_data.get("total_expenses", {})

        # add new budget to user data
        last_budget_num = int(max(user_budget.keys()).split('_')[-1]) if user_budget else 0
        new_budget_num = last_budget_num + 1
        user_budget[f"budget_{new_budget_num}"] = {"budget": budget, "remarks": budget_remark}
        if not user_expenses:
            user_expenses[f"expense_0"] = {"expense": self.expense, "remarks": self.expense_remark}

        # Delete budget_0 if exists
        if 'budget_0' in user_budget:
            del user_budget['budget_0']

        # update data with new user expenses
        user_data['total_budget'] = user_budget
        data[self.email] = user_data
        user_data['total_expenses'] = user_expenses
        data[self.email] = user_data

        # save data to records.json
        with open("records.json", 'w') as f:
            json.dump(data, f, indent=4)

    def edit_budget(self):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found *** \n")
            return

        if self.email not in data:
            print("*** EMPTY_DATA!!! Records Not Found To Edit!!! *** \n")

        else:
            count_data = []
            for count in data[self.email]["total_budget"].values():
                count_data.append(count)

            # To validate User Input For Edit
            while True:
                try:
                    edit = int(input(f"Enter respective S.No. to Edit Your Budget (Should be 1 to {len(count_data)}): "))
                    if edit <= 0:
                        print("*** ERROR!!! Value Should note be less than 1 ***\n")
                    elif edit > len(count_data):
                        print(f"*** ERROR!!! Record Not Found for Budget S.No. {edit} ***\n")
                    else:
                        break
                except ValueError:
                    print("*** ERROR!!! Enter respective S.No. to Edit Your Budget ***\n")

            # Logic starts for edit
            if count_data[edit - 1]:
                budget_nos = []
                data_list = data[self.email]['total_budget'].keys()
                for key in data_list:
                    budget_nos.append(key)
                budget_no = (budget_nos[edit - 1])

                old_amount = data[self.email]["total_budget"][budget_no]['budget']
                old_remark = data[self.email]["total_budget"][budget_no]['remarks']

                # Getting New Values from User
                while True:
                    try:
                        print(f'\n*** DATA!!! Your Existing Budget Amount was "{old_amount}" ***')
                        new_amount = float(input("Edit Your Budget Amount: "))
                        if new_amount < 0:
                            print("*** ERROR!!! Amount Must Be Greater Than 0 ***\n")
                        else:
                            print(f'\n*** DATA!!! Your Existing Budget Remark was "{old_remark}" ***')
                            new_remark = input("Edit Your Remarks: ")
                            # Assigning Edited data to dictionary
                            data[self.email]["total_budget"][budget_no]['budget'] = new_amount
                            data[self.email]["total_budget"][budget_no]['remarks'] = new_remark
                            print("*** SUCCESS!!! Your Data Has Been Successfully Edited ***\n")
                            break
                    except ValueError:
                        print("*** ERROR!!! Amount Must Be A Number ***\n")

                with open("records.json", 'w') as f:
                    json.dump(data, f, indent=4)

    def delete_budget(self):
        try:
            with open("records.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found ***\n")

        if self.email not in data:
            print("*** EMPTY_DATA!!! Records Not Found To Edit!!! *** \n")
        else:
            count_data = []
            for count in data[self.email]["total_budget"].values():
                count_data.append(count)

            # To validate User Input For Delete
            while True:
                try:
                    delete = int(
                        input(f"Enter respective S.No. to Edit Your Budget (Should be 1 to {len(count_data)}): "))
                    if delete <= 0:
                        print("*** ERROR!!! Value Should note be less than 1 ***\n")
                    elif delete > len(count_data):
                        print(f"*** ERROR!!! Record Not Found for Budget S.No. {delete} ***\n")
                    else:
                        break
                except ValueError:
                    print("*** ERROR!!! Enter respective S.No. to Edit Your Budget ***\n")

            # Logic To Delete data
            if count_data[delete - 1]:
                budget_nos = []
                data_list = data[self.email]['total_budget'].keys()
                for key in data_list:
                    budget_nos.append(key)
                budget_no = (budget_nos[delete - 1])
                amount_to_del = data[self.email]["total_budget"][budget_no]['budget']
                remark_to_del = data[self.email]["total_budget"][budget_no]['remarks']

                # Get confirmation from user
                print("\nYour Existing Budget: ", amount_to_del)
                print("Your Existing Remark: ", remark_to_del)
                conformation = input(f"Are You Sure You Want To Delete Above Data (y/n): ").lower()

                if conformation == "y":
                    data[self.email]["total_budget"].pop(budget_no)
                    print("*** SUCCESS!!! Record Has Been Deleted Successfully ***\n")

                else:
                    print("*** INFO!!! Nothing Has Been Changed ***\n")
                    go_back_to_user_menu()

                with open("records.json", 'w') as f:
                    json.dump(data, f, indent=4)

    def view_budget(self):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found ***\n")
            return

        if self.email not in data:
            print("*** EMPTY_DATA!!! No Records Are Found ***\n")
        else:

            budget_amount = []
            budget_remark = []

            for budgets_no, budget_value in data[self.email]["total_budget"].items():
                amount = budget_value['budget']
                remark = budget_value['remarks']
                budget_amount.append(amount)
                budget_remark.append(remark)

            total_budget = 0
            print("S.No.\tAmount\t\tTotal_Budget\tRemarks")
            for i, amount in enumerate(budget_amount):
                total_budget += float(amount)
                remark = budget_remark[i]
                print("{:<8}{:<15}{:<13}{:}".format(i + 1, amount, round(total_budget, 2), remark))

    def add_expenses(self, expense, expense_remark):
        # load data from records.json
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # add or update user's expenses
        user_data = data.get(self.email, {})
        user_budget = user_data.get('total_budget', {})
        user_expenses = user_data.get('total_expenses', {})

        # add new expense to user's expenses
        last_expense_num = int(max(user_expenses.keys()).split('_')[-1]) if user_expenses else 0
        new_expense_num = last_expense_num + 1
        user_expenses[f"expense_{new_expense_num}"] = {"expense": expense, "remarks": expense_remark}
        if not user_budget:
            user_budget[f"budget_0"] = {"budget": self.budget, "remarks": self.budget_remark}

        # Delete expense_0 if exists
        if 'expense_0' in user_expenses:
            del user_expenses['expense_0']

        # update data with new user expenses
        user_data['total_budget'] = user_budget
        data[self.email] = user_data
        user_data['total_expenses'] = user_expenses
        data[self.email] = user_data

        # save data to records.json
        with open("records.json", 'w') as f:
            json.dump(data, f, indent=4)

    def edit_expenses(self):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found ***\n")
            return

        if self.email not in data:
            print("*** EMPTY_DATA!!! Records Not Found To Edit!!! ***\n")
        else:
            count_data = []
            for count in data[self.email]["total_expenses"].values():
                count_data.append(count)

            # To validate User Input For Edit
            while True:
                try:
                    edit = int(
                        input(f"Enter respective S.No. to Edit Your Expense Should be (1 to {len(count_data)}): "))
                    if edit <= 0:
                        print("*** ERROR!!! Value Should not be less than 1 ***\n")
                    elif edit > len(count_data):
                        print(f"*** ERROR!!! Record Not Found for Expense S.No. {edit} ***\n")
                    else:
                        break
                except ValueError:
                    print("*** ERROR!!! Enter respective S.No. to Edit Your Expense *** \n")

            # Logic starts for edit
            if count_data[edit - 1]:
                budget_nos = []
                data_list = data[self.email]['total_expenses'].keys()
                for key in data_list:
                    budget_nos.append(key)
                budget_no = (budget_nos[edit - 1])

                old_amount = data[self.email]["total_expenses"][budget_no]['expense']
                old_remark = data[self.email]["total_expenses"][budget_no]['remarks']

                # Getting New Values from User
                while True:
                    try:
                        print(f'\n*** DATA!!! Your Existing Expense Amount was "{old_amount}"')
                        new_amount = float(input("Edit Your Expense: "))
                        if new_amount < 0:
                            print("*** ERROR!!! Amount Must Be Greater Than 0 ***\n")
                        else:
                            print(f'\nYour Existing Budget Remark was "{old_remark}"')
                            new_remark = input("Edit Your Remarks: ")

                            # Assigning Edited data to dictionary
                            data[self.email]["total_expenses"][budget_no]['expense'] = new_amount
                            data[self.email]["total_expenses"][budget_no]['remarks'] = new_remark
                            print("*** SUCCESS!!! Your Data Has Been Successfully Edited ***\n")
                            break
                    except ValueError:
                        print("*** ERROR!!! Amount Must Be A Number ***\n")

                with open("records.json", 'w') as f:
                    json.dump(data, f, indent=4)

    def delete_expenses(self):
        try:
            with open("records.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found ***\n")

        if self.email not in data:
            print("*** EMPTY_DATA!!! Records Not Found To Delete!!! *** \n")
        else:
            count_data = []
            for count in data[self.email]["total_expenses"].values():
                count_data.append(count)

            # To validate User Input For Delete
            while True:
                try:
                    delete = int(
                        input(f"Enter respective S.No. to Delete Your Expense (Should be 1 to {len(count_data)}): "))
                    if delete <= 0:
                        print("*** ERROR!!! Value Should note be less than 1 ***\n")
                    elif delete > len(count_data):
                        print(f"*** ERROR!!! Record Not Found for Expense S.No. {delete} ***\n")
                    else:
                        break
                except ValueError:
                    print("*** ERROR!!! Enter respective S.No. to Delete Your Expense ***\n")

            # Logic To Delete data
            if count_data[delete - 1]:
                budget_nos = []
                data_list = data[self.email]['total_expenses'].keys()
                for key in data_list:
                    budget_nos.append(key)
                budget_no = (budget_nos[delete - 1])
                amount_to_del = data[self.email]["total_expenses"][budget_no]['expense']
                remark_to_del = data[self.email]["total_expenses"][budget_no]['remarks']

                # Get confirmation from user
                print("\nYour Existing Expense: ", amount_to_del)
                print("Your Existing Remark: ", remark_to_del)
                conformation = input(f"Are You Sure You Want To Delete Above Data (y/n): ").lower()

                if conformation == "y":
                    data[self.email]["total_expenses"].pop(budget_no)
                    print("*** SUCCESS!!! Record Has Been Deleted Successfully ***\n")

                else:
                    print("*** INFO!!! Nothing Has Been Changed ***\n")

                with open("records.json", 'w') as f:
                    json.dump(data, f, indent=4)

    def view_expenses(self):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found ***\n")
            return

        if self.email not in data:
            print("*** EMPTY_DATA!!! No Records Are Found ***\n")
        else:
            expense_amount = []
            expense_remark = []

            for expense_no, expense_value in data[self.email]["total_expenses"].items():
                amount = expense_value['expense']
                remark = expense_value['remarks']
                expense_amount.append(amount)
                expense_remark.append(remark)

            total_expenses = 0
            print("S.No.\tAmount\t\tTotal_Expenses\tRemarks")
            for i, amount in enumerate(expense_amount):
                total_expenses += float(amount)
                remark = expense_remark[i]
                print("{:<8}{:<15}{:<13}{:}".format(i + 1, amount, total_expenses, remark))

    def view_balance(self, email, name):
        try:
            with open("records.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("*** ERROR!!! File Not Found *** \n")
            return

        if self.email not in data:
            print("*** EMPTY_DATA!!! Records Not Found To Show Your Balance ***\n")
        else:
            budget_total = 0
            expense_total = 0
            budget_count = []
            expense_count = []

            for amounts in data[self.email]["total_budget"].values():
                amount = amounts['budget']
                budget_count.append(amounts)
                budget_total += amount
            for amounts in data[self.email]["total_expenses"].values():
                amount = amounts['expense']
                expense_count.append(amounts)
                expense_total += amount

            balance = round(budget_total - expense_total, 2)

            print(f"      *************** SUMMARY OF YOUR ACCOUNT ***************")
            print(f"Account Holder: {name}\nAccount Email: {email}")
            print(f"Budget Entered: {len(budget_count)} Times")
            print(f"Expense Entered: {len(expense_count)} Times")
            print("-" * 70)
            print("Total_Budget_Amount(Cr.)\tTotal_Expense_Amount(Dr.)\tBalance Status")
            print("{:^22}{:^30}{:^19}".format(budget_total, expense_total, balance))
            print("-" * 70)
            print("*" * 150)
            if balance < -1000:
                print("WARNING: Your expenses have exceeded your budget by a significant amount. It is crucial that you "
                      "immediately reduce your spending to avoid financial difficulties.")
            elif balance < 0:
                print("'WARNING'!!! Your expenses have exceeded your budget. Please try to reduce your spending to avoid "
                      "running out of funds.")
            elif balance == 0:
                print("'ATTENTION'!!! Your expenses and budget are currently equal. Please review your spending to "
                      "avoid going over your budget.")
            elif balance > 1000:
                print("GREAT JOB!!! Your expenses are currently less than your budget. Keep it up and continue to monitor "
                      "your spending.")
            else:
                print("GOOD NEWS!!! Your expenses are currently under control. However, keep in mind that unexpected "
                      "expenses can arise, so continue to monitor your spending.")
            print("*" * 150)


def main():
    menu()
    while True:
        menu_choice = input("Please Choose an option: ")
        if menu_choice == "1":
            print(f"------------- Create New Account -------------")
            name = input("Enter Your Name: ").title()
            email = input("Enter Your Email: ").lower()
            password1 = input("Enter Your Password: ")
            password2 = input("Confirm Your Password: ")
            user = Account(name, email, password1, password2)
            user.create_user()
            go_back_to_menu()
        elif menu_choice == "2":
            while True:
                print(f"------------- Account Login -------------")
                email = input("Enter Your Email: ").lower()
                if "@" not in email:
                    print("*** ERROR!!! Invalid Email ID, Try Again ***\n")
                else:
                    break
            password = input("Enter Your Password: ")
            user = Account("", email, password, password)
            login_success = user.login_user()

            if login_success:
                name = login_success[1]
                while True:
                    menu_choice = input("Please Choose an Action: ")
                    if menu_choice == "1":
                        while True:
                            calc = Calculation(email)
                            print(f"------------- Add Budget {name} -------------")
                            try:
                                budget = float(input("Enter Your Budget Amount: "))
                                if budget <= 0:
                                    print("*** ERROR!!! Budget Amount Must Be Greater Than ZERO ***\n")
                                    continue
                                budget_remark = input("Enter Remark: ")
                                calc.add_budget(budget, budget_remark)
                                print("*** SUCCESS!!! Your Budget Has Been Added Successfully ***\n")
                                go_back_to_user_menu()
                                user_menu(email, name)
                                break
                            except ValueError:
                                print("*** ERROR!!! Input must be a valid number ***\n")
                    elif menu_choice == "2":
                        budget_edit = Calculation(email)
                        print(f"------------- Edit Your Current Budget {name} -------------")
                        budget_edit.view_budget()

                        while True:
                            choice = input(
                                "\nDo You Want To 'Edit' or 'Delete' The Existing Data ('e' for Edit / 'd' for "
                                "Delete): ").lower()
                            if choice == "e":
                                budget_edit.view_budget()
                                budget_edit.edit_budget()
                                break
                            elif choice == "d":
                                budget_edit.view_budget()
                                budget_edit.delete_budget()
                                break
                            else:
                                print("*** ERROR!! Please Enter ('e' for Edit / 'd' for Delete): ")
                                continue
                        go_back_to_user_menu()
                        user_menu(email, name)
                        continue
                    elif menu_choice == "3":
                        budget_view = Calculation(email)
                        print(f"------------- Your Current Budget Status {name} -------------")
                        budget_view.view_budget()
                        go_back_to_user_menu()
                        user_menu(email, name)
                    elif menu_choice == "4":
                        while True:
                            calc = Calculation(email)
                            try:
                                print(f"------------- Add Expenses {name} -------------")
                                expense = float(input("Enter Your Expense Amount: "))
                                if expense <= 0:
                                    print("*** ERROR!!! Expense Amount Must Be Greater Than ZERO ***\n")
                                    continue
                                expense_remark = input("Enter Remark: ")
                                calc.add_expenses(expense, expense_remark)
                                print("*** SUCCESS!!! Your Expense Has Been Added Successfully ***\n")
                                go_back_to_user_menu()
                                user_menu(email, name)
                                break
                            except ValueError:
                                print("*** ERROR!!! Input Must Be A Valid Number ***\n")
                    elif menu_choice == "5":
                        expense_edit = Calculation(email)
                        print(f"------------- Edit Your Current Expenses {name} -------------")
                        expense_edit.view_expenses()
                        while True:

                            choice = input(
                                "\nDo You Want To 'Edit' or 'Delete' The Existing Data ('e' for Edit / 'd' for "
                                "Delete): ").lower()
                            if choice == "e":
                                expense_edit.view_expenses()
                                expense_edit.edit_expenses()
                                break
                            elif choice == "d":
                                expense_edit.view_expenses()
                                expense_edit.delete_expenses()
                                break
                            else:
                                print("*** ERROR!! Please Enter ('e' for Edit / 'd' for Delete): ")
                                continue
                        go_back_to_user_menu()
                        user_menu(email, name)
                        continue
                    elif menu_choice == "6":
                        expenses_view = Calculation(email)
                        print(f"------------- Your Current Expenses Status {name} -------------")
                        expenses_view.view_expenses()
                        go_back_to_user_menu()
                        user_menu(email, name)
                    elif menu_choice == "7":
                        balance_view = Calculation(email)
                        print(f"------------- Your Current Balance Status {name} -------------")
                        balance_view.view_balance(email, name)
                        go_back_to_user_menu()
                        user_menu(email, name)
                        continue
                    elif menu_choice == "8":
                        print("*** SUCCESS!!! You are Logged Out Successfully. \n")
                        go_back_to_menu()
                        break
                    else:
                        print("""Invalid Choice!!!
                        Enter 1 to Add your Budget
                        Enter 2 to Edit your Budget
                        Enter 3 to View your Budget
                        Enter 4 to Add your Expenses
                        Enter 5 to Edit your Expenses
                        Enter 6 to View your Expenses
                        Enter 7 to View your Balance
                        Enter 8 to Log Out""")
            else:
                go_back_to_menu()
        elif menu_choice == "3":
            while True:
                print(f"------------- Reset Password -------------")
                email = input("Enter Your Email: ").lower()
                if "@" not in email:
                    print("*** ERROR!!! Invalid Email ID, Try Again ***\n")
                else:
                    break
            password = input("Enter Your Old Password: ")
            user = Account("", email, password, password)
            user.reset_password()
            go_back_to_menu()
        elif menu_choice == "4":
            about()
            go_back_to_menu()
        elif menu_choice == "5":
            exit()
        else:
            print("""Invalid Choice!!!
            Enter 1 to Create an Account
            Enter 2 to Login with your Account
            Enter 3 to Reset Your Password
            Enter 4 to Know about App
            Enter 5 to Exit""")


if __name__ == "__main__":
    main()
