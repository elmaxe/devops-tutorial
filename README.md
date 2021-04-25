# CI for Python with unittest using GitHub Actions

# Introduction

In this tutorial you will learn how to set up a basic CI workflow for Python with GitHub Actions. You will learn how to set up unit tests and create an automated GitHub workflow that runs on pushes and pull requests to the master branch. The workflow will test and lint the code.

## What is unittest?
Unittest is a unit testing capable module in Python’s standard library.

## What is flake8?
Flake8 is a tool to lint your code, in other words make sure it follows a certain style convention, which can be customized in any way you want.

## What is GitHub Actions?
GitHub Actions automates your CI/CD workflows. You can build, test and deploy your code right on GitHub. In this tutorial we will use GitHub Actions to automatically lint the code and run unit tests when you push to master or create a pull request to the master branch.

## Prerequisites
This tutorial is written for and intended to run on Ubuntu/Windows 10 with:
- Python 3.8
- Git

# Step 1 - Set up project
Start by setting up the file structure of the project. The structure will look like this:
```
example_project/
├── .github/
|    └── workflows/          
|    	    └── ci.yml    GitHub Action configuration.
├── src/                  Python package with source code.
|    ├── __init__.py      Makes the folder a package.
|    └── app.py           Example module.
├── test/                 Python package with source code.
|    ├── __init__.py      Makes the folder a package.
|    └── test_app.py      Example test module.
├── requirements.txt
├── .gitignore
└── README.md             README with info of the project.
```

Create the `src` and `test` folders. These will hold our source code and our unit tests respectively. Make sure to create an empty `__init__.py` file in both folders. This file creates a module from the folder it is resided in, which makes us able to import functions. When writing unit tests we would for example like to import functions from `src/` and use them in unit tests.

For the next step, we will provide some examples of source code and their unit tests. Create `app.py` and paste the following code:
```python
import random

default = ["Meh", "Boring", "What about it?", "Nothing special"]
present = 2021

def review(year):
    if not isinstance(year, int):
        raise TypeError("Expected int, received {x}".format(x = type(year).__name__))
    if year > present:
        raise ValueError("Can't review a year that has not happened yet (year > {x})".format(x = present))
    if year == 0:
        return "Jesus Christ what a year!"
    elif year == 42:
        return "A year worth living for"
    elif year == 1337:
        return ":sunglasses:"
    elif year == 1984:
        return "You never felt alone"
    elif year == 1987:
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    elif year == 2020:
        return "Sad year :("
    else:
        return default[random.randint(0, len(default) - 1)]
```

This code implements a function `review()`, which “reviews” the year you pass to it, returning a string.

## Implement unit test
It’s time to write some unit tests for this function. Create the file `test_app.py` in the `test`-folder and paste the following code:
```python
import unittest
from src.app import review, default, present

class TestApp(unittest.TestCase):

    def test_review_should_return_default(self):
        self.assertIn(review(1), default)
        self.assertIn(review(-10), default)
        self.assertIn(review(2021), default)

    def test_review_should_not_return_default(self):
        with self.subTest(msg="year = 0"):
            self.assertEqual(review(0), "Jesus Christ what a year!")
        with self.subTest(msg="year = 42"):
            self.assertEqual(review(42), "A year worth living for")
        with self.subTest(msg="year = 1337"):
            self.assertEqual(review(1337), ":sunglasses:")
        with self.subTest(msg="year = 1984"):
            self.assertEqual(review(1984), "You never felt alone")
        with self.subTest(msg="year = 1987"):
            self.assertEqual(review(1987), "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with self.subTest(msg="year = 2020"):
            self.assertEqual(review(2020), "Sad year :(")

    def test_review_invalid_type_raise(self):
        self.assertRaises(TypeError, review, "42")
        self.assertRaises(TypeError, review, 42.3)

    def test_review_future_year_raise(self):
        self.assertRaises(ValueError, review, present + 1)
```

This file can sure look a bit complicated if you are not used to unit tests. First and foremost we import the `unittest` library so that we can use its functions. After that we create a class that extends the `unittest.TestCase` class. All unit test functions in this class must have names beginning with `test` in order for unittest to recognize them as unit tests. The class contains four different unit tests that test the review function in different ways.

There are many different ways to design your unit tests. We have used three different kinds of assertions: `assertEqual`, `assertRaises` and `assertIn`, but there are many more you can use. If you are interested, read the [unittest documentation](https://docs.python.org/3/library/unittest.html).

- `assertEqual` tests that a value is equal to a specific value, in our case we use it to check that when we review a specific year we get the correct string output returned to us.
- `assertIn` tests that the provided value is in the provided array. This can be used when you want to accept different answers, in our case when we want to accept any default answer from the review function.
- `assertRaises` tests that an error is raised. We use it to test that `review` raises an error when inputting something other than an integer as argument to the function and to check that you’re not reviewing a year greater than the current year.

### Sub tests
When creating unit tests, it is common to insert many assertions into one function, making that function contain a lot of assertions. If one of these assertions would fail, `unittest` wouldn’t tell us which of them failed. Instead, it would only tell us in what test function the error occurred. Sub tests solve this problem. By dividing the test into sub tests, `unittest` will tell you specifically which assertion failed, making it easier to see what went wrong. We implemented subtests in the `test_review_should_not_return_default` function.

## Misc files
Before we are done, create two more files in the root of the project: `requirements.txt` and `.gitignore`. In the `.gitignore`, paste `__pycache__` so that git won’t keep track of changes to these folders.

`requirements.txt` is a file that lists what dependencies a Python project has. In our case, we only have one dependency: `flake8`. Type that into `requirement.txt` and save it.

# Step 2 - Run the code
First, we need to install the dependencies we just configured. This is done by running the following in the root of the repo:
```
pip install -r requirements.txt
```

Run `python -m unittest` to run the unit tests. If everything is set up correctly, it should tell you that it ran some number of tests and if they succeeded or not.

Run `flake8 .` to see that flake8 is installed and runs on your code. Flake8 will probably give you some errors and warnings about the format of your code.

If everything ran successfully you can push the code to your repo, and you are ready to go to the next step: creating a pipeline that does these things automatically for you.

> **Note:** If you have multiple Python version on your computer, you may run into problems when you run these commands. In that case, you need to specify which Python version you use when running the commands. Therefore, run the following commands instead
```
<python> -m pip install -r requirements.txt
<python> -m unittest
<python> -m flake8 .
```
where you substitute `<python>` with `python3` on Ubuntu and `py -3.8` on Windows.

# Step 3 - Configure CI pipeline with GitHub Actions
GitHub looks for definitions of GitHub Actions in a directory named `.github/workflows` in your repo. Therefore, you need to create such a directory and in that directory create a YAML file defining a new GitHub Actions workflow. You can name this to whatever you like, we chose `ci.yml`. The final version of the file includes the following:

```yml
name: CI

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test
      run: python -m unittest
```

This file may look a bit complicated if you are unfamiliar with the YAML syntax and GitHub Actions. Do not be scared, we will explain the content of the file in the following sections.

## Name the workflow
We define a name for our workflow with the `name` keyword. To give the workflow the name “CI”, you write:

```yml
name: CI
```
You can of course choose another name than “CI”.

## Trigger workflow by certain events
Since we want to test new code, we would only really want to build and test when there is a new push or a new pull request. To trigger the workflow on all push and pull request events, we would add the following to our YAML file:
```yml
on: [push, pull_request]
```
If we have multiple branches and only want our CI workflow to run when there are new things on a specific branch, we could instead rewrite the `on` value to:
```yml
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
```
This is the configuration used in our YAML file. It is possible to add multiple branches to the `branches` list, and also possible to add other restrictions for the `on` value. You can read more about the `on` workflow syntax [here](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#on).

## Define jobs in the workflow
A workflow can consist of one or more jobs. These jobs will run in their own environments and will therefore not share any data. However, it is possible to configure jobs to be dependent on the status of other jobs. To define jobs in our workflow we use the `jobs` keyword. The basic syntax for this keyword is:
```yml
jobs:
    <job1 id>:
        <job1 specification>
    <job2 id>:
        <job2 specification>
    ⋮
```
As id we can write any string containing only alphabetical characters, `-` or `_`. If you define multiple jobs inside the `jobs` environment, you must make sure they get unique ids. In our workflow we have defined a single job with the id `test`.

The `<job specification>` consists of multiple key-value pairs. First, we use the `runs-on` keyword to specify the OS that should be used by GitHub when running the job. Since we want to use Ubuntu, we have added
```yml
runs-on: ubuntu-latest
```
to our `<job specification>`. You can find a full list of possible OSs [here](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idruns-on).

To define the actions that should be executed in the job, we use the `steps` keyword. The general syntax for this keyword is:
```yml
steps:
    - <step 1 specification>
    - <step 2 specification>
    ⋮
```
The `<step specification>` also consists of multiple key-value pairs. There are three important keywords here:
- `name` -  specify the name of the step
- `uses` -  specify that a predefined action should be executed during the step
- `run` - specify specific commands that should be executed during the step

In our test job we will perform the following steps:
1. Clone the repo
2. Install Python
3. Install the dependencies of our Python project
4. Lint, i.e. run static analysis to check syntax and code complexity
5. Run the tests

### Clone the repo
For the job to get access to the code in our repo we use the action [`actions/checkout`](https://github.com/actions/checkout). This will fetch the repo in the state it had when the event that triggered the workflow occured. To specify that we want to use the latest version of the action, version 2, we specify the step as:
```yml
- uses: actions/checkout@v2
```

### Install Python
To install Python in our job environment we use the action [`actions/setup-python`](https://github.com/actions/setup-python). When using this action, we must specify the Python version to use. This is done with the `with` keyword. We can specify a step that installs Python version 3.8 as:

```yml
- name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
```
#### Multiple Python version
If you want to support multiple Python versions (e.g. 3.8 and 3.7) and want to test all of them, it is possible to add
```yml
strategy:
      matrix:
        python-version: [3.8, 3.7]
```
to the job specification. Then we can modify the “Set Up Python” step to use the different versions:
```yml
- name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
```
With this setup, GitHub will launch one job for each Python version. You can read more about the `strategy` and `matrix` keywords [here](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix).

### Install dependencies
To install the dependencies we use [`pip`](https://pypi.org/project/pip/), a package installer for Python. We install pip with `python -m pip install --upgrade pip`, and then install the project dependencies by running `pip install -r requirements.txt`, which will install all modules defined in `requirements.txt`. A step running these commands can be defined as:
```yml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

### Lint
Our linting step is defined as:
```yml
- name: Lint
  run: |
    # stop the build if there are Python syntax errors or undefined names
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```
This step is divided into two parts. One part that catches fatal errors such as syntax errors and/or undefined names, and one part that checks everything else, but as a warning and not an error. This means that if there is a syntax error, the CI job will fail, but if there is one too many newlines, the linter will only produce a warning and not fail the job.

You can customize this however you want. You could for example be very strict and fail at the slightest rule break. Read more about the different flake8 options [here](https://flake8.pycqa.org/en/latest/manpage.html).

### Run tests
The tests are run with `python -m unittest`. Hence, a step running the tests can be configured as:
```yml
- name: Test
  run: python -m unittest
```

# Step 4 - Check that everything works
If you push all the files we have written in the previous steps to your GitHub repo, your new workflow should be triggered. If you open the repo and go to the "Actions" tab, your CI workflow should be listed. If you click on it, you should be able to see that your it is running and get access to its logs.

**Congratulations!** :star2:

You have now completed the tutorial.
