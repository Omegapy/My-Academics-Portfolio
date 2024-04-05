-- This is the first query:

SELECT DISTINCT year from population_years;

--3. Codecademy given first query:

SELECT DISTINCT year from population_years;

--4. largest population size for Gabon

SELECT year, population FROM population_years
WHERE country = 'Gabon'
ORDER BY population DESC
LIMIT 1;

--5. 10 lowest population countries in 2005

SELECT year, country, population FROM population_years
WHERE year = '2005'
ORDER BY population ASC
LIMIT 10;

--6. distinct countries with a population of over 100 million in the year 2010

SELECT DISTINCT country FROM population_years 
WHERE year = 2010 AND population > 100
ORDER BY country;

--7. countries in this dataset with the word “Islands” in their name

SELECT DISTINCT country FROM population_years
WHERE country LIKE '%Islands%'
ORDER BY country;

--8. population between 2000 and 2010 in Indonesia

SELECT year, population FROM population_years
WHERE country = 'Indonesia' AND year >= 2000 AND year <= 2010
ORDER BY year;
