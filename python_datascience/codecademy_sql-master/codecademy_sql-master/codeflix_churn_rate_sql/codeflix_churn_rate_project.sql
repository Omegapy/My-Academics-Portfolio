
/*-------------------------------------------------------------------------*
 *																		                                     *
 *  Codecademy Data Science course SQL                                     *
 *  Analyze Real Data with SQL section                                     *
 *  User Churn with Codeflix                                               *
 *                                                                         *
 *-------------------------------------------------------------------------*/
 
 
/*-----------------------------*
 * Get familiar with the data  *
 *-----------------------------*/
 
---------------------------------------------------------------------------
--1. Take a look at the first 100 rows of data in the subscriptions table.
---------------------------------------------------------------------------

SELECT *
FROM subscriptions
LIMIT 100;

 -- How many different segments do you see?
 
SELECT DISTINCT segment
FROM subscriptions;

--2. Determine the range of months of data provided. 

SELECT 
    MIN(subscription_start) AS 'range_from_date',
    MAX(subscription_end) AS 'range_to_date'
FROM subscriptions;

/*----------------------------------------*
 * Calculate churn rate for each segment  *
 *----------------------------------------*/

----------------------------------------
--3. Create a temporary table of months
----------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
)
SELECT *
FROM months;

-------------------------------------------------------------------------------
--4. Create a temporary table, cross_join, from subscriptions and your months.
-------------------------------------------------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
------------------------- Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
)
------------------------- Query
SELECT *
FROM cross_join
LIMIT 10;

-----------------------------------------------------------------------------
--5. Create a temporary table, status, from the cross_join table you created.
-----------------------------------------------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    -- Checking if the customer's subscription is active during each individual months  
    CASE -- segment 87
      WHEN (subscription_start < first_day) 
        AND segment = 87
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_87,
      CASE -- segment 30
        WHEN (subscription_start < first_day) 
          AND segment = 30
          AND (subscription_end > first_day
            OR subscription_end IS NULL) THEN 1
          ELSE 0
      END AS is_active_30
  FROM cross_join
)
------------------------- Query
SELECT *
FROM status
LIMIT 10;

----------------------------------------------------------------------
--6. Add an is_canceled_87 and an is_canceled_30 column to the status
----------------------------------------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
------------------------- Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    -- Checking if the customer's subscription is active during each individual months  
    CASE -- segment 87 active
      WHEN (subscription_start < first_day) 
        AND segment = 87
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_87,
      CASE -- segment 30 active
        WHEN (subscription_start < first_day) 
          AND segment = 30
          AND (subscription_end > first_day
            OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_30,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE -- segment 87 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 87 THEN 1
        ELSE 0
      END AS is_canceled_87,
      CASE -- segment 30 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 30 THEN 1
        ELSE 0
      END AS is_canceled_30 
  FROM cross_join
)
------------------------- Query
SELECT *
FROM status
LIMIT 10;

------------------------------------------------------------------------------
--7. Create a status_aggregate temporary table 
--   that is a SUM of the active and canceled subscriptions for each segment, 
--   for each month.
------------------------------------------------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  cross_join table
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  status table
status AS (
  SELECT 
    id, 
    first_day AS month,
    -- Checking if the customer's subscription is active during each individual months  
    CASE -- segment 87 active
      WHEN (subscription_start < first_day) 
        AND segment = 87
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_87,
      CASE -- segment 30 active
        WHEN (subscription_start < first_day) 
          AND segment = 30
          AND (subscription_end > first_day
            OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_30,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE -- segment 87 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 87 THEN 1
        ELSE 0
      END AS is_canceled_87,
      CASE -- segment 30 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 30 THEN 1
        ELSE 0
      END AS is_canceled_30 
  FROM cross_join
),
-------------------------  status_aggregate table
status_aggregate AS (
  SELECT
      month,
      SUM(is_active_87) AS sum_active_87,
      SUM(is_active_30) AS sum_active_30,
      SUM(is_canceled_87) AS sum_canceled_87,
      SUM(is_canceled_30) AS sum_canceled_30
  FROM status
  GROUP BY month
)
------------------------- Query
SELECT *
FROM status_aggregate;

---------------------------------------------------------------------------------
--8.  Calculate the churn rates for the two segments over the three month period
---------------------------------------------------------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    -- Checking if the customer's subscription is active during each individual months  
    CASE -- segment 87 active
      WHEN (subscription_start < first_day) 
        AND segment = 87
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_87,
      CASE -- segment 30 active
        WHEN (subscription_start < first_day) 
          AND segment = 30
          AND (subscription_end > first_day
            OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_30,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE -- segment 87 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 87 THEN 1
        ELSE 0
      END AS is_canceled_87,
      CASE -- segment 30 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 30 THEN 1
        ELSE 0
      END AS is_canceled_30 
  FROM cross_join
),
-------------------------  status_aggregate table
status_aggregate AS (
  SELECT
      month,
      SUM(is_active_87) AS sum_active_87,
      SUM(is_active_30) AS sum_active_30,
      SUM(is_canceled_87) AS sum_canceled_87,
      SUM(is_canceled_30) AS sum_canceled_30
  FROM status
  GROUP BY month
)
-------------------------  Churn rates
SELECT 
  month,
  ROUND(1.0 * sum_canceled_87 / sum_active_87, 2) AS churn_rate_87,
  ROUND(1.0 * sum_canceled_30 / sum_active_30, 2) AS churn_rate_30
FROM status_aggregate;

    -----------------------------------------
    -- Which segment has a lower churn rate?
    -----------------------------------------
  
WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
------------------------- Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    -- Checking if the customer's subscription is active during each individual months  
    CASE -- segment 87 active
      WHEN (subscription_start < first_day) 
        AND segment = 87
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_87,
      CASE -- segment 30 active
        WHEN (subscription_start < first_day) 
          AND segment = 30
          AND (subscription_end > first_day
            OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active_30,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE -- segment 87 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 87 THEN 1
        ELSE 0
      END AS is_canceled_87,
      CASE -- segment 30 canceled
        WHEN (subscription_end BETWEEN first_day AND last_day) 
          AND segment = 30 THEN 1
        ELSE 0
      END AS is_canceled_30 
  FROM cross_join
),
-------------------------  status_aggregate table
status_aggregate AS (
  SELECT
      SUM(is_active_87) AS sum_active_87,
      SUM(is_active_30) AS sum_active_30,
      SUM(is_canceled_87) AS sum_canceled_87,
      SUM(is_canceled_30) AS sum_canceled_30
  FROM status 
)
-------------------------  Churn rates
SELECT
  ROUND(1.0 * sum_canceled_87 / sum_active_87, 2) AS overall_churn_rate_87,
  ROUND(1.0 * sum_canceled_30 / sum_active_30, 2) AS overall_churn_rate_30
FROM status_aggregate;

/*--------*
 * Bonus  *
 *--------*/

---------------------------------------------------------------------------
--9. How would you modify this code to support a large number of segments?
---------------------------------------------------------------------------

    ----------------------------------
    -- Step-1 modify the status table
    ----------------------------------
  
WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    segment,
    -- Checking if the customer's subscription is active during each individual months  
    CASE 
      WHEN (subscription_start < first_day) 
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE 
        WHEN (subscription_end BETWEEN first_day AND last_day) THEN 1
        ELSE 0
      END AS is_canceled   
  FROM cross_join
  GROUP BY id, segment, first_day
)
------------------------- Query
SELECT *
FROM status
LIMIT 10;

    --------------------------------------------
    -- Step-2 modify the status_aggregate table
    --------------------------------------------
    
WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    segment, -- Added 'segment'
    -- Checking if the customer's subscription is active during each individual months
   CASE
      WHEN (subscription_start < first_day) 
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE 
        WHEN (subscription_end BETWEEN first_day AND last_day) THEN 1
        ELSE 0
      END AS is_canceled   
  FROM cross_join
  GROUP BY  first_day, segment, id
),
-------------------------  status_aggregate table
status_aggregate AS (
  SELECT
      month,
      segment,
      SUM(is_active) AS sum_active,
      SUM(is_canceled) AS sum_canceled  
  FROM status 
  GROUP BY  month, segment
)
------------------------- Query
SELECT *
FROM status_aggregate;

    -------------------------------
    -- Step-3 The churn rate query
    -------------------------------

WITH months AS ( 
  SELECT 
    '2017-01-01' AS first_day, 
    '2017-01-31' AS last_day 
  UNION 
  SELECT 
    '2017-02-01' AS first_day, 
    '2017-02-28' AS last_day 
  UNION 
  SELECT 
    '2017-03-01' AS first_day, 
    '2017-03-31' AS last_day
  FROM subscriptions
),
-------------------------  Table cross_join
cross_join AS (
  SELECT *
  FROM subscriptions
  CROSS JOIN months
),
-------------------------  Table status
status AS (
  SELECT 
    id, 
    first_day AS month,
    segment,
    -- Checking if the customer's subscription is active during each individual months
   CASE 
      WHEN (subscription_start < first_day) 
        AND (subscription_end > first_day
          OR subscription_end IS NULL) THEN 1
        ELSE 0
      END AS is_active,
      -- Checking if the customer's subscription is canceled during each individual months 
      CASE 
        WHEN (subscription_end BETWEEN first_day AND last_day) THEN 1
        ELSE 0
      END AS is_canceled   
  FROM cross_join
  GROUP BY  first_day, segment, id
),
-------------------------  status_aggregate table
status_aggregate AS (
  SELECT
      month,
      segment,
      SUM(is_active) AS sum_active,
      SUM(is_canceled) AS sum_canceled  
  FROM status 
  GROUP BY  month, segment
)
-------------------------  Churn rates
SELECT 
  month,
  segment,
  ROUND(1.0 * sum_canceled / sum_active, 2) AS month_churn_rate
FROM status_aggregate
GROUP BY month, segment;
