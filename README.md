# Sportradar_Backend

OVERVIEW:

This application task/project is a basic relational database system with a scalable structure of tables and a basic frontend. It's in the 3rd normal form normalization, so there are no transitive dependencies and every entry is functionally dependent on a primary key. 
For demonstration I applied a function to import the test data which was sent in a JSON format into the specified databases tables. 
After the import you can display the data by using the index.html file and filter the entries by some parameters.

HOW TO USE:

This will give you a short instruction how to create the database, import the testfile and display the table on the index.html.

1. Download the repository and open it as a project in your IDE.
2. Run the database_handler.py file. This will create the .db file in your project folder.
3. Run the import_test_data.py file. This will read the sportData.json file in the project folder and import the data with the given structure.
4. Run the backend_logic.py file. This will run a Flask web application on your local port http://127.0.0.1:5000.
5. Open the address in your browser.
