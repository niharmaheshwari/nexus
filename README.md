# nexus

## Contents
1. [About](#1-about)
2. [Team](#2-team)
4. [Issues](#3-issues)
5. [Setup](#4-setup)

___

#### 1. About
COMS - W4156 ADVANCED SOFTWARE ENGINEERING group project.

___

#### 2. Team

Name | UNI | GitHub ID
-----|-----| -----
Nihar Maheshwari | nm3223 | [@niharmaheshwari](https://github.com/niharmaheshwari)
Shantanu Jain | slj2142 | [@shantanu-jain-2142](https://github.com/shantanu-jain-2142)
Talya Koschitzky | tk2892 | [@tykosc](https://github.com/tykosc)
Vaibhav Goyal | vg2498 | [@vaibhav12345](https://github.com/vaibhav12345)

___

#### 3. Issues
Check [this](https://github.com/niharmaheshwari/nexus/issues) for active development tickets and issues.

#### 4. Tests
**Steps for running unit tests and coverage**
For running individual tests:
```
python3 -m unittest -v <test-module-path>
```

For running coverage:
```
coverage run -m unittest discover
```

For generating html report:
```
coverage html --omit="**/Library/*,*__init__.py" -d test/coverage
```
The above command generates a report in the `test` forlder.

**Sonar Test Link**
https://sonarcloud.io/dashboard?id=niharmaheshwari_nexus&branch=main&resolved=false

#### 5. Build and Run the service
**Steps for building and running the nexus service**
1. ssh to the ec2 server "3.135.193.250"
2. Login to the user nexus using the password 'nexus' without quotes
```
sudo su nexus
```
3. Switch to home directory
```
cd ~
```
4. Run the following commands, when prompted for ssh password enter "nexus123" without quotes
```
source env/bin/activate
tmux kill-server
tmux
./deploy.sh
```

#### 6. Building the Client UI
## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.


#### 7. API Documentation
# Project: Nexus
### NEXUS API Collection
This document enlists all the APIs with their parameters for Nexus.

## End-point: Signup
### Signup API
Allows the user to create an account with user details. Sends otp confirmation on the user email id.

#### Params:
- email: str, email address of the user.
- name: str, full name of the user
- birthdate: str, format(MM/DD/YYYY)
- phone_number: str, (code)xxxxxxxxxx
- password: str, with caps, special characters.

#### Note:
Email should be unique.
### Method: POST
>```
>{{hostname}}:{{port}}/auth/signup
>```
### Body (**raw**)

```json
{
    "email": "nm3223@columbia.edu",
    "name": "Nihar Maheshwari",
    "birthdate": "05/03/1997",
    "phone_number": "+19173784373",
    "password": "Admin@12345"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Confirm-Signup
### Confirm Signup
Verifies otp sent to the user's email address. It is valid for 24 hours. 

#### Params:
- email: str, email address for the user
- code: str, otp code (6 digits)
### Method: POST
>```
>{{hostname}}:{{port}}/auth/confirm-signup
>```
### Body (**raw**)

```json
{
    "email": "nm3223@columbia.edu",
    "code": "211011"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Login
### Login API
Allows the user to login using email and password.

#### Params
* email: str, user email
* password: str, user password
### Method: POST
>```
>{{hostname}}:{{port}}/auth/login
>```
### Body (**raw**)

```json
{
    "email": "nm3223@columbia.edu",
    "password": "Admin@12345"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Get-User-Details
### Get user details
Fetches the user details and returns a json. This is a protected API. User needs to have authorization id-token to call this API.

#### Params:
- email: str, email address of the user

#### Header:
- token: str, unique id_token for the user session.
### Method: POST
>```
>{{hostname}}:{{port}}/auth/get-user
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Body (**raw**)

```json
{
    "email": "nm3223@columbia.edu"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: InitGet
### Init API
Sample GET API.
### Method: GET
>```
>{{hostname}}:{{port}}/auth/
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: POST Snippet API
### POST SNIPPET API

- This endpoint is responsible for adding a new snippet by a specific user to the database.
- The POST body takes in 2 files, one is the code snippet itself { .py | .java | .cpp file } and the second file as the request body containing the metadata of the request itself.
- **IMPROTANT** : Ensure that both the files are present and are visible to postman so that the runner can pick these files and attach it to the request body.

#### Params:
- data: a json file representing the snippet metadata. Contains fields like:
  - tags : List of tags
  - description : Description
- file : A {.cpp | .py | .java} file having the actual code snippet.
### Method: POST
>```
>{{hostname}}:{{port}}/snippet
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Body formdata

|Param|value|Type|
|---|---|---|
|data|/Users/nmw/tmp/ips/test.json|file|
|file|/Users/nmw/tmp/ips/binary_search.py|file|



⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: GET Snippet API
### GET Snippet
- This request fetches a snippet given its snippet ID from the Dynamo Database.
- A valid fetch results in a 200 OK. 
- An invalid fetch (the case where the id does not exist) results in a 404 (NOT_FOUND)

#### Params:
- id : The ID of the snippet.
### Method: GET
>```
>{{hostname}}:{{port}}/snippet?id=f7e001ea-4689-11ec-a171-13e5113b32d1
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Query Params

|Param|value|
|---|---|
|id|f7e001ea-4689-11ec-a171-13e5113b32d1|



⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: PUT Snippet API
# PUT SNIPPET
- Use this method to update an existing code snippet **OR** its metadata.
- The method takes in the metadata { this parameter in the POST body is **MANDATORY** } which should have the id of the snippet being updated. 
- The second (and optional) parameter is the file which is the updated snippet.
- Note that there may be a case where the user just wants to update the tags and not the actual code file. In this case, the 2nd parameter is not at all required.

#### Params:
- data: a json file representing the snippet metadata. Contains fields like:
  - tags : List of tags
  - description : Description
- file : A {.cpp | .py | .java} file having the actual code snippet.
### Method: PUT
>```
>{{hostname}}:{{port}}/snippet
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Body formdata

|Param|value|Type|
|---|---|---|
|data|/Users/nmw/tmp/ips/test_update.json|file|



⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: DELETE Snippet API
### DELETE Snippet
- Use this request to delete a snippet from the database (and its relevant search indexes in elastic).
- User **MUST** specify the id of the snippet to be deleted

#### Params:
- id: The identifier of the snippet.
### Method: DELETE
>```
>{{hostname}}:{{port}}/snippet?id=8e0092ba-4640-11ec-81b9-1e003b213c26
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Query Params

|Param|value|
|---|---|
|id|8e0092ba-4640-11ec-81b9-1e003b213c26|



⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: GET Server Ping API
### SERVER PING
This is a utility method to check if the server is live. The path parameter for this server ends in ping. The server accordingly responds with a response body of "pong", indicating that the server is live and accepting requests.

#### Parameters:
None
### Method: GET
>```
>{{hostname}}:{{port}}/test/ping
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: GET Server Time API
### SERVER TESTS
This is a utility endpoint to check if the server is active. If active, the server responds with the current unix timestamp.

#### Parameters:
None
### Method: GET
>```
>{{hostname}}:{{port}}/test
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: GET Generate Dummy Data API
### GET Generate Dummy Data
- This endpoint is used to generate dummy data
- Dummy data is added to elasticsearch database 
and dynamodb

#### Parameters
- None
### Method: GET
>```
>{{hostname}}:{{port}}/dummy
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: General Search
### Search API
Allows the user to search for snippets efficiently. Full text matching will be applied on the language, tags, and descriptions of a user's snippets, and snippets that match will be returned. .

#### Params:
- search_string: str to use for searching
- email: str, email address of the user
### Method: POST
>```
>{{hostname}}:{{port}}/search
>```
### Headers

|Content-Type|Value|
|---|---|
|token|{{token}}|


### Body (**raw**)

```json
{
    "search_string": "binary",
    "email" : "shantanujainrko@gmail.com"
}
```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
_________________________________________________
Powered By: [postman-to-markdown](https://github.com/bautistaj/postman-to-markdown/)

