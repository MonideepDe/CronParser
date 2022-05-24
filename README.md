# Introduction
This is a simple cron parser.

<b>Input:</b> <br>
`*/15 0 1,15 * 1-5 /usr/bin/find`

<b>Output:</b> <br>
```
minute 0 15 30 45
hour 0
day of month 1 15
month 1 2 3 4 5 6 7 8 9 10 11 12
day of week 1 2 3 4 5
command /usr/bin/find
```

# Setup
- create a python virtual environment: <br>
    `python3 -m venv <Virtual Environment Name>`
- Activate the virtual environment: <br>
    `source <Virtual Environment Name>/bin/activate`
- Install required python packages. This is a one-time step <br>
    `pip3 install -r requirements.txt`

# How to run the program
- Once you are done with the setup and have the virtual environment activated, there are two ways to execute:
    - ## Using VS Code
        - We have included the necesarry `launch.json` files with this repository. Just go to "Run and Debug" section and RUN the configuration named `CronParser`
    - ## From Command Line
        - `export PYTHONPATH="<Repository Folder Path>"; python3 src/main.py "<Cron Entry String>"`
- To run the tests
    - ## VS Code
        - Go to "Tests" section on the left hand ribbon and select the tests to run.
    - ## From Command Line
        - From the top level directory of the repository, execute the command `pytest`