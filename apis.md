/submit/expense/
  POST, returns a json
  input: date (optional), text, amount, token
  output: status:ok

/submit/income/
  POST, returns a json
  input: date (optional), text, amount, token
  output: result:ok

/accounts/login/
  POST, returns a json
  input: username, password
  output: status:ok & token

/accounts/register/
  step1:
    POST
    input: username, email, password
    output: status:ok
  step2: #click on link with the code in the email
    GET
    input: email, code
    output: status: ok (shows the token)

/q/generalstat/
  POST, returns a json
  input: fromdate (optional), todate(optional), token
  output: json from some general stats related to this user

/q/incomes/
  POST, returns json
  input: token, num (optional, default is 10)
  output: last num incomes

/q/expenses/
  POST, returns json
  input: token, num (optional, default is 10)
  output: last num  expenses
