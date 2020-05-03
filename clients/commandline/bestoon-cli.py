import requests, sys, os

BASE_URL = "http://127.0.0.1:8009/"

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

def Income(token):
    url = BASE_URL+"p/1/"
    amount = input("Enter amount /> ")
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
    

# curl --data "token=$TOKEN&=$AMOUNT&=$TEXT" $BASE_URL/submit/expense/

def main():
    clear_terminal()
    token = get_token()
    argvs = sys.argv
    if len(argvs) <= 1:
        help_text()
    elif argvs[1] == "help":
        help_text()
    elif argvs[1] == "-i":
        Income(token)
    elif argvs[1] == "-g":
        help_text()
    elif argvs[1] == "-e":
        help_text()
    elif argvs[1] == "--edit":
        edit_token()
    else:
        help_text()

if __name__ == "__main__":
    main()