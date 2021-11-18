- Objective - API para lidar com transações bancárias
- Methods - GET, POST
- Resources - Home, Register_User, Add, Transfer, Check_Balance, Takeload, Payload

| Resource      | Method | Path      | User_For                | Params                                         | Status_Code        |
|---------------|--------|-----------|-------------------------|------------------------------------------------|--------------------|
| Home          | GET    | /         | Homepage                | -                                              | 200                |
| Register_User | POST   | /register | Registrar usuários      | username,password:str                          | 200, 301, 302      |
| Add           | POST   | /add      | Adicionar dinheiro      | username,password:str e amount:int             | 200, 301, 302, 304 |
| Transfer      | POST   | /tranfers | Tranferir dinheiro      | username,password,username_to:str e amount:int | 200, 301, 303, 304 |
| Check_Balance | POST   | /balance  | Checar dividas e outros | username,password:str                          | 200, 301, 304      |
| Takeload      | POST   | /takeload | Fazer takeload          | username,password:str e amount:int             | 200, 301, 304      |
| Payload       | POST   | /payload  | Fazer payload           | username,password:str e amount:int             | 200, 301, 303, 304 |

| Status_Code | Meaning                          |
|-------------|----------------------------------|
| 200         | OK                               |
| 301         | Invalid username                 |
| 302         | Invalid password                 |
| 303         | Not enough money                 |
| 304         | Amount of money <= 0             |
| 400         | Missing parameter                |