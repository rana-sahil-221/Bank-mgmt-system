import mysql.connector
from datetime import date
import time

def clean():
    for _ in range(64):
        print()

def add_acc():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="altolxi@968",
        database="bankdb",
    )
    mycursor=mydb.cursor()
    try:
        name = input("Enter your name: ")
        mail=input("Enter your email: ")
        ph=input("Enter phone number: ")
        adhar=input("Enter aadhar number: ")
        addr = input("Enter address: ")
        acc_t=input("Saving or Current??")
        bal =input("Account opening balance: ")

        sql = 'insert into customer(user_name,email,phone,aadhar_no,address,1' \
              'acc_type,balance,stat) values ("' +name+ '", "'+mail+'", "'+ph+'","'+adhar+'","'+addr+'","'+acc_t+'","'+bal+'","active");'
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        print("Customer added succesfully!!")
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))

def modify_acc():
    try:
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="altolxi@968",
            database="bankdb"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as err:
        print("Connection couldn't be established!{}".format(err))

    try:

        a_no = input("Enter your account number: ")
        print("---------------------Customer Information Modification------------------")
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








def Menu():
    while True:
        #clean()
        print("-------------------------------------------------BANK MANAGEMENT SYSTEM -----------------------------------------------------")
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
            break

if __name__ == "__main__":
    Menu()