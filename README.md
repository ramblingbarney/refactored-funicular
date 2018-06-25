# Stream 2B Flask Material UI application

The purpose of this application is provide an easy way to store, rate and use cooking recipes.

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](https://git-scm.com/)
* [Python3](https://www.python.org/) (with HomeBrew & Venv)
* [Google Chrome](https://google.com/chrome/)

## Installation

* ```git clone git@github.com:ramblingbarney/refactored-funicular.git```
* ```cd refactored-funicular```
* ```pip3 install -r /path/to/requirements.txt```

### Running Tests

* Download the latest phantomjs binary: http://phantomjs.org, update line 52 of 'test_front_end.py' to the location of the pantomjs binary.
* ```phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134```
* ```python3 -m unittest tests/test_front_end.py```
* ```python3 -m unittest tests/test_back_end.py```

* Create an mongo db instance called 'recipe_buddy_test' using mLab with;
  * User 'recipeapp' with read/write permissions
  * Collections
    * 'category'


## Acceptance tests


## Manual Testing



## Known Issues
