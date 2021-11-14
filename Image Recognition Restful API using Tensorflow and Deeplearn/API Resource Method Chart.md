- Objective - API para a classificação de imagens
- Methods - GET, POST
- Resources - Home, Register_User, Classify, Refill

| Resource       | Method | Path      | User_For                | Params                                        | Status_Code        |
|----------------|--------|-----------|-------------------------|-----------------------------------------------|--------------------|
| Home           | GET    | /         | Homepage                | -                                             | 200                |
| Register_User  | POST   | /register | Registrar usuários      | username,password:str                         | 200, 301           |
| Classify_Image | POST   | /classify | Classificar imagens     | username,password,url:str                     | 200, 301, 302, 303 |
| Refill_Tokens  | POST   | /refill   | Refill tokens de acesso | username,admin_password:str e refill_cont:int | 200, 301, 304      |


| Status_Code | Meaning                          |
|-------------|----------------------------------|
| 200         | OK                               |
| 301         | Out of tokens                    |
| 302         | Invalid username and/or password |
| 303         | User already registered          |
| 304         | Invalid admin password           |
| 400         | Missing parameter                |