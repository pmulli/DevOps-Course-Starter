# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The application uses MongoDB to fetch and save to-do tasks. DB_CONNECTION_URL, TODO_DB_NAME and TODO_BOARD_ID variables need to be set in the `.env` file.
https://cloud.mongodb.com/v2/619cbd1bc2bd301fe7bf4421#clusters

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Authentication
The application's authentication is secured using GitHub OAuth.

### Authentication
The application's authorisation is secured using role based auth. Only users with a 'writer' role will be able to create and update items.

### Running the app in a virtual machine (vm)
- Download and install [`VirtualBox`](https://www.virtualbox.org/) hypervisor
- Download and install [`Vagrant`](https://www.vagrantup.com/)
- Start the app in the vm using:
```bash
$ vagrant up
```
- Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
- You can ssh into the vm using
```bash
$ vagrant ssh
```

### Running the app in Docker
Download and install [`Docker`](https://www.docker.com/get-started)
Build the docker image for development using:
```bash
docker build --target development --tag todo-app:dev .
```
Build the docker image for production using:
```bash
docker build --target production --tag todo-app:prod .
```
Run the development docker image using:
```bash
docker run -p 5000:5000 --env-file .env --mount type=bind,source="$(pwd)"/todo_app,target=/todo_app todo-app:dev
```
Run the production docker image using:
```bash
docker run -p 5000:80 --env-file .env todo-app:prod
```



## Testing the application

The project is using pytest for unit testing.

Add testing framework dependencies
- `Execute poetry add pytest selenium pytest-dotenv`

Add pytest as a dependency:
- Execute the `Python: Configure Tests` command on the Command Palette in Visual Studio Code
- Execute the `Python: Discover tests` command

Run unit and integration tests:
- From a terminal window and project directory, `poetry run pytest`
- With a test file open, select the `Run Test CodeLens` adornment that appears above a test method.
- Select `Run Tests` on the Status Bar
- In Test Explorer

Run Selenium Tests:
- Download Firefox
- Download geckodriver.exe and place in project root folder
- Exectue `poetry run pytest todo_app/tests_e2e` from project root

### Testing the app in Docker
docker build --target test --tag my-test-image .
docker run --env-file .env.test my-test-image tests
docker run --env-file .env my-test-image tests_e2e

## CI in Github Actions
https://github.com/pmulli/DevOps-Course-Starter/actions
Ensure secrets are added for DB_CONNECTION_URL, DOCKER_HUB_PASSWORD, DOCKER_HUB_USERNAME, HEROKU_API_KEY, SECRET_KEY

## CD in Heroku
https://dashboard.heroku.com/apps/todo-pdm

