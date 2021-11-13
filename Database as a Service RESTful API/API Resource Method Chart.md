Objective = {
    Registration of a user
    Each user gets 10 tokens
    Store a sentence on our database for 1 token
    Retrieve his stored sentence on our database for 1 token
}
Methods = GET, POST, PUT, DELETE
Resources = Home, Register_User, Store_Sentence, Retrieve_Sentence, /


| Resource          | Method | Path      | User_For          | Params                                            | Status_Code                                                                                       |
|-------------------|--------|-----------|-------------------|---------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Home              | GET    | /         | Home page         | -                                                 | 200                                                                                               |
| Register_User     | POST   | /register | Register users    | username:string e password:string                 | 200 (OK) e 400 (Missing parameter) e 301 (Out of tokens) e 302 (Invalid username and/or password) e 303 (User already registered)|
| Store_Sentence    | POST   | /store    | Store sentence    | username:string, password:string e sentece:string | 200 (OK) e 400 (Missing parameter) e 302 (Invalid username and/or password)                       |
| Retrieve_Sentence | POST    | /retrieve | Retrieve sentence | username:string e password:string                 | 200 (OK) e 400 (Missing parameter) e 301 (Out of tokens) e 302 (Invalid username and/or password) |