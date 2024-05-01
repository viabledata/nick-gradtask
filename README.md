## Flask Excel Reader

Small python service using Pydantic, Flask and SQLALchemy to read a execel file.

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
3. Run the Flask app from the current directory using:
   ```bash
   flask run --debug
   ```

## How to Use
This project can be used with a tool like insomnia and can be accessed by visiting the avialable endpoints:
- /read [POST] sends a POST request to Flask and reads the excel file `static/Library_register_data.xlsx`
- /get/all [GET] sends a GET request to Flask and retrieves all users from the database.
- /get/`<name>` [GET] sends a GET request to flask with a name Path Variable.
