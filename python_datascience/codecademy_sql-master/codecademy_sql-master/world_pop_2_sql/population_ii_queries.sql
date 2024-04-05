-- This is the first query:

SELECT DISTINCT year from population_years;

--3 How many entries in the countries table are from Africa?

SELECT COUNT(*) AS total_countries_from_africa
FROM countries
WHERE continent = 'Africa';

--4 What was the total population of the continent of Oceania in 2005?

  -- Using INNER JOIN, best solution

SELECT ROUND(SUM(population), 2) AS 'total_population_oceania_2005'
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE year = 2005 AND continent = 'Oceania';

  -- Using the WITH clause, creating an oceania temporary table 

WITH oceania AS (
  SELECT id 
  FROM countries
  WHERE continent = 'Oceania'
)
SELECT ROUND(SUM(population), 2) AS 'total_population_oceania_2005'
FROM population_years
JOIN oceania
  ON population_years.country_id = oceania.id
WHERE year = 2005; 

--5 What is the average population of countries in South America in 2003?

SELECT ROUND(AVG(population), 2) AS 'average_country_population_south_america_2003'
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE year = 2003 AND continent = 'South America';

--6 What country had the smallest population in 2007?
 
SELECT countries.name AS 'country_smallest_population_2007', MIN(population) AS 'population'
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE year = 2007;

--7 What is the average population of Poland during the time period covered by this dataset?

SELECT countries.name AS 'country', ROUND(AVG(population), 2) AS 'average_population_in_the_dataset'
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE country = 'Poland';

  -- question 7 solution listing the period covered by the dataset with the aliases from_year to_year 
  
SELECT countries.name AS 'Country', 
       ROUND(AVG(population), 2) AS 'average_population', 
       MIN(year) AS 'from_year', MAX(year) AS 'to_year' 
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE country = 'Poland';

--8 How many countries have the word “The” in their name?

SELECT COUNT(*) AS 'counties_with_The_in_name'
FROM countries
WHERE name  LIKE '% The %' OR name LIKE '% The' OR name LIKE 'The %'; 
/* Looking for the WORD "The", 
(the question asks for the word "The", 
it does not ask for the string made of the letters "The"). */

   -- countries with the word “The” in their name
   
SELECT name AS 'countries_with_The_in_name'
FROM countries
WHERE name  LIKE '% The %' OR name LIKE '% The' OR name LIKE 'The %';

--9 What was the total population of each continent in 2010?

SELECT countries.continent, ROUND(SUM(population), 2) AS 'total_population_2010'
FROM population_years
JOIN countries
  ON population_years.country_id = countries.id
WHERE year = 2010
GROUP BY 1
ORDER BY 2 DESC;