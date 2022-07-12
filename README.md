# RestAPI for books.json file

This application reads `books.json` file and provides three endpoints for user:

- `/api/book/{isbn}` witch is used to retrieve book with specified ISBN number
- `/api/category/{categoryName}/books` witch is used to return books in provided category
- `/api/rating/category` witch list categories with average rating of books in every category

For two first endpoints if provided value didn't exist in books.json application will return response `404`. 
Application address is `127.0.0.1:4000` and under the address `127.0.0.1:4000/docs` is located the documentation for this 
application with possibility to test how it works.

## 1. How to run this application
To run this application navigate to folder where application is located and type following command:

### For Linux
`source venv/bin/activate`
### For Windows
`C:\<path_to_api_folder>\venv\bin\activate`

or

`C:\<path_to_api_folder>.\\venv\bin\activate`

After running the virtual environment stay in the same location in CLI/CMD and just simple run the API.py:

### For Linux
`python3 API.py`
### For Windows
`python API.py`

If application raise an error `NoModuleNamed ...` it means that your environment is missing one or more modules required 
to run this app. To solve this problem installs required modules from `requirements.txt`

### For Linux and Windows (change / to \)
`pip install -r <path_to_requirements>/requirements.txt`

## 2. Changing localization of books.json file
If for some reason You want to change the location of `books.json` file open the `dir` file and type new path 
as `<path_to_file>/<name_of_file>.json` 
Application will read this file and take the path from it.
