<h3> What is Columbus? </h3>

Columbus is a tool that generates a working async REST API web application from only two pieces of user input: a simple yaml config and an SQLAlchemy database table. 

<h3> Installation and quickstart </h3>

``pip install columbus``

``start`` This command will generate two files: 'main.yml' and 'models.py'

``run`` This will run the very basic web application.

These three commands are enough to run a basic hello world application. However, for Columbus to actually do its magic you will first need to write the database table definition in models.py, set up the database and make migrations. After that, Columbus will do all the work for you, no coding necessary. Based on the methods (GET, POST, PUT, DELETE) specified in the yaml config, Columbus will generate the corresponding API endpoints and their urls (those will be generated from the name of your database table).

<h3> How does it work? Does it fit my use case? </h3>

Columbus is built on top of Starlette, just like <a href="https://fastapi.tiangolo.com">FastAPI</a>, so it is async and just as fast. However, it serves a slightly different purpose. It is less of a framework and more of a code generator. It's built for the most general use case: you are building a simple CRUD REST API and you are finding yourself having to write a lot of boilerplate. If you need the flexibility of having to do operations on your data before returning it to the user as JSON, Columbus is not for you (at least not in its current form). But if all your code does is perform database queries and returns JSON objects, then congratulations: Columbus can do that for you! No coding, no testing. Your API is basically ready to deploy.

<h3> Is it actually production ready? </h3>

Probably not, yet. All the aforementioned features are present and working, but integration tests need to be added to the test suite before we can confidently recommend it for production. Bug reports and contributions are very welcome!
