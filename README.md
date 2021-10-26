# trading view test task

## deploy:
### postgres
```shell
sudo su - postgres
psql
alter user postgres password 'postgres';
create database trading_view_task owner 'postgres';
```
### python
```shell
cd ./backend
python3.9 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## docker-compose:
```shell
docker-compose up --build
```

## api interface
### token
```
POST: api/auth/
Header: Content-type - application/json
Body: Json
{
    "username": "",
    "password": ""
}

Response: Json

{
  "token": "token"
}
```
### create_account
```
POST: api/account/create/
Header: Content-type - application/json,
       Authorization - Token 'token'
Body: Json
{
	"amount": 100.0 # precision - 2
}

Response: Json

{
  "number": "b6cfc7fe78e7037d-55d94b735e2056e7-794d98426035b31d-b4f3d9d6bc884f8e"
}
```
### create_transaction
```
POST: api/transaction/create/
Header: Content-type - application/json,
        Authorization - Token 'token'
Body: Json
{
    "type": "transfer/letter_of_credit/invoice",
    "amount": 10.0,
    "account_from": "number",
    "account_to": "number"
}

Response: Json
{
  "checksum": "995f8075bc85767d3f5de6203a07a15f543b9f0822e91f52852fce56f53bd686"
}
```
### confirm_transaction
```
POST: api/transaction/confirm/
Header: Content-type - application/json,
        Authorization - Token 'token'
Body: Json
{
  "checksum": "995f8075bc85767d3f5de6203a07a15f543b9f0822e91f52852fce56f53bd686"
}

Response: Json
{
  "checksum": "995f8075bc85767d3f5de6203a07a15f543b9f0822e91f52852fce56f53bd686"
}
```
### cancel_transaction
```

POST: api/transaction/cancel/
Header: Content-type - application/json,
        Authorization - Token 'token'
Body: Json
{
  "checksum": "995f8075bc85767d3f5de6203a07a15f543b9f0822e91f52852fce56f53bd686"
}

Response: Json
{
  "checksum": "995f8075bc85767d3f5de6203a07a15f543b9f0822e91f52852fce56f53bd686"
}
```
### get_top_accounts
```
GET api/account/top/
Header: Authorization - Token 'token'

Response: Json
{
  "top": [
    {
      "user_from_id": 1,
      "total": "30.00"
    },
    {
      "user_from_id": 2,
      "total": "20.00"
    }
  ]
}
```
