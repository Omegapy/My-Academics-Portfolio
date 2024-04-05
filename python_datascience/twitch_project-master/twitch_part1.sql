-------------------------------------------------------------------------
--                                                                         
--                   Codecademy Data Science course Python                 
--             Data Visualization with the Matplotlib Library
--                Twitch Part 1: Analyze Data with SQL         
--                                                                         
--                            "Twitch"                                     
--                                                                         
-------------------------------------------------------------------------

--------------------------
----- Getting Started
--------------------------
-- 1. Select all columns from the first 20 rows  from the tables stream and chat
SELECT * FROM stream LIMIT 20;
SELECT * FROM chat LIMIT 20;

-- 2. What are the unique games in the stream table?
SELECT DISTINCT game FROM stream;

-- 3. What are the unique channels in the stream table?
SELECT DISTINCT channel FROM stream;

----------------------------
----- Aggregate Functions
----------------------------

-- 4. What are the most popular games in the stream table?
SELECT game, COUNT(*) AS 'Number of Views' FROM stream
GROUP BY game
ORDER BY COUNT(*) DESC;

-- 5. Create a list of countries and their number of LoL viewers.
SELECT country, COUNT(*) AS 'Number of LoL Views' FROM stream
WHERE game = 'League of Legends'
GROUP BY 1
ORDER BY 2 DESC;

-- 6. Create a list of players and their number of streamers.
SELECT player AS 'Source', COUNT(*) AS 'Number of Streams' FROM stream
GROUP BY 1
ORDER BY 2 DESC;

-- 7. Create a new column named genre for each of the games.
SELECT game,
  CASE
    WHEN game = 'Dota 2' 
      OR game = 'League of Legends' 
      OR game = 'Heroes of the Storm'
        THEN 'MOBA'
    WHEN game = 'DayZ' 
      OR game = 'ARK: Survival Evolved'
        THEN 'Survival'
    WHEN game = 'Counter-Strike: Global Offensive'
        THEN 'FPS'
  ELSE 'Other'
  END AS 'genre', 
  COUNT(*)
FROM stream
GROUP BY 1
ORDER BY 3 DESC;

-----------------------------------------------------------
----- How does view count change in the course of a day?
-----------------------------------------------------------

-- 8. Query and take a look at the time column from the stream table
SELECT time FROM stream
LIMIT 10;

-- 9. SQLite comes with a strftime() function
SELECT time,
   strftime('%S', time)
FROM stream
GROUP BY 1
LIMIT 20;

-- 10. Let’s write a query that returns three columns
SELECT strftime('%H', time) AS 'Hour', COUNT(*) AS 'Number of Viewers'
FROM stream
WHERE country = 'US'
GROUP BY 1;

------------------------------
----- Joining the two tables
------------------------------

-- 11. Let’s join the two tables on that column.
SELECT * FROM stream
JOIN chat ON stream.device_id = chat.device_id;

