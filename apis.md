# API User Manual

## Submits
### /submit/expense/
#### Submit A Expense
-  POST, returns a json
-  input: date (optional), text, amount, token
-  output: status:ok

### /submit/income/
#### Submit A Income
-  POST, returns a json
-  input: date (optional), text, amount, token
-  output: result:ok

## Account Managment 
### /accounts/login/
#### Login A User
-  POST, returns a json
-  input: username, password
-  output: status:ok & token

### /accounts/register/
#### Singup A User
####  Step 1:
-    POST
-    input: username, email, password
-    output: status:ok
####  Step 2 (this part is not required, Email verifacation is not working.):
##### Note: Click on link with the code in the email
-    GET
-    input: email, code
-    output: status: ok (shows the token)

## Get Status and Previous Data(s)
### /q/generalstat/
#### Get General Status Of User
-  POST, returns a json
-  input: fromdate (optional), todate(optional), token
-  output: json from some general stats related to this user

### /q/incomes/
#### Get Previous Incomes
-  POST, returns json
-  input: token, num (optional, default is 10)
-  output: last num incomes

### /q/expenses/
#### Get Previous Expenses
-  POST, returns json
-  input: token, num (optional, default is 10)
-  output: last num  expenses

## Edit and Remove Data
### /edit/expense/
#### Edit Expense
-  POST, returns json
-  input: pk(id), text, amount, token
-  output: status: ok

### /edit/income/
#### Edit Income
-  POST, returns json
-  input: pk(id), text, amount, token
-  output: status: ok

### /edit/rmincome/
#### Remove Income
-  POST, returns json
-  input: pk(id), token
-  output: status: ok

### /edit/rmexpence/
#### Remove Expence
-  POST, returns json
-  input: pk(id), token
-  output: status: ok

