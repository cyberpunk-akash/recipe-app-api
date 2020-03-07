# Recipe App API  
The recipe app API lets you create, modify and view tags and ingredients. You can create your own custom recipes using these tags and ingredients.  

## Technology Stack:  
**Language**: Python3  
**Frameworks**: Django2, Django-REST   
**Database**: PostgreSQL  
**PAAS**: Docker  

The project has been built using **_Test Driven Development_(TDD)**, thus contains automated tests to test multiple functionalities of API.  

## API Endpoints:

**POST**   _/api/user/create_ (To create authenticated users)  
**POST**  _/api/user/token_ (Post credentials to get the token as output)  
**GET**  _/api/user/token_ (Get the token as output and add it to ModHeader under the name **Authorization**)  
**PUT/PATCH**  _/api/user/me_ (To edit the credentials of user)  
**GET**  _/api/recipe_ (Router to access recipe, tags and ingredients endpoints)  
**POST** _/api/recipe/tags_ (Add a tag)  
**GET** _/api/recipe/tags_ (View tags)  
**POST** _/api/recipe/ingredients_ (Add a ingredient)  
**GET** _/api/recipe/ingredients_ (View ingredients)  
**POST** _/api/recipe/recipes_ (Add a recipe)  
**GET** _/api/recipe/recipes_ (View recipes)  
**GET** _/api/recipe/recipes/<recipe-id>_ (View the particular recipe details)  
**PUT/PATCH/DELETE** _/api/recipe/recipes/<recipe-id>_ (Modify or delete the particular recipe details)  
**POST**  _/api/recipe/recipes/<recipe-id>/upload-image_ (Upload image for the particlar recipe)  
**GET** _/api/recipe/recipes/?tags=x&ingredients=y_ (Lists all recipes with tag-id=x and ingredient-id=y )  
**GET** _/api/recipe/tags/?assigned-only=1_ (Lists only those tags which are used in atleast one recipe)  
**GET** _/api/recipe/ingredients/?assigned_only=1_ (Lists only those ingredients which are used in atleast one recipe)  


## How to run the application?
You need to follow these steps after cloning:
- Install python3
- Install pip
- Install Docker
- Configure PostgreSQL on the system
- Change the password of PostgreSQL in docker-compose.yaml file
- Install a text editor(preferably Atom or Sublime) to view the files.
- Run the commands:
```docker
    docker-compose build
    docker-compose up
```
- If the last command doesn't show any error, the API will be available at _localhost:8000_
