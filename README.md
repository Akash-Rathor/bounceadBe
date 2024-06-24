# WorkFors Backend

## Author and developer

- Akash Rathor

## Getting started

To make it easy for you to get started with this project, here's a list of recommended next steps.

## Clone repository in your local system


```
cd your_folder_where_you_want_to_clone_it
git clone https://github.com/Akash-Rathor/myprojectname.git
git checkout dev

```

## reset project name to your project name
```
ctrl+shift+f (VS code shortcut to search content throughout project)
search - myprojectname
replace with - your_proejct_name

update folder name of myprojectname to your_proejct_name

```

## Setup virtual environment

```
cd myprojectname
python3 -m venv .myprojectname
source myprojectname/bin/activate

```
## Install Dependencies

```
cd myprojectname
pip install -r requirements.txt

```

## setup .env file
 > [!NOTE]
 > Change the value as per your local setup

```
 - Go to Console and copy ".env.copy" to ".env" in the same folder
 - cp /path/to/.env.copy /path/to/.env
 ```




# Once database connection is set:
**1. Run Migrations**
```
    - python manage.py makemigrations
```

# DEV TAILWIND SETUP START

## DEVEPMENT-ONLY to start working with tailwind css
> [!IMPORTANT] 
> _This step is not required in deployment step_
> Skip to [DEV TAILWIND SETUP START END](https://github.com/Akash-Rathor/myprojectname?tab=readme-ov-file#next-steps-below)

```
- make sure you have npm installed in your machine
```
**Check node version if already installed**
```
 - node -v
 - npm -v
```

**otherwise run these commands to install**
- Go to https://nodejs.org/en/download/ and follow the steps

> this is required as this project uses tailwind css
> go to console and run following commands
```
    - npm install
```
**start changing or create new html file and use tailwind in it, to apply changes run command**
> command to reflect your changes on webpage
```
    - npm run build

```
# DEV TAILWIND SETUP END HERE

# NEXT STEPS BELOW

> [!IMPORTANT]
> This step is important only on deployment, not required for development
```
    - python manage.py collectstatic

```

## Start Server

> [!TIP] 
> *1- If you wanna run on localhost:8000 or 127.0.0.1:8000*

```
 - Go to Console and type below command
 - python manage.py runserver

```

> [!TIP] 
> *2- If you wanna run on your IP address*

```
 - Go to Console and type below command
   ~~e.g : python manage.py runserver <your ip address>~~
 - python manage.py runserver 196.128.13.31:8000

```