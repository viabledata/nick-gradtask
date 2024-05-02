## Flask Excel Reader

Small python service using Pydantic, Flask and SQLAlchemy to read a excel file.

## Setting up a python venv (Virtual Environment)
1. Create a new venv by using the following commands:
   ```bash
   python -m venv .venv
   ```
2. For macOS activate the venv by using the following command:
   ```bash
   source .venv/bin/activate
   ```
   or on windows use:
   ```bash
   .venv\Scripts\activate
   ```
3. install the required packages inside the venv using:
   ```bash
   pip install -r requirements.txt
   ```

## Install Guide
1. Clone this repository or download the files.
   ```bash
   git clone git@github.com:viabledata/nick-gradtask.git
   cd nick-gradtask
   ```
2. Install the required python packages
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tests using pytest before starting the flask service:
   ```bash
   python -m pytest tests -vv
   ```
4. Run the Flask app from the current directory using:
   ```bash
   flask run --debug
   ```

## How to Use
This project can be used with a tool like insomnia and can be accessed by visiting the available endpoints:
- /read [POST] sends a POST request to Flask and reads the excel file `static/Library_register_data.xlsx`
- /users/ [GET] sends a GET request to Flask and retrieves all users from the database.
- /users/`<name>` [GET] sends a GET request to flask with a name Path Variable.

## How to contribute:
To contribute to this project, the styleguide roughly follows the PEP-8 Style guide which can be found here:
> https://peps.python.org/pep-0008/

Aside from that ensure that functions have typehints & return types specified and a docstring 
stating what the function does.

1. Clone the repository to your local machine.
   ```bash
   git clone git@github.com:viabledata/documentation.git
   cd documentation
   ```
2. Create a new branch for your changes:
   ```bash
   git checkout -B your-branch-name
   ```

3. Make your changes and commit them:
   ```bash
   git commit -am "Remove pydantic and use marshmallow"
   ```

4. Push your changes:
   ```bash
   git push
   ```

Create a pull request from your branch to the main branch.
Wait for a reviewer to approve your pull request. Approval is required from two reviewers before pull requests
are merged.


