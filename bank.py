import mysql.connector
from datetime import date
from datetime import datetime
import time
import sys

def clean():
    for _ in range(64):
        print()

def get_connection():
    global mydb
    mydb = mysql.connector.connect(
        host = "localhost",
        user="root",
        password = "admin123",
        database = "bankdb",
    )
    global mycursor
    mycursor = mydb.cursor()



def add_acc():
    try:
        get_connection()
        name = input("Enter your name: ")
        mail=input("Enter your email: ")
        ph=input("Enter phone number: ")
        adhar=input("Enter aadhar number: ")
        addr = input("Enter address: ")
        acc_t=input("Saving or Current??  ")
        bal =input("Account opening balance: ")

        sql = 'insert into customer(user_name,email,phone,aadhar_no,address,acc_type,balance,stat) values ("' +name+ '", "'+mail+'", "'+ph+'","'+adhar+'","'+addr+'","'+acc_t+'","'+bal+'","active");'
        mycursor.execute(sql)
        mydb.commit()
        sql2 = 'select ac_no from customer where aadhar_no = "'+adhar+'";'
        mycursor.execute(sql2)
        res = mycursor.fetchone()
        for i in res:
            print("Account number alloted to you is: ",i)
        mydb.close()
        print("Customer added succesfully!!")
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
    mydb.close()

def modify_acc():
    try:
        get_connection()
        a_no = input("Enter your account number: ")
        print("-"*130)
        print("Customer Information Modification")
        print("-"*130)
        print("1) Update your Name")
        print("2) Update your Contact number ")
        print("3) Update your Address")
        print("4) Update email")
        choice = int(input("Enter choice you want to change"))
        new_dat = input("Enter the new information ")
        field_val=""
        if choice == 1:
            field_val='name'
        if choice == 2:
            field_val='phone'
        if choice == 3:
            field_val='address'
        if choice == 4:
            field_val='email'

        sql = 'update customer set ' +field_val+ '="' +new_dat+ '" where ac_no='+a_no+';'
        mycursor.execute(sql)
        print("Updating your information.....")
        time.sleep(2)
        mydb.commit()
        print("Customer information updated successfully")
    except mysql.connector.Error as e:
        print("There is a problem updating the information!!{}".format(e))
    mydb.close()

def close_acc():
    try:
        get_connection()
        print("------------------------ACCOUNT CLOSING----------------------------------")

        ac = int(input("Enter account number: "))
        sql='update customer set stat = "Closed" where ac_no='+ac+';'
        print("Closing your account, please wait......")
        time.sleep(2)
        mycursor.execute(sql)
        print("Account closed!!!")
        mydb.commit()
    except ValueError as a:
        print("Enter account number in digit only!!!")
    except mysql.connector.Error as e:
        print("Not able to establish a connection {}".format(e))
    mydb.close()

def transactions():
    clean()
    try:
        print("-"*130)
        print("                                                 TRANSACTIONS MENU                                            ")
        print("-"*130)
        print("1) Deposit Cash")
        print("2) Withdraw Cash")
        print("3) Return to Main Menu")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            deposit()
        if ch == 2:
            withdraw()
        if ch == 3:
            Menu()
    except ValueError:
        print("Please enter choice in digit only!!!")

def ac_status(ac):
    get_connection()
    sql = 'select stat,balance from customer where ac_no="'+ac+'";'
    result = mycursor.execute(sql)
    result = mycursor.fetchone()
    #mydb.close()
    return result


def deposit():
    clean()
    try:
        get_connection()
        print("-"*130)
        print("                                                          DEPOSIT YOUR CASH                                      ")
        print("-"*130)
        today = datetime.today().strftime('%Y-%m-%d')
        ac = input("Enter your account number: ")
        amount = input("Enter amount in digits you want to deposit: ")
        res = ac_status(ac)

        if res[0] == 'active':
            sql = 'update customer set balance=balance + "'+amount+'" where ac_no="'+ac+'" and stat="active";'
            sql2='insert into transact(amount,t_type,dot,ac_no) values ("'+amount+'","deposit", "'+str(today)+'", "'+ac+'");'
            print("Depositing your Cash, Please Wait........")
            time.sleep(3)
            mycursor.execute(sql2)
            mycursor.execute(sql)
            mydb.commit()
            print("Your amount has been deposited! Thank you for using our services!")
            mydb.close()
        else:
            print("Your account is Suspended or Closed, Please visit your nearest branch")
    except mysql.connector.Error as e:
        print("Couldn't establish connection {}".format(e))
    except ValueError:
        print("Enter amount and account number in digits!!")

    cl = input("Type Close to exit")
    if cl == "close" or "Close":
        Menu()

def withdraw():
    try:
        get_connection()
        clean()
        print("-"*130)
        print("                                WITHDRAW CASH                               ")
        print("-"*130)
        today = datetime.today().strftime('%Y-%m-%d')
        ac = input("Enter your account number: ")
        amount = input("Enter amount: ")
        res = ac_status(ac)
        if res[0] == "active" and int(res[1]) >= int(amount):
            sql = 'update customer set balance=balance - "'+amount+'" where ac_no = "'+ac+'" and stat="active";'
            sql2 = 'insert into transact(amount,t_type,dot,ac_no) values ("'+amount+'", "withdraw", "'+str(today)+'", "'+ac+'");'
            mycursor.execute(sql2)
            mycursor.execute(sql)
            print("Withdrawing Cash, Please wait....")
            time.sleep(3)
            mydb.commit()
            print("Amount successfully debited from your account")
            mydb.close()
        else:
            print("Insufficient Balance or your account is suspended/closed. Please contact your nearest branch")
    except mysql.connector.Error as e:
        print("Connection could not be established {}".format(e))
    except ValueError:
        print("Enter amount and account in digits!")
    cl=input("Type close to exit")
    if cl == "close" or "Close":
        Menu()

def search_menu():
    try:
        get_connection()
        print("-"*130)
        print("                                       SEARCH YOUR INFORMATION                                 ")
        print("-"*130)
        ac = input("Enter your Account number: ")
        sql = 'select * from customer where ac_no = "'+ac+'";'
        mycursor.execute(sql)
        result = mycursor.fetchmany(8)
        n = len(result)
        clean()
        print("Fetching Data please wait....")
        time.sleep(2)
        print("                    DATA FOUND!!!                   ")
        print("-"*100)
        for i in result:
            print("Name: ",i[1])
            print("Email: ",i[2])
            print("Phone number: ",i[3])
            print("Aadhar number: ",i[4])
            print("Address: ",i[5])
            print("Account Type: ",i[6])
            print("Available balance: ",i[7])
            print("Account Status: ",i[8])
        print("-"*100)

        if n < 0:
            print('Data does not exist in database!!!')
        cl = input("Type close to exit")
    except mysql.connector.Error as e:
        print("Cannot establish connection {}".format(e))
    except ValueError:
        print("Please enter account number in digits only")
    finally:
        if cl == "close" or "Close":
            Menu()
        mydb.close()

def reports():
    print("-"*120)
    print("                                     REPORTS MENU                                 ")
    print("-"*120)
    print("1) Daily Report")
    print("2) Monthly Report")
    print("3) Return to Menu")

    choice  = int(input("Enter your choice: "))
    if choice == 1:
        daily()
    if choice == 2:
        monthly()
    if choice == 3:
        Menu()

def daily():
    try:
        get_connection()
        today = input("Enter date in 'Y-M-D' format: ")
        sql = 'select tid,amount,t_type,dot,ac_no from transact where dot="'+today+'";'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        n = len(result)
        print("Fetching reports, please wait.....")
        time.sleep(2)
        clean()
        print("-"*120)
        print("                          Daily Transaction Reports:                      ")
        print("-"*120)
        for i in result:
            print("Transaction Id: ",i[0])
            print("Amount: ",i[1])
            print("Type: ",i[2])
            print("Date: ",i[3])
            print("Account number: ",i[4])

        print("-"*120)
        if (n < 0):
            print("No result found for your query!!!")
        cl = input("Type close to exit: ")
        if cl == "close" or "Close":
            Menu()
    except mysql.connector.Error as e:
        print("Cannot establish connection {}".format(e))
    except ValueError:
        print("Enter correct information")

def monthly():
    try:
        get_connection()
        month = input("Enter month number: ")
        sql = 'select tid,amount,t_type,dot,ac_no from transact where month(dot)="'+month+'";'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        n = len(result)
        print("Fetching report,please wait....")
        time.sleep(2)
        clean()
        print("-"*120)
        print("                                   Monthly Report                               ")
        print("-"*120)
        for i in result:
            print("Transaction Id: ",i[0])
            print("Amount: ",i[1])
            print("Type: ",i[2])
            print("Date: ",i[3])
            print("Account Number: ",i[4])
        print("-"*120)
        if(n<0):
            print("No data found!!!")
        cl = input("Type Exit to close ")
        if cl == "Exit" or "exit":
            Menu()
    except mysql.connector.Error as e:
        print("Connection could not be established {}".format(e))
    except ValueError:
        print("Enter correct information!")





















def Menu():
    try:
        while True:
            #clean()
            print("-"*150)
            print("                                                   $ WELCOME TO THE  BANK MANAGEMENT SYSTEM $                                     ")
            print("-"*150)
            print("1) Add new Account")
            print("2) Modify your account")
            print("3) Transactions")
            print("4) Close your account")
            print("5) Search")
            print("6) Reports")
            print("7) Close the application")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_acc()
            elif choice == 2:
                modify_acc()
            elif choice == 3:
                transactions()
            elif choice == 4:
                close_acc()
            elif choice == 5:
                search_menu()
            elif choice == 6:
                reports()
            elif choice == 7:
                print("Thanks for using our services!")
                print("Exiting....")
                time.sleep(2)
                sys.exit()
    except ValueError:
        print("Please choose from the options above!!")
        Menu()

if __name__ == "__main__":
    Menu()