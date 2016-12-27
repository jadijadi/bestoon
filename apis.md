/submit/expense/
  POST, returns a json
  input: date (optional), text, amount, user
  output: status:ok

/submit/income/
  POST, returns a json
  input: date (optional), text, amount, user
  output: status:ok

/accounts/register/
  step1:
    POST
    input: username, email, password
    output: status:ok
  step2: #click on link with the code in the email
    GET
    input: email, code
    output: status: ok (shows the token)
