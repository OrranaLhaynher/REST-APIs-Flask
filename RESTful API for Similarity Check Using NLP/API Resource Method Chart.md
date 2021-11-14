- Objective = Compare similarity os documents
- Methods = GET, POST
- Resources = Home, Register_User, Detect_Similarity, Refill 


| Resource          | Method | Path      | User_For          | Params                                          | Status_Code              |
|-------------------|--------|-----------|-------------------|-------------------------------------------------|--------------------------|
| Home              | GET    | /         | Home page         | -                                               | 200                      |
| Register_User     | POST   | /register | Register users    | username, password : str                        | 200, 301, 302, 303 e 400 |
| Detect_Similarity | POST   | /detect   | Detect similarity | username, password, text1, text2 : str          | 200, 302 e 400           |
| Refill            | POST   | /refill   | Refill tokens     | username, admin_password : str, refill_cont:int | 200, 301, 302 e 400      |


| Status_Code |             Meaning              |
|-------------|----------------------------------|
| 200         | OK                               |
| 301         | Out of tokens                    |
| 302         | Invalid username and/or password |
| 303         | User already registered          |
| 304         | Invalid admin password           |
| 400         | Missing parameter                |

