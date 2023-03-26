
## Set-up and Installation

### Prerequiites
    - Python 3.8

### Clone the Repo
Run the following command on the terminal:

### Create a Virtual Environment
Run the following commands in the same terminal:
```bash
sudo apt-get install python3.8-venv
python3.8 -m venv virtual
source virtual/bin/activate
```

### Install dependancies
Install dependancies that will create an environment for the app to run
`pip install -r requirements`

### Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### Running the app in development
In the same terminal type:
`python3 manage.py server`

Open the browser on `http://localhost:8000/`


### Assumptions
1. Only one customer is created from one potential lead
2. A lead_creator(One who creates the lead) only creates leads and nothing else
3. A customer_creator(One who turn leads into customers) only creates customers from leads and nothing else


**REST API endpoints:**

`/api/user/ (GET, POST) - get all products or create a new user and obtain a token to use during login`

`/api/login (POST) - authenticate user`

`api/lead_conversion/ (GET, POST) - get all leads or create a new lead`

`api/lead_conversion/:id (GET, PUT, DELETE) - get, update or delete a specific lead by its id`

`api/customer_creation/ (GET, POST) - get all customers or create a new customer from a lead`
`
/api/products/ (GET, POST) - get all products or create a new product`
