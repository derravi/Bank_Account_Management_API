from pydantic import BaseModel,Field,EmailStr
from typing import Annotated
from typing import Optional

class account_details(BaseModel):
    account_id : Annotated[str,Field(...,description="Enter the Account ID",examples=["A001"])]
    name : Annotated[str,Field(...,description="Enter the name of the Accountent.",examples=["Harshil"])]
    balance : Annotated[float,Field(...,ge=0,description="Enter the Balacne of the Account.",examples=[123.01])]
    gmail : Annotated[EmailStr,Field(...,description="Enter the Gmail of the Accountent.",examples=["abcd@gmail.com"])]
    password : Annotated[str,Field(...,min_length=6,description="Enter the Password of the Accountent.",examples=["password"])]

class dummy_account_details(BaseModel):
    name : Annotated[str,Field(...,description="Enter the name of the Accountent.",examples=["Harshil"])]
    balance : Annotated[float,Field(...,ge=0,description="Enter the Balacne of the Account.",examples=[123.01])]
    gmail : Annotated[EmailStr,Field(...,description="Enter the Gmail of the Accountent.",examples=["abcd@gmail.com"])]

#Optional EndPoints
class opational_account_model(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    balance:Annotated[Optional[float],Field(default=None)]
    gmail:Annotated[Optional[EmailStr],Field(default=None)]
    password:Annotated[Optional[str],Field(default=None)]

#response model for Deposit Balance
class deposit_mmodel(BaseModel):
    balance : Annotated[float,Field(...,ge=0,description="Enter the Balacne of the Account.",examples=[123.01])]

#response model for Withdraw Balance
class withdraw_mmodel(BaseModel):
    balance : Annotated[float,Field(...,ge=0,description="Enter the Balacne of the Account.",examples=[123.01])]

#Transfer Model
class transfer_model(BaseModel):
    to_account:Annotated[str,Field(...,description="Reciver account ID.")]
    balance:Annotated[float,Field(...,gt=0,description="Transfer Ammount.")]