# Flanks Python Library
The Flanks Python library provides convenient access to the Flanks API from applications written in the Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically from API responses which makes it compatible with a wide range of versions of the Flanks API.

## Documentation

Soon

## Installation

Soon

### Requirements
* Python 3.4+

## Usage

### Initialize Client
Basic usage for initialize the client.

```
import flanks
API_TOKEN = 'TOKEN_API'
flank = Flanks(API_TOKEN)
```

### Create User
Creating users. Fill BANK_USERNAME, BANK_PASSWORD, BANK, BANK_PASSWORD2 with real data.

```
import flanks
API_TOKEN = 'TOKEN_API'
flank = Flanks(API_TOKEN)
username='BANK_USERNAME'
password='BANK_PASSWORD'
bank='BANK'
password2='BANK_PASSWORD2' #If it is necessary
user_token = flank.create_user(username, password, bank, password2)
```


### GET DATA OF USER
You only need one line:

```
    user = flank.get_data(user_token)
```