# UBase
It is a basic django 2.2 application with in-build features like:

1. [User Management](#user-management)
2. Permission Management 
3. Localities Management
   2. Erg
      3. Erg
        
4. Lookups Management
5. Notification Management
6. Common Functionality

and many more.


## User Management
To be completed...


## How To setup in local machine  

1. Setup AWS CLI Profile.
    ~~~shell script
    $ aws configure --profile `your-profile`
    ~~~
    and add information as and when required.  
    Click 
    [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html "Configuring the AWS CLI")
    for Configuring the AWS CLI.  

2. Clone
    ~~~bash
    $ git clone https://git-codecommit.ap-south-1.amazonaws.com/v1/repos/ubase-backend -c credential.helper='!aws codecommit credential-helper --profile `your-profile`  $@' -c credential.UseHttpPath=true .
    ~~~

    **Note :**  
    Remove `your-profile` with your profile name.
    
3. setup virtual env
4. setup pip
5. runserver
    
#Coming soon:
1) add permission, auth, change/reset password, user management, login 
2) add django-filter
3) .env for environment setup
4) lookups
5) notification
6) add example .env in readme doc  
  
  
---
#Tips & Tricks

### 1) To access postgres remotely

Add listen_addresses
```shell script
$ sudo nano /etc/postgresql/10/main/postgresql.conf
$ listen_addresses = '*'
```

Add remote ips
```shell script
$ sudo nano /etc/postgresql/10/main/pg_bha.conf
```
add `host all all all md5` at last
# uBase-shivansh-
