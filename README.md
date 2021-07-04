MyRecipes
A website designed for user's on the platform to share their recipes to other users on the platform. This project should give users the ability to create/edit/delete recipes. Generate profiles for users on login, and giving them the ability to modify it. Being able o subscribe and unsubscribe to users which will display their recipes on a personalised newsfeed for recipes. On the recipe page users can review the recipe by commenting or liking/dislike, and on the same page a recommendation tab will display a list of recipes that is "similar" to the current recipe.

**_ How to install your project _**
First, need to setup database.

- Name database rec, and change password in **init**.py accordingly.
- To connect to database use:
  psql -h localhost -p 5432 -U postgres rec
- Copy schema.sql into database.

Second, install dependencies

- Using the following line, installs all of the libraries inside requirements.md
- pip install -r requirements.txt

**_ Running the application _**
python main.py
