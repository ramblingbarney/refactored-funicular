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
* ```npm install```
* ```export YOURAPPLICATION_SETTINGS=config.py``` to load app configuration file to the environment variables
* ```export FLASK_CONFIG=development``` to create FLASK_CONFIG environment variable for development version of the app
* ```export FLASK_CONFIG=production``` to create FLASK_CONFIG environment variable for production version of the app

### Running Tests

* Download the latest chromedriver binary: https://sites.google.com/a/chromium.org/chromedriver/downloads, for linux ensure the binary is in your path or for windows provide a full path 'c:\< >.exe' on line 21 of 'test_front_end.py'.  
* Install and run MongoDB (community edition) locally on the default port: https://docs.mongodb.com/manual/administration/install-community/
  * ```sudo chown -R <user>:<user> /data/db```
  * ```mkdir ~/mongo```
  * ```mkdir ~/mongo/mongodb```
  * ```cp /etc/mongo.conf ~/mongo/```
  * Update paths in mongo.conf to the absolute user path e.g. /home/<user>/mongo
  * ```mongo --host localhost``` Mongo Shell
  * ```use admin```
  * ```db.runCommand({getCmdLineOpts: 1})``` Verify setup of running local Mongo instance with expected output below
    ```
    {
    	"argv" : [
    		"mongod",
    		"--config",
    		"/home/<user>/mongo/mongod.conf"
    	],
    	"parsed" : {
    		"config" : "/home/<user>/mongo/mongod.conf",
    		"net" : {
    			"bindIp" : "127.0.0.1",
    			"port" : 27017
    		},
    		"processManagement" : {
    			"timeZoneInfo" : "/usr/share/zoneinfo"
    		},
    		"storage" : {
    			"dbPath" : "/home/<user>/mongo/mongodb",
    			"journal" : {
    				"enabled" : true
    			}
    		},
    		"systemLog" : {
    			"destination" : "file",
    			"logAppend" : true,
    			"path" : "/home/<user>/mongo/mongod.log"
    		}
    	},
    	"ok" : 1
    }
    ```

  * ```use recipe_app_testing```
  * ```db.createUser({user:"recipeapptester", pwd:"changeme5", roles:[{role: "dbOwner", db: "recipe_app_testing" }]})```

* Run the following commands
  * ```chromedriver --port=9515```
  * ```export FLASK_CONFIG=testing```
  * ```export YOURAPPLICATION_SETTINGS=config.py```
  * ```mongod --config ~/mongo/mongod.conf```
  * ```mongo --host localhost```
    * ```use recipe_app_testing``` Mongo Shell command
    * ```db.createUser( { user: "recipeapptester", pwd: "changeme5", roles: [ "readWrite", "dbAdmin" ] } )``` Mongo Shell command
  * ```python3 -m unittest tests/test_front_end.py```

## Acceptance tests

### Get Category (Show all fixture categories)

* As a user I want to see the categories that have been created from fixtures ['Meal for 1', 'Evening Meal for 2', 'Sunday Lunch for all the family'].

  * Example acceptance criteria:
    * 3 categories will be shown on the page ['Meal for 1', 'Evening Meal for 2', 'Sunday Lunch for all the family']

### Get Category (Show all fixture categories with Delete button)

* As a user I want to see the categories that have been created and each one will be shown with a 'Delete' button.

  * Example acceptance criteria:
    * Each category created will have a 'Delete' link/button
    * The page will have 3 'Delete' link/buttons

### Get Category (Show all fixture categories with Edit button)

* As a user I want to see the categories that have been created and each one will be shown with a 'Edit' button.

  * Example acceptance criteria:
    * Each category created will have a 'Edit' link/button
    * The page will have 3 'Edit' link/buttons

### Delete the first Category

* As a user I want to click on the 'Delete' link/button for the first category, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the first category line
    * The category entry is no longer shown

### Delete all the Categories

* As a user I want to click on the 'Delete' link/button for all categories, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the categories shown
    * All deleted categories will disappear
    * No category entries will exist to be shown

### Delete the last Category

* As a user I want to click on the 'Delete' link/button for the last category, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the last category line
    * The category entry is no longer shown

### Edit Last Category

* As a user I want to click on the 'Edit' link/button on the last category and that category will be shown individually on a page where it can be edited, cancelled and amendments saved.

* Example acceptance criteria:
  * An input box with the existing category text
  * links/buttons to create a 'Cancel' the amendment and 'Edit' (save) the category

* As a user I want to click on the 'Edit' link/button for a category and that category will be shown individually on a page where it can be cancelled and then all categories will be shown.

  * Example acceptance criteria:
    * Each category created will have a 'Delete' and 'Edit' link/button
    * Clicking on Edit will show that category individually with the text in an input box
    * Clicking will return the user to the all categories shown page

### Add Category

* As a user I want to add a category.

* Example acceptance criteria:
  * Entering text into the input box Category Name
  * Clicking button 'Add Category'
  * The recipe name will appear on the 'get_categories' page

### Get Cuisine (Show all fixture cuisines)

* As a user I want to see the cuisines that have been created from fixtures ['Thai','Chinese','Indian'].

  * Example acceptance criteria:
    * 3 cuisines will be shown on the page ['Thai','Chinese','Indian']

### Get Cuisine (Show all fixture Cuisines with Delete button)

* As a user I want to see the cuisines that have been created and each one will be shown with a 'Delete' button.

  * Example acceptance criteria:
    * Each cuisine created will have a 'Delete' link/button
    * The page will have 3 'Delete' link/buttons

### Get Cuisine (Show all fixture Cuisines with Edit button)

* As a user I want to see the cuisines that have been created and each one will be shown with a 'Edit' button.

  * Example acceptance criteria:
    * Each cuisine created will have a 'Edit' link/button
    * The page will have 3 'Edit' link/buttons

### Delete the first Cuisine

* As a user I want to click on the 'Delete' link/button for the first cuisine, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the first cuisine line
    * The cuisine entry is no longer shown

### Delete all the Cuisines

* As a user I want to click on the 'Delete' link/button for all cuisines, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the cuisines shown
    * All deleted cuisines will disappear
    * No cuisine entries will exist to be shown

### Delete the last Cuisine

* As a user I want to click on the 'Delete' link/button for the last cuisine, the page refreshes and it disappears

  * Example acceptance criteria:
    * Click on the 'Delete' link/button for the last cuisine line
    * The cuisine entry is no longer shown

### Edit Last Cuisine

* As a user I want to click on the 'Edit' link/button on the last cuisine and that cuisine will be shown individually on a page where it can be edited, cancelled and amendments saved.

* Example acceptance criteria:
  * An input box with the existing cuisine text
  * links/buttons to create a 'Cancel' the amendment and 'Edit' (save) the cuisine

* As a user I want to click on the 'Edit' link/button for a cuisine and that cuisine will be shown individually on a page where it can be cancelled and then all cuisines will be shown.

  * Example acceptance criteria:
    * Each cuisine created will have a 'Delete' and 'Edit' link/button
    * Clicking on Edit will show that cuisine individually with the text in an input box
    * Clicking will return the user to the all cuisines shown page

### Add cuisine

* As a user I want to add a cuisine.

* Example acceptance criteria:
  * Entering text into the input box cuisine Name
  * Clicking button 'Add Cuisine'
  * The recipe name will appear on the 'get_cuisines' page

### Get Recipes Headings (Show all fixture recipes headings)

* As a user I want to see the recipe headings that have been created from fixtures ['Avocado and Tuna Tapas', 'Chinese Pepper Steak', 'Moroccan Chicken with Saffron and Preserved Lemon'].

* Example acceptance criteria:
  * 3 recipes headings will be shown on the page ['Avocado and Tuna Tapas', 'Chinese Pepper Steak', 'Moroccan Chicken with Saffron and Preserved Lemon']

### Get Recipes Descriptions (Show all fixture recipes descriptions)

* As a user I want to see the recipe descriptions that have been created from fixtures.

* Example acceptance criteria:
  * 3 recipe descriptions will be shown on the page

### Add Recipe Name

* As a user I want to add a recipe name.

* Example acceptance criteria:
  * Entering text into the input box Recipe Name
  * Clicking button 'Add Recipe'
  * The recipe name will appear on the 'get_recipes' page

### Add Recipe Description

* As a user I want to add a recipe description.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button 'Add Recipe'
  * The recipe description will appear on the 'get_recipes' page

### Add Recipe Increase Total Time

* As a user I want to add a recipe total time to cook in increments of 15 minutes.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 15 mins'
  * The recipe Total Time will be 15 mins

### Add Recipe Decrease Total Time

* As a user I want to decrease the recipe total time to cook in increments of 15 minutes.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 15 mins'
  * Clicking button '+ 15 mins'
  * Clicking button '- 15 mins'
  * The recipe Total Time will increase to 30 mins and then decrease to 15 mins

### Add Recipe Total Time will be zero or more

* As a user I want the total time to cook to be zero or greater and never negative.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 15 mins'
  * Clicking button '+ 15 mins'
  * Clicking button '- 15 mins'
  * Clicking button '- 15 mins'
  * Clicking button '- 15 mins'
  * The recipe Total Time will increase to 30 mins and then decrease to 0 mins

### Add Recipe Increase User Votes

* As a user I want to increase the User Vote by 1.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 1' User Vote
  * The recipe User Votes will be 1

### Add Recipe Decrease User Votes

* As a user I want to decrease the User Votes by 1.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 1' User Vote
  * Clicking button '+ 1' User Vote
  * Clicking button '- 1' User Vote
  * The recipe Total User Votes will increase to 2 and then decrease to 1

### Add Recipe User Votes can be negative

* As a user I want the total User Votes to be negative.

* Example acceptance criteria:
  * Entering text into the input box Recipe Description
  * Clicking button '+ 1' User Vote
  * Clicking button '+ 1' User Vote
  * Clicking button '- 1' User Vote
  * Clicking button '- 1' User Vote
  * Clicking button '- 1' User Vote
  * The recipe User Votes will increase to 3 and then decrease to - 1

### Show Recipe

* As a user I want to click on the 'show' recipe link/button and be shown the full recipe (name, description, instructions and ingredients).

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

### Edit Recipe Category

* As a user I want to change the recipe category

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Change Category select box values
  * Click save
  * Clicking 'Show' loads page with Category changed

### Edit Recipe Cuisine

* As a user I want to change the recipe cuisine

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Change Category select box values
  * Click save
  * Clicking 'Show' loads page with Cuisine changed

### Edit Recipe Add One More Instruction

* As a user I want to add an additional instruction to an existing recipe

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Click the 'Add More Instructions' button
  * Enter instruction text into the new last instruction input box
  * Click save
  * Clicking 'Show' loads page with the additional instruction showing

### Edit Recipe Remove One Instruction

* As a user I want to remove an instruction for an existing recipe

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Click the 'Remove' button beside the instruction you want to remove
  * Click save
  * Clicking 'Show' loads page with the removed instruction not showing

### Edit Recipe Add One More Ingredient

* As a user I want to add an additional ingredient to an existing recipe

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Click the 'Add More Ingredient' button
  * Enter ingredient text into the new last ingredient input box
  * Click save
  * Clicking 'Show' loads page with the additional ingredient showing

### Edit Recipe Remove One Ingredient

* As a user I want to remove an ingredient for an existing recipe

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
  * Click the 'Remove' button beside the ingredient you want to remove
  * Click save
  * Clicking 'Show' loads page with the removed ingredient not showing

### Edit First Recipe Add Time

* As a user I want to change the first recipe total time

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '+ 15 mins' button
  * Click save
  * Clicking 'Show' loads page with the Total Time increased by 15 minutes

### Edit First Recipe Remove Time

* As a user I want to change the first recipe total time

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '- 15 mins' button
  * Click save
  * Clicking 'Show' loads page with the Total Time decreased by 15 minutes

### Edit First Recipe Remove All Time

* As a user I want to change the first recipe total time to zero and not be able to set a negative time

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '- 15 mins' button more times than the result of the initial total time divided by 15
  * Click save
  * Clicking 'Show' loads page with the Total Time of zero

### Edit First Recipe Add User Votes

* As a user I want to change the first recipe user votes

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '+ 1' User Vote button
  * Click save
  * Clicking 'Show' loads page with the User Votes increased by 1

### Edit First Recipe Remove User Votes

* As a user I want to change the first recipe user votes

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '- 1' User Vote button
  * Click save
  * Clicking 'Show' loads page with the User Votes decreased by 1

### Edit First Recipe Negative User Votes

* As a user I want to change the first recipe user votes to negative

* Example acceptance criteria:
  * Clicking 'Show' loads page with;
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes

  * Clicking 'Edit' loads page with:
    * Recipe name
    * Recipe description
    * Recipe instructions
    * Recipe ingredients
    * Recipe category
    * Recipe cuisine
    * Recipe Total Time
    * Recipe User Votes
  * Click '- 1' User Votes button as many times as required to enter a negative vote figure
  * Click save
  * Clicking 'Show' loads page with the Total Time of zero

### Delete the first Recipe

* As a user I want to click on the 'Delete' link/button for the first show recipe , the page refreshes and it disappears

  * Example acceptance criteria:
    * Click the show recipe button for the first recipe on the 'get_Recipes' page
    * Click on the 'Delete' link/button
    * When you return to the 'get_recipes' page it is no longer shown

### Delete the last Recipe

* As a user I want to click on the 'Delete' link/button for the last show recipe , the page refreshes and it disappears

  * Example acceptance criteria:
    * Click the show recipe button for the last recipe on the 'get_Recipes' page
    * Click on the 'Delete' link/button
    * When you return to the 'get_recipes' page it is no longer shown

### Delete all the Recipes

* As a user I want to click on the 'Delete' link/button for all the recipes on each show recipe page, the page refreshes and it is not shown on the 'get_recipes' page

  * Example acceptance criteria:
    * Click the show recipe button for each of the recipes on the 'get_Recipes' page
    * Click on the 'Delete' link/button
    * When you return to the 'get_recipes' page it is no longer shown

### Not Logged in Divert

* As a user I want to go to the 'get_recipes' page and be shown the 'login' page

* Example acceptance criteria:
  * As a user that is not logged in
  * Open http://localhost:5000/add_category
  * You are then redirected to http://localhost:5000/login

### Register (New & Existing User)

* As a user I want to enter username, email, passwords on the 'http://localhost:5000/register' page and then be redirected to the 'http://localhost:5000/' page

* Example acceptance criteria:
* Enter username, email, passwords on the 'http://localhost:5000/register' page
* You are then redirected to http://localhost:5000/

### Register (Password Validation Error)

* As a user I want to enter username, email, passwords on the 'http://localhost:5000/register' page and then be redirected to the 'http://localhost:5000/' page

* Example acceptance criteria:
* Enter username, email and two different passwords on the 'http://localhost:5000/register' page
* You are then shown the error message '[Passwords must match]'
* You are then redirected to http://localhost:5000/

### Register (Validation Errors)

* As a user I want to not enter in details and be shown the 'http://localhost:5000/register' page with validation error messages

* Example acceptance criteria:
  * No details are entered on http://localhost:5000/register and submit is clicked
  * Below the username and password field the error message '[This field is required.]' is shown in red
  * You are then redirected to http://localhost:5000/register

### Login (Success)

* As a user I want to enter in registered user details and be shown the 'http://localhost:5000/' page

* Example acceptance criteria:
  * Registered user enters email and password on http://localhost:5000/login
  * The flash message 'Welcome back, your logged in' is shown
  * You are then redirected to http://localhost:5000/

### Login (Failure)

* As a user I want to enter in registered user details and be shown the 'http://localhost:5000/login' page

* Example acceptance criteria:
  * Registered user enters email and password on http://localhost:5000/login
  * The flash message 'Sorry login failed' is shown
  * You are then redirected to http://localhost:5000/login

### Login (Validation Errors)

* As a user I want to not enter in registered user details and be shown the 'http://localhost:5000/login' page with validation error messages

* Example acceptance criteria:
  * No details are entered on http://localhost:5000/login and submit is clicked
  * Below the username and password field the error message '[This field is required.]' is shown in red
  * You are then redirected to http://localhost:5000/login

### Logout

* As a user I want to enter in registered user details and be shown the 'http://localhost:5000/add_category' page and then logout by visiting 'http://localhost:5000/logout' or clicking 'logout'

* Example acceptance criteria:
  * Registered user enters email and password on http://localhost:5000/login
  * You are then redirected to http://localhost:5000/add_category
  * You then click logout or visit 'http://localhost:5000/logout'
  * If you then visit 'http://localhost:5000/add_category' you are redirected to 'http://localhost:5000/login'

### Search No Recipe Results found

* As a user I want to enter text into the search box to search for Categories/Cuisines/User Votes and no recipes will be found/shown

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known not to exist
  * Click 'Search'
  * The user is shown the text 'No Recipes found'


### Search Recipe Results found

* As a user I want to enter text into the search box to search for Categories/Cuisines/User Votes and recipes will be found/shown

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist
  * Click 'Search'
  * The user is shown the Recipe header and description
  * The user is not shown the text 'No Recipes found'

### Search Recipes by Category, Results with Ascending User Votes

* As a user I want to enter text into the search box to search for Categories and the results to be returned with ascending user votes

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for categories
  * select the 'Categories' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching category with the first result having the lowest number of user votes with the rest of the results in ascending user vote order

### Search Recipes by Category, Results with Descending User Votes

* As a user I want to enter text into the search box to search for Categories and the results to be returned with descending user votes

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for categories
  * select the 'Categories' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching category with the first result having the lowest number of user votes with the rest of the results in descending user vote order


### Search Recipes by Category, Results with Ascending Total Time

* As a user I want to enter text into the search box to search for Categories and the results to be returned with ascending total time

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for categories
  * select the 'Categories' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching category with the first result having the lowest total time with the rest of the results in ascending total time order

### Search Recipes by Category, Results with Descending Total Time

* As a user I want to enter text into the search box to search for Categories and the results to be returned with descending total time

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for categories
  * select the 'Categories' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching category with the first result having the lowest total time with the rest of the results in descending total time order

### Search Recipes by Cuisine, Results with Ascending User Votes

* As a user I want to enter text into the search box to search for Cuisines and the results to be returned with ascending user votes

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for cuisines
  * select the 'Cuisines' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching cuisine with the first result having the lowest number of user votes with the rest of the results in ascending user vote order

### Search Recipes by Cuisine, Results with Descending User Votes

* As a user I want to enter text into the search box to search for Cuisines and the results to be returned with descending user votes

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for cuisines
  * select the 'Cuisines' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching cuisine with the first result having the lowest number of user votes with the rest of the results in descending user vote order


### Search Recipes by Cuisine, Results with Ascending Total Time

* As a user I want to enter text into the search box to search for Cuisines and the results to be returned with ascending total time

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for Cuisines
  * select the 'Cuisines' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching Cuisine with the first result having the lowest total time with the rest of the results in ascending total time order

### Search Recipes by Cuisine, Results with Descending Total Time

* As a user I want to enter text into the search box to search for Cuisines and the results to be returned with descending total time

* Example acceptance criteria:
  * Enter text to search for in the navigation bar that is known to exist for cuisines
  * select the 'Cuisines' search type
  * Click 'Search'
  * The user is shown the Recipe header and description for matching the matching cuisine with the first result having the lowest total time with the rest of the results in descending total time order

### Click on Bubble Graph Label with Cuisine results with Descending User Votes

* As a user I want to click on the graph bubble label and be shown that cuisine recipes by User Votes descending

* Example acceptance criteria:
  * Click on bubble graph label
  * The user is shown the Recipe header and description for matching the matching cuisine with the first result having the highest User Votes with the rest of the results in descending User Votes order

### Bubble Graph Label for no recipes stored

* As a user I want to see 'No Recipes, register to add recipes' as the graph bubble label when no recipes have been stored

* Example acceptance criteria:
  * The 1 bubble visible has the label 'No Recipes, register to add recipes'


## Manual Testing

### Required fields Add Recipe

* Open 'http:://localhost:5000/add_recipe.html' template, add text to all fields and select an option in the category select box, leave a different field empty or unselected select box each time and attempt to submit the form, a hover message should appear on the empty field or unselected select box stating input text required or selection required.

### Remember Me

* Open 'http:://localhost:5000/register.html' template, enter username, email, password and repeat password fields.  Go to 'http:://localhost:5000/logout' url and then go to 'http:://localhost:5000/login.html' and enter the same email and password with the 'remember_me' checkbox ticked.  Close the browser tab and then reopen and go to 'http:://localhost:5000/get_recipes', you should be shown the Recipes list page 'http:://localhost:5000/get_recipes.html' and not the 'http:://localhost:5000/login' page.

## Known Issues

* Mongo DB admin password has not been set & database setup is for local testing only
* When running all tests a resource warning is displayed for a number of unclosed sockets
  "ResourceWarning: unclosed <socket.socket fd=9, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('127.0.0.1', 55958), raddr=('127.0.0.1', 55261)>"
* Cuisines, Cateogries, Total Time, Recipes can have duplicates, I would recommend either having an index in the names and then using a switch to an update statement when the insert fails or using javascript checkon the page with a dummy route as used in my Stream 2A project
* If a user attempts to register the same email address twice the record is updated with the last password as the site doesn't have a lost password functionality
* The Bubble chart on the index page will show label text for 'Cuisines' without 'User Votes' but without a bubble
* The 'Spanish' label cannot be tested using the same unit tests as 'Indian' and 'Thai', I suspect the label has padding or leading spaces
