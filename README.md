# Sportradar_Backend

OVERVIEW:

This application task/project is a basic relational database system with a scalable structure of tables and a basic frontend. It's in the 3rd normal form normalization, so there are no transitive dependencies and every entry is functionally dependent on a primary key. 
For demonstration I applied a function to import the test data which was sent in a JSON format into the specified databases tables. 
After the import you can display the data by using the index.html file and filter the entries by some parameters.

HOW TO USE:

This will give you a short instruction how to create the database, import the testfile and display the table on the index.html.

1. Download the repository and open it as a project in your IDE. >> git clone https://github.com/Potterino/Sportradar_Backend.git
2. Install the requirements.txt file. >> pip install -r requirements.txt
3. Run the database_handler.py file. This will create the .db file in your project folder.
4. Run the import_test_data.py file. This will read the sportData.json file in the project folder and import the data with the given structure.
5. Run the backend_logic.py file. While this script is running, this will run a Flask web application on your local port http://127.0.0.1:5000.
6. Open the address in your browser.

ASSUMPTIONS:

1. I decided to create a Matches database to keep track of every single match which was shown in the JSON file. Even if the data structure doesn't show it explicitly int the file, i think it's the most practical way.
2. The modules I used to create this application are sqlite3 and flask since I already used them before and they are perfectly suitable for the demanded tasks.
3. The creation of databases that store the teams, the result of each game and the stage a match is played in are also useful, since it contributes to the scalability (add more teams and different stages).
4. Another database regarding the different stadiums would also be important in the final app, but since the value is always NULL in the JSON file, I left it out until this point.
5. Although there was no specific task to insert the JSON file data into the database, I found it very useful to have this file to see a possible structure. In addition to that, I thought it might be helpful to see the actual data in the database and eventually on the HTML page. That's why I decided to write a script for the import.
6. I added a form to add a new event. The home team, the away team, the date and the time are required fields. The default value for the season (if nothing is added via the form) is the current year.
   
