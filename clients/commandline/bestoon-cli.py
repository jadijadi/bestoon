import requests, sys, os

BASE_URL = "https://bestoon.ir"

def clear_terminal():
    if sys.platform == "linux" or "linux2":
        os.system("clear")
    elif sys.platform == "window":
        os.system("cls")
    else:
        pass

def help_text():
    text = """
    python bestoon-cli.py <metod>
    
    metods:
    -i : Record Income
    -e : Record Expense 
    -g : Get generalstat
    --edit :  Edit Your Token
    """
    print(text)

def get_token():
    try:
        open("token.bestoon-cli.txt","a")
        with open("token.bestoon-cli.txt","r") as f:
            data = f.read().splitlines()
        if data == []:
            this_token = input("Enter token \> ")
            if len(this_token) < 40 and this_token != "test":
                while True:
                    this_token = input("Enter token (q for Quit)\> ")
                    if len(this_token) > 40:
                        break
                    elif this_token == "test":
                        break
                    elif this_token == "q":
                        exit(0)
                    else:
                        pass
            else:
                print("you token saved to file token.bestoon-cli.txt")
                with open("token.bestoon-cli.txt","w") as f:
                    f.write(this_token)
        else:
            this_token = data[0]
        return this_token
    except Exception as err:
        print(err)
        exit(0)

def edit_token():
    open("token.bestoon-cli.txt","a")
    with open("token.bestoon-cli.txt","r") as f:
        data = f.read().splitlines()
    if data != []:
        this_token = input("OK Enter New TOKEN \> ")
        if len(this_token) < 40 and this_token != "test":
            while True:
                this_token = input("Enter token (q for Quit)\> ")
                if len(this_token) > 40:
                    break
                elif this_token == "test":
                    break
                elif this_token == "q":
                    exit(0)
                else:
                    pass
            with open("token.bestoon-cli.txt","w") as f:
                f.write(this_token)
        else:
            print("token edited")
            with open("token.bestoon-cli.txt","w") as f:
                f.write(this_token)
    else:
        print("YOU NOT TOKEN :(")

def income(token):
    try:
        url = BASE_URL+"/submit/income/"
        amount = input("[Income] Enter amount /> ")
        if amount.isnumeric():
            amount = int(amount)
        else:
            while True:
                amount = input("Enter amount (only number) /> ")
                if amount.isnumeric():
                    amount = int(amount)
                    break
        text = input("Enter Text \> ")
        heder = {"token":token,"amount":amount,"text":text}
        message = requests.post(url,heder)
        print(message)
    except Exception as err:
        print(err)
    
def expense(token):
    try:
        url = BASE_URL+"/submit/expense/"
        amount = input("[Expense] Enter amount /> ")
        if amount.isnumeric():
            amount = int(amount)
        else:
            while True:
                amount = input("Enter amount (only number) /> ")
                if amount.isnumeric():
                    amount = int(amount)
                    break
        text = input("[Expense] Enter Text \> ")
        heder = {"token":token,"amount":amount,"text":text}
        message = requests.post(url,heder)
        print(message)
    except Exception as err:
        print(err)

def generalstat(token):
    try:
        url = BASE_URL+"/q/generalstat/"
        heder = {"token":token}
        message = requests.post(url,heder)
        print(message)
    except Exception as err:
        print(err)

def main():
    clear_terminal()
    token = get_token()
    argvs = sys.argv
    if len(argvs) <= 1:
        help_text()
    elif argvs[1] == "help":
        help_text()
    elif argvs[1] == "-i":
        income(token)
    elif argvs[1] == "-g":
        generalstat(token)
    elif argvs[1] == "-e":
        expense(token)
    elif argvs[1] == "--edit":
        edit_token()
    else:
        help_text()

if __name__ == "__main__":
    main()