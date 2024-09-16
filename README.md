# coretas-assignment
Solution to assignment from Coretas

## How to run

### Create a virtual environment

First, create and activate a virtual environment, named .venv, using this command:

#### Windows

```sh
py -m venv .venv
.\.venv\Scripts\activate
```

#### Linux

```sh
virtualenv .venv
source ./.venv/bin/activate
```

Note that this has only been tested on Windows, for now, using Python 3.12.6.


### Dependencies

Install the dependencies on the virtual environment from requirements.txt:

#### Windows

```sh
py -m pip install -r requirements.txt
```

#### Linux

```sh
pip install -r requirements.txt
```

Note that this has only been tested on Windows, for now, using Python 3.12.6.


### Running the project

Please make sure to add the host from which you will be running the frontend to CORS_ALLOWED_ORIGINS and CSRF_TRUSTED_ORIGINS in settings.py, in the tasks_app/tasks_app folder, before running the app! For example, http://127.0.0.1:5500 is already added and should work with the API if you use port 5500. A great way to run this project locally is using VSCode's Live Server extension, since it uses port 5500 by default.

#### Apply the migrations

```sh
python ./tasks_app/manage.py migrate
```

#### Start the development server

```sh
python ./tasks_app/manage.py runserver
```

#### CSRF Security

For registration, Django's CSRF security might prevent you from using the endpoint from a program such as Postman or Insomnia. If you want to use the endpoints like that, please make sure to add the ``@csrf_exempt`` decorator before the definition of the desired view. Make sure to also import it like so: ``from django.views.decorators.csrf import csrf_exempt``.

### Missing features

The backend has been almost fully completed. Most missing features are from the frontend.

#### Pagination

Pagination is missing from the frontend. There are various ways to implement it, like dropdown boxes for things such as page size, and/or an input of type text for page number.

Pagination works on the backend to avoid extra load on the database in cases when there's a lot of entries.

#### Filtering based on completion status

Filtering based on completion status is missing from the frontend. For that, we could add a button to make a request to get complete tasks only, or incomplete tasks only. Alternatively, we could change the design of the app. More on that on the next section.

In the backend, filtering works but only for completed tasks, provided that there's a non false ``filtered`` parameter on the GET request. Fixing this is really easy, it's a matter of parameters passing, and using the Task.objects.filter() function correctly.

#### Changing the design of the app

In hindsight, it would have been a better idea to use a table to display the list of tasks, and add an arrow or a button to each column name for filtering.

#### Usernames are case sensitive

Usernames are case sensitive. This can be fixed on the backend by calling lower on the username string before persisting on the database and before authentication.