from fastapi import FastAPI, HTTPException 
from typing import Dict
from pydantic import BaseModel

database : dict[str,dict]={}

class user(BaseModel):
    username: str
    password: str
    balance : float = 0.0
  #  transactions : list[transaction] = []

class transaction(BaseModel):
    sender: user
    reciever: user
    amount: float = 0.0


def get_user(username) -> user:
    if username not in database:
        raise HTTPException(status_code=404, detail="user not found")
    return user(**database[username])

def update_user_info(user: user) :
    database[user.username] = user.dict()    #Alabto dict hena
    
def do_transactions(username: user, sender:user , amount: float):
  #  if username or sender not in database:
   #     raise HTTPException(status_code=400, detail="user doesn't exist")
   # if amount <=0 or amount >= sender.balance: 
    #    raise HTTPException(status_code=400, detail="invalid amount")
    username.balance += amount 
    sender.balance -= amount
    update_user_info(username)
    update_user_info(sender)

app=FastAPI()

@app.post("/login")
def login(user:user):
    exisitingUser = get_user(user.username)
    if exisitingUser.password != user.password:
        raise HTTPException(status_code=401, detail="wrong password pr username")
    return {"message:" : "Login successful"}

@app.post("/register")
def register(user:user):
    if user.username in database: 
        raise HTTPException(status_code=400, detail="User alreaady exists")
    database[user.username] = user.dict()
    return {"message": "Registeration successful"}

@app.get("/balance")
def get_balance(username:str):
    user = get_user(username)
    return {"message": f'your current balance is : {user.balance}'}

@app.post("/cashin")
def cash_in(username:str, amount:float):
        user = get_user(username)
        if amount <=0 : 
            raise HTTPException(status_code=400, detail="invalid amount of cash")
        user.balance += amount
        update_user_info(user)
        return {"message", "added cash successfully"}

@app.post("/cashout")
def cash_out(username:str, amount:float):
        user = get_user(username)
        if amount <=0 or amount >= user.balance: 
            raise HTTPException(status_code=400, detail="invalid amount of cash")
        user.balance -= amount
        update_user_info(user)
        return {"message", "Lost cash successfully"}

@app.post("/transfer")
def do_transfer(tran: transaction):
 #   if tran.amount <=0 or tran.amount >= tran.sender.balance: 
  #          raise HTTPException(status_code=400, detail="invalid amount of cash transfer")
    
    do_transactions(tran.reciever,tran.sender,tran.amount)
    #tran.sender.transaction.append(tran)
    #tran.reciever.transaction.append(tran)
    return {f'Message", "Money transfered to {tran.reciever.username} successfully'}

@app.get("/")
def main():
    print("Welcome to the cash transfer system!")
    while True:
        print("Please choose to 1)register or 2)login or 3)exit")
        choice=input("your choice: ")
        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            users = user(username=username,password= password)
            response = register(users)
            print(response)
        elif choice == "2":
            print("Enter username: ")
            username = input()
            print("Enter password: ")
            pw = input()
            users= user(username=username, password=pw)
            response = login(users)
            print("your login is: ", response)
            if response.get("message:") == "Login successful" : 
                while True: 
                    print("\nPlease select an action:")
                    print("1. Cash-in")
                    print("2. Cash-out")
                    print("3. Transfer")
                    print("4. Check balance")
                    print("5. Show transaction history")
                    print("6. Logout")
                    choice2 = input()
                    if choice2 == "1":
                        print("Please enter amount to cash in : ")
                        amount = float(input())
                        response=cash_in(users.username, amount)
                        print(response)
                    elif choice2 == "2":
                        print("Please enter amount to cash out : ")
                        amount = float(input())
                        response=cash_out(users.username, amount)
                        print(response)
                    elif choice2 == "3":
                        print("Please enter the user you want to transfer to and the amount you want to transfer: ")
                        recievername= input("Receiver: ")
                        amount = float(input("Transfer Amount: "))
                        reciever = get_user(recievername)
                        transactions = transaction(sender=users, reciever=reciever, amount=amount)
                        response=do_transfer(transactions)
                        print(response)
                    elif choice2 == "4":
                        response=get_balance(users.username)
                        print(response)
                    elif choice2 =="5":
                    # print(users.transactions)
                        pass
                    elif choice2 == "6":
                        break
                    else :
                        print("invalid choice, try again")
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again")
            

if __name__  == "__main__":
    main()
