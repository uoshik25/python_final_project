import time
import os

def wait_and_clear(seconds = 1.5):
    time.sleep(seconds)
    os.system('cls' if os.name == 'nt' else 'clear')

def Main_menu():
    print("=======  Main Menu =======\n")
    print("1. Sign Up")
    print("2. Log In")
    print("3. Exit")

def SignUp_Menu():
    print("======= SignUp Menu =======\n")

    print("Select a Role:\n")
    print("1. Admin")
    print("2. Student")
    print("3. Exit")

def authorize(ad_user,ad_pass):
    if ad_user == "admin@123" and ad_pass == "admin123#":
        return True
        wait_and_clear(seconds=1.5)

def user_exists(user):
    try:
        with open("passwords.txt","r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == user:
                    return True
        return False
    except FileNotFoundError:
        return False
    
def SignUp(user,password,re_pass,role):
    if password!= re_pass:
        return "Passwords do not match"
    
    if user_exists(user):
        return "Username already exists"
    
    try:
        with open("passwords.txt","a") as pw, open("users.txt","a") as us:
            us.write(f"{user},{role}\n")
            pw.write(f"{user},{password}\n")
        return "Signed Up Successfully! Returning to Main menu..."
    except:
        return "Error during signup."

def collect_signup_data(role):
    print(f"\n===== {role.upper()} SIGNUP =====\n")

    user = input("Enter username: ")
    password = input("Enter password: ")
    re_pass = input("Re-enter password: ")

    message = SignUp(user, password, re_pass, role)
    print(f"\n{message}")


def LogIn_Menu():
    print("======= LogIn Menu =======\n")



while True:
    Main_menu()
    ch = int(input("\nSelect an option:"))
    wait_and_clear(seconds=1.5)
    if ch==1:
        SignUp_Menu()
        role_ch = int(input("Enter a role to sign Up:"))
        if role_ch == 1:
            wait_and_clear(seconds=1.5)
            print("======= Authorization Required =======\n")
            auth_user = input("Enter username : ")
            auth_pass = input("Enter password : ")
            res = authorize(auth_user, auth_pass)

            if res == True:
                print("\nVerification Sucessful. Proceeding to Sign Up menu for admin")
                wait_and_clear(seconds=1)
            else:
                print("\nIncorrect credentials")
                break
            collect_signup_data("Admin")
            wait_and_clear(seconds=1.5)

        elif role_ch == 2:
            collect_signup_data("Student")
            wait_and_clear(seconds=1.5)
    elif ch == 2:
        LogIn_Menu()




