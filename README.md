# Columbus

![PyPI](https://img.shields.io/pypi/v/columbus)



### What is Columbus?

Columbus is a Python web framework that automatically generates an async CRUD REST API web application from an SQLAlchemy table.

### How does it work?

Under the hood Columbus uses [Starlette](https://www.starlette.io), [Databases](https://pypi.org/project/databases/) and [SQLAlchemy](https://www.sqlalchemy.org) along with some interesting metaprogramming techniques to generate a web app based solely on your YAML specification and SQLalchemy table definition. 

### Installation

 ```pip install columbus```

### Quickstart

You can have your API up and running in only a couple of simple steps:

1. ```start```

	This command will generate two files for you:
	main.yml with a basic config template and an empty models.py.

2. **In models.py define your database table using SQLAlchemy.** <br><br>
	Then create the tables ([Alembic](https://alembic.sqlalchemy.org/en/latest/) is generally the recommended way to do this) and add some data whichever way you like. Columbus doesn't need you to connect to the database or write any queries for the app to work, it will do that for you. All you need to do is provide it with the database url.

3. **In main.yml add the database url** as a value for the 'database' key. **Add the name of your table** as the value for the 'table' key. <br><br>Here is a basic working example (provided you've set up the database with this url and your table is named my_table and located in models.py).

	```
	models: models.py
	database: postgresql://someuser:postgres@localhost/mydatabase
	APIs:
	  hello_world:
	    table: my_table
	    methods: [GET]
	```    
	


4. ```run```

	This command will run your app. **Navigate to localhost:8000/my_table and see your API in action**.
	
	
### Documentation

Here is a comprehensive list of possible keys and values in the YAML config.

Keys:

- **models**: relative path to the file where your SQLAlchemy table is defined


- **database**: valid database url

- **APIs**: the APIs you want Columbus to generate. Each API can be named whatever you want, but it has two mandatory keys:
	
	- **table**: name of SQLAlchemy table from which you want to generate the API
	
	-  **methods**: list of http methods (GET, PUT, POST, DELETE) you want the API to support. Attention: this is the only key that needs to be a list, so put the methods in square brackets.

Below is an example of a more comprehensive animals API, which should give you a feel for the correct YAML structure Columbus understands. Incorrect structures will throw an error and the app won't run.


```
models: models.py
database: postgresql://someuser:postgres@localhost/mydatabase
APIs:
  dogs:
    table: dogs
    methods: [GET, POST]
  cats:
    table: cats   
    methods: [GET, POST, PUT, DELETE] 
  snakes:
    table: snakes
    methods: [GET, POST, PUT]   
  bears:
    table: bears
    methods: [GET]    
```    
    
    
    
    
    
    
### What use cases does it support?

Columbus is still in the early days of active development, so it only supports the most basic use case for now. Feel free to open an issue for a missing feature and it will most likely be pushed to the top of the priority list and shipped soon.
            




	
	
	
