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

def Income():
    url = BASE_URL+"p/1/"
    token = "test" 
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
    argvs = sys.argv
    if len(argvs) <= 1:
        help_text()
    elif "help" in argvs:
        help_text()
    elif "-i" in argvs:
        Income()
    elif "-g" in argvs:
        help_text()
    elif "-e" in argvs:
        help_text()

if __name__ == "__main__":
    main()