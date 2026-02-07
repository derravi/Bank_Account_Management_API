from fastapi import FastAPI,HTTPException
from typing import Dict
from fastapi.responses import JSONResponse
from Models.models import account_details,dummy_account_details
from Models.models import opational_account_model,deposit_mmodel,withdraw_mmodel,transfer_model
from datetime import datetime

import json

app = FastAPI(title="Bank Account Management API")

try:
    def load_data():
        with open('account.json','r') as f:
            return json.load(f)
except FileNotFoundError as e:
    print(f"Error {e}.")
except Exception as f:
    print(f"Error {f}")

try:
    def save_data(data):
        with open('account.json','w') as g:
            json.dump(data,g)
except FileNotFoundError as e:
    print(f"Error {e}.")
except Exception as f:
    print(f"Error {f}")

@app.get("/")
def default():
    return {"message":"This is the Bank Account Management API pipeline."}

#Get all the data into from the Json file
@app.get("/ac_details",response_model=Dict[str,dummy_account_details])
def ac_details():
    data = load_data()
    return data

#Get the Data for perticular Accountent
@app.get("/ac_details/{account_no}",response_model=dummy_account_details)
def act_details(account_no:str):
    try:
        data = load_data()

        if account_no not in data:
            raise HTTPException(status_code=404,detail="Data not Existed")
    
        return data[account_no]
    
    except Exception as e:
        print(f"Error {e}.")

#Create new Account for student
@app.post("/create_account",status_code=201)
def create_account(account:account_details):
    
    data = load_data()

    if account.account_id in data:
        raise HTTPException(status_code=400, detail="Account ID already exists")
    
    #Check the Given Gmail is alredy existed or not.    
    for i in data.values():
        if i['gmail'] == account.gmail:
            raise HTTPException(status_code=409,detail="Gmail id alredy Existed please us Different Gmail account.")
    
    data[account.account_id] = account.model_dump(exclude={"account_id"})

    #save Data
    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Data Succesfully saved."})
    

#Update Endpoints for details updating of accountent 
@app.put("/edit_account/{account_id}")
def update_acct(account_id:str,edit_acnt:opational_account_model):

    data = load_data()

    if account_id not in data:
        raise HTTPException(status_code=404,detail="Account not existed.")
    
    existing_data = data[account_id]

    updated_account = edit_acnt.model_dump(exclude_unset=True)

    for key,values in updated_account.items():
        existing_data[key] = values

    existing_data["account_id"] = account_id

    pydentic_object = account_details(**existing_data)
    
    #to save the data 
    data[account_id] = pydentic_object.model_dump(exclude={"account_id"})

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Data Successfully updated."})

#Delete Endpoint use for delete the account of the User.
@app.delete("/delete_account/{account_id}")
def del_account(account_id:str):

    data = load_data()
    
    if account_id not in data:
        raise HTTPException(status_code=404,detail="Account data is not Existed.")
    
    del data[account_id]

    save_data(data)
    
    return JSONResponse(status_code=200,content={"message":"Account data is removed."})

#Deposite Endpoint for Accountent.
@app.put("/deposit/{account_id}")
def deposit_amount(account_id:str,dep_model:deposit_mmodel):
    
    data = load_data()

    if account_id not in data:
        raise HTTPException(status_code=404,detail="Account not Existed.")
    
    if dep_model.balance <=0:
        raise HTTPException(status_code=400, detail="Deposit amount must be grater than 0.")

    data[account_id]["balance"] += dep_model.balance

    save_data(data)

    return {"message":"Deposite Successfull.",
            "Account id":account_id,
            "Deposite Amount":dep_model.balance,
            "Total Amount":data[account_id]["balance"]}

# withdraw endpoints
@app.put("/withdraw/{account_id}")
def withdraw_money(account_id:str,with_model:withdraw_mmodel):

    data = load_data()

    if account_id not in data:
        raise HTTPException(status_code=404,detail="Account not Existed.")
    
    if with_model.balance == 0:
        raise HTTPException(status_code=400, detail="Total Amount is 0.")
    
    data[account_id]["balance"] -= with_model.balance

    save_data(data)

    return {"message":"Deposite Successfull.",
            "Account id":account_id,
            "Deposite Amount":with_model.balance,
            "Total Amount":data[account_id]["balance"]}

#Money Transfer Model.
@app.put("/transfer/{account_id}")
def money_transfer(account_id:str,trans_model:transfer_model):

    data = load_data()

    #To check Sender Account is existed or not 
    if account_id not in data:
        raise HTTPException(status_code=404,detail="Sender Account not Found.")
    
    #To check Reciver Account is existed or not 
    if trans_model.to_account not in data:
        raise HTTPException(status_code=404,detail="Reciver Account not Found.")

    #To check both account same or not
    if account_id == trans_model.to_account:
        raise HTTPException(status_code=400,detail="Sender and Reciveraccount can not be same.")
    
    #Check the Balance of User need to transfer.
    if trans_model.balance <=0:
        raise HTTPException(status_code=400, detail="Transfer ammount must be grater than 0.")
    
    #To Check the balance of sender account.
    if data[account_id]['balance'] < trans_model.balance:
        raise HTTPException(status_code=400,detail="Insufficient balance in sender account.")
    
    #Balance management from both account.
    data[trans_model.to_account]['balance'] = data[trans_model.to_account]['balance'] + trans_model.balance
    data[account_id]['balance'] = data[account_id]['balance'] - trans_model.balance

    #save updated data
    save_data(data)

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    #Return requernment field.
    return {
        "message": "Money transferred successfully",
        "From Account": account_id,
        "To Accounnt" : trans_model.to_account,
        "Transfer Ammount": trans_model.balance,
        "Current Sender Balance":data[account_id]['balance'],
        "Current Reciver Balance":data[trans_model.to_account]['balance'],
        "Time":timestamp
    }