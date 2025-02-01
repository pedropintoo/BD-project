# 2ano/2semestre/BD/BD-project

# Nota: 18.1

Pedro Pinto (115304)

João Pinto (104383)

# Base de Dados - Final Project

## Structure

The project is structured as follows:
- `persistency/` - Contains the database connection and the queries.
- `templates/` - Contains the HTML files for the project.
- `tables/` - Contains the SQL queries in the tables.
- `app.py` - Main file of the project. Contains the routes and the application configuration.
- `conf.ini` - Configuration file for the database connection.
- `pyproject.toml` - Poetry configuration file. Contains the project dependencies.

# SQL queries in the tables

The `tables` directory is structured as follows:

- `tables.py` - Contains the tables structure.
- `setup_tables.py` - Executes the SQL files:
    - `create_tables.sql` - Contains the SQL queries to create the tables. 
    - `create_indexes.sql` - Contains the SQL indexes. 
    - `create_procedures.sql` - Contains the SQL procedures. 
    - `create_udfs.sql` - Contains the SQL functions. 
    - `create_triggers.sql` - Contains the SQL triggers. 
- `clear_tables.py` - Contains the SQL queries to clear the tables. 
- `drop_tables.py` - Contains the SQL queries to drop the tables.

## Running

Then install the project dependencies with: `poetry install`.

You can then use: `poetry shell` to run the project.

To run the application, use the following command: `flask run --debug`
