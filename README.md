# Block2School backend project

## Requirements  
- Python 3.9.10 or more (must be executed in bash with the command `python3`)
- pip 22.0.4 or more

## Installation  
- Execute `start.sh` script to run the project

## How to see all routes ?  
All routes are documented. The documentation is available at: `localhost:8080/docs`  
_Replace `localhost` with the good url if you are not in local mode_

## Do a migration of the database  

>**To do this part, you need to add this into your .env: `DB_VERSION=0`**
- Launch from root path `bash scripts/create_db_update.sh`
- Enter a file name
- Open created python file
- Create your migration inside (you can see an [example here](/db/1_tutorial_table.py))
- Push your python file **AND** the [`version`](/db/version) file
- Your database will be updated when you will use the script `start.sh`

_Read the wiki to see more informations on this project_
