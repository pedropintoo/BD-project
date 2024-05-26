# SQL queries in the tables

This directory contains the SQL queries for the tables in the database.

## Structure

The directory is structured as follows:
- `tables.py` - Contains the tables structure.
- `create_tables.py` - Executes the SQL file.
- `create_tables.sql` - Contains the SQL queries to create the tables. 
- `insert_samples.py` - Contains the SQL queries to insert data into the tables.
- `clear_tables.py` - Contains the SQL queries to clear the tables. 
- `drop_tables.py` - Contains the SQL queries to drop the tables.


```sql

CREATE PROCEDURE Top3TopicsPerYear
AS
BEGIN
    SELECT PublicationYear, T.TopicName, TopicCount
    FROM (
        SELECT COUNT(L.TopicID) AS TopicCount, L.TopicName AS TopicName, RANK() OVER (PARTITION BY YEAR(PublicationDate) ORDER BY COUNT(L.TopicID) DESC, L.TopicName) AS rank_pub, YEAR(PublicationDate) AS PublicationYear
        FROM ListAllArticlesPerTopic() AS L
        INNER JOIN JournalVolume ON JournalVolume.JournalID = L.JournalID 
        GROUP BY L.TopicName, YEAR(PublicationDate)
    ) AS T
    WHERE T.rank_pub <= 3
    ORDER BY T.PublicationYear DESC, T.rank_pub
END;





```