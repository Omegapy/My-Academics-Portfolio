

/*-------------------------------------------------------------------------*
 *																		                                     *
 *  Codecademy Data Science course SQL                                     *
 *  Analyze Real Data with SQL section                                     *
 *  Attribution Queries with CoolTShirts                                   *
 *                                                                         *
 *-------------------------------------------------------------------------*/
 
 
  /*-----------------------------*
   * Get familiar with the data  *
   *-----------------------------*/
                                                    
-----------------------------------------------------------
-- 1. How many campaigns and sources does CoolTShirts use? 
-----------------------------------------------------------

SELECT DISTINCT utm_campaign 
FROM page_visits;

SELECT DISTINCT utm_source 
FROM page_visits;
 
    -------------------------------------------
    -- Which source is used for each campaign?
    ------------------------------------------

SELECT 
    DISTINCT utm_source,
    utm_campaign
FROM page_visits
ORDER BY 1;
                                                    
                            /************************************/
                                                    
-------------------------------------------------
-- 2. What pages are on the CoolTShirts website? 
-------------------------------------------------

SELECT DISTINCT page_name
FROM page_visits;
                                                    
                            /************************************/
                                                    
    /*----------------------------*
     * What is the user journey?  *
     *----------------------------*/
 
--------------------------------------------------------------
-- 3. How many first touches is each campaign responsible for? 
--------------------------------------------------------------

--------------------------------- first_touch table
WITH first_touch AS ( 
    SELECT 
        user_id,
        MIN(timestamp) AS first_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- ft.attr table
ft_attr AS (
  SELECT 
      ft.user_id,
      ft.first_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
      ON ft.user_id = pv.user_id
      AND ft.first_touch_at = pv.timestamp
)
--------------------------------- query
SELECT 
    utm_campaign,
    utm_source,
    COUNT(*) AS number_of_first_touches
FROM ft_attr
GROUP BY 1, 2
ORDER BY 3 DESC;
                                                    
                            /************************************/
                                                    
--------------------------------------------------------------
-- 4. How many last touches is each campaign responsible for?
--------------------------------------------------------------

--------------------------------- last_touch table
WITH last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt.attr table
lt_attr AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
)
--------------------------------- query
SELECT 
    utm_campaign,
    utm_source,
    COUNT(*) AS number_of_last_touches
FROM lt_attr
GROUP BY 1, 2
ORDER BY 3 DESC;
                                                    
                         /************************************/
                                                    
-----------------------------------------
-- 5. How many visitors make a purchase?
-----------------------------------------

SELECT COUNT(DISTINCT  user_id) AS number_of_purchases
FROM page_visits
WHERE page_name = '4 - purchase';
                                                    
                          /************************************/
                                                    
--------------------------------------------------
-- 6. Number of last touches on the purchase page 
--    is each campaign responsible for?
--------------------------------------------------

--------------------------------- last_touch table
WITH last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt_attr_purchases table
lt_attr_purchases AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
  WHERE pv.page_name = '4 - purchase' 
)
--------------------------------- query
SELECT 
    utm_campaign,
    COUNT(*) AS number_of_last_touch_purchases
FROM lt_attr_purchases
GROUP BY 1
ORDER BY 2 DESC;
                                                    
                            /************************************/
                                                     
-------------------------------------------------------
-- 7. Five campaigns with the most last touch purchase
------------------------------------------------------

    -----------------------------------------------
    -- 7.4 User that made a purchase journey 
    --     from first touch campaign attribution
    --     to last touch attribution 
    -----------------------------------------------
  
--------------------------------- first_touch table
WITH first_touch AS ( 
    SELECT 
        user_id,
        MIN(timestamp) AS first_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- ft.attr table
ft_attr AS (
  SELECT 
      ft.user_id,
      ft.first_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
      ON ft.user_id = pv.user_id
      AND ft.first_touch_at = pv.timestamp
),
--------------------------------- last_touch table
last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt_attr_purchases table
lt_attr_purchases AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
		  pv.utm_source,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
  WHERE pv.page_name = '4 - purchase' 
),
--------------------------------- ft_attr_purchases table
ft_attr_purchases AS (
  SELECT 
      lap.user_id,
      fa.first_touch_at AS first_touch,
      lap.last_touch_at AS purchase_date,
      fa.utm_source AS ft_source,
		  lap.utm_source AS ltp_source,
      fa.utm_campaign AS ft_campaign,
		  lap.utm_campaign AS ltp_campaign   
  FROM lt_attr_purchases lap
  JOIN ft_attr fa
      ON lap.user_id = fa.user_id
)
--------------------------------- query
SELECT *
FROM ft_attr_purchases
ORDER BY 2
LIMIT 10;
                                                  
                                                    
                            /************************************/
                                                    
    ---------------------------------------------------
    -- 7.5 Purchase numbers for first touch campaigns
    ---------------------------------------------------

--------------------------------- first_touch table
WITH first_touch AS ( 
    SELECT 
        user_id,
        MIN(timestamp) AS first_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- ft.attr table
ft_attr AS (
  SELECT 
      ft.user_id,
      ft.first_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
      ON ft.user_id = pv.user_id
      AND ft.first_touch_at = pv.timestamp
),
--------------------------------- last touch table
last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt_attr_purchases table
lt_attr_purchases AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
		  pv.utm_source,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
  WHERE pv.page_name = '4 - purchase' 
),
--------------------------------- ft_attr_purchases table
ft_attr_purchases AS (
  SELECT 
      lap.user_id,
      fa.first_touch_at AS first_touch,
      lap.last_touch_at AS purchase_date,
      fa.utm_source AS ft_source,
		  lap.utm_source AS ltp_source,
      fa.utm_campaign AS ft_campaign,
		  lap.utm_campaign AS ltp_campaign   
  FROM lt_attr_purchases lap
  JOIN ft_attr fa
      ON lap.user_id = fa.user_id
)
--------------------------------- query
SELECT 
    ft_campaign AS 'First Touch Campaign',
    ft_source AS 'First Touch Campaign''s Source',
    COUNT (*) AS 'Number of First Touch Resulting in a Purchase',
    COUNT(DISTINCT CASE
              WHEN ft_campaign = ltp_campaign
                THEN user_id
          END) AS 'Number of First-Last Touch resulting in a Purchase'
FROM ft_attr_purchases
GROUP BY ft_campaign
ORDER BY 3 DESC;

                                                 
                            /************************************/
                                                    
    -------------------------------------------------
    -- 7.6 Purchase numbers for last touch campaigns
    --------------------------------------------------

--------------------------------- first_touch table
WITH first_touch AS ( 
    SELECT 
        user_id,
        MIN(timestamp) AS first_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- ft.attr table
ft_attr AS (
  SELECT 
      ft.user_id,
      ft.first_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
      ON ft.user_id = pv.user_id
      AND ft.first_touch_at = pv.timestamp
),
--------------------------------- last touch table
last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt_attr_purchases table
lt_attr_purchases AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
		  pv.utm_source,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
  WHERE pv.page_name = '4 - purchase' 
),
--------------------------------- ft_attr_purchases table
ft_attr_purchases AS (
  SELECT 
      lap.user_id,
      fa.first_touch_at AS first_touch,
      lap.last_touch_at AS purchase_date,
      fa.utm_source AS ft_source,
		  lap.utm_source AS ltp_source,
      fa.utm_campaign AS ft_campaign,
		  lap.utm_campaign AS ltp_campaign   
  FROM lt_attr_purchases lap
  JOIN ft_attr fa
      ON lap.user_id = fa.user_id
),
--------------------------------- retargeting_campaign_table
retargeting_campaign_table AS (
  SELECT 
        user_id,
      CASE 
          WHEN ltp_campaign = 'weekly-newsletter' THEN ltp_campaign
          WHEN ltp_campaign = 'retargetting-ad' THEN ltp_campaign
          WHEN ltp_campaign = 'retargetting-campaign' THEN ltp_campaign
          WHEN ltp_campaign = 'paid-search' THEN ltp_campaign
      END AS retargeting_campaign,
      CASE 
          WHEN ltp_campaign = 'weekly-newsletter' THEN ltp_source
          WHEN ltp_campaign = 'retargetting-ad' THEN ltp_source
          WHEN ltp_campaign = 'retargetting-campaign' THEN ltp_source
          WHEN ltp_campaign = 'paid-search' THEN ltp_source
      END AS retargeting_campaign_source
  FROM ft_attr_purchases
  WHERE retargeting_campaign IS NOT NULL
)
--------------------------------- Query
SELECT 
   retargeting_campaign AS 'Retargeting Campaign',
   retargeting_campaign_source AS 'Retargeting Campaign''s Source',
   COUNT(*) AS 'Number of purchases'
FROM retargeting_campaign_table
GROUP BY retargeting_campaign
ORDER BY 3 DESC;

                                                 
                            /************************************/
                                                    
    -------------------------------------------------------
    -- 7.7 Numbers of purchases out come for each campaign
    -------------------------------------------------------

--------------------------------- first_touch table
WITH first_touch AS ( 
    SELECT 
        user_id,
        MIN(timestamp) AS first_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- ft.attr table
ft_attr AS (
  SELECT 
      ft.user_id,
      ft.first_touch_at,
      pv.utm_source,
		  pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
      ON ft.user_id = pv.user_id
      AND ft.first_touch_at = pv.timestamp
),
--------------------------------- last touch table
last_touch AS ( 
    SELECT 
        user_id,
        MAX(timestamp) AS last_touch_at
    FROM page_visits
    GROUP BY user_id
),
--------------------------------- lt_attr_purchases table
lt_attr_purchases AS (
  SELECT 
      lt.user_id,
      lt.last_touch_at,
		  pv.utm_source,
		  pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
      ON lt.user_id = pv.user_id
      AND lt.last_touch_at = pv.timestamp
  WHERE pv.page_name = '4 - purchase' 
),
--------------------------------- ft_attr_purchases table
ft_attr_purchases AS (
  SELECT 
      lap.user_id,
      fa.first_touch_at AS first_touch,
      lap.last_touch_at AS purchase_date,
      fa.utm_source AS ft_source,
		  lap.utm_source AS ltp_source,
      fa.utm_campaign AS ft_campaign,
		  lap.utm_campaign AS ltp_campaign   
  FROM lt_attr_purchases lap
  JOIN ft_attr fa
      ON lap.user_id = fa.user_id
),
--------------------------------- retargeting_campaign_table
retargeting_campaign_table AS (
  SELECT 
        user_id,
      CASE 
          WHEN ltp_campaign = 'weekly-newsletter' THEN ltp_campaign
          WHEN ltp_campaign = 'retargetting-ad' THEN ltp_campaign
          WHEN ltp_campaign = 'retargetting-campaign' THEN ltp_campaign
          WHEN ltp_campaign = 'paid-search' THEN ltp_campaign
      END AS retargeting_campaign,
      CASE 
          WHEN ltp_campaign = 'weekly-newsletter' THEN ltp_source
          WHEN ltp_campaign = 'retargetting-ad' THEN ltp_source
          WHEN ltp_campaign = 'retargetting-campaign' THEN ltp_source
          WHEN ltp_campaign = 'paid-search' THEN ltp_source
      END AS retargeting_campaign_source
  FROM ft_attr_purchases
  WHERE retargeting_campaign IS NOT NULL
),
--------------------------------- ft_campaign_purchases table
ft_campaign_purchases AS (
  SELECT 
      user_id,
      ft_campaign,
      ft_source
  FROM ft_attr_purchases
),
--------------------------------- retargeting_campaign_purchases table
retargeting_campaign_purchases AS (
  SELECT 
     user_id,
     retargeting_campaign,
     retargeting_campaign_source
  FROM retargeting_campaign_table
),
--------------------------------- campaign_purchases table
campaign_purchases AS (
  SELECT 
      user_id,
      ft_campaign AS campaign,
      ft_source AS source
  FROM ft_attr_purchases
  UNION
  SELECT
      user_id,
      retargeting_campaign AS campaign,
      retargeting_campaign_source AS source
  FROM retargeting_campaign_purchases
),
--------------------------------- campaign_purchase_type table    
campaign_purchase_type as (
  SELECT 
      user_id,
      campaign,
      source,
      CASE 
        WHEN campaign = 'weekly-newsletter' THEN 'retargeting'
        WHEN campaign = 'retargetting-ad' THEN 'retargeting'
        WHEN campaign = 'retargetting-campaign' THEN 'retargeting'
        WHEN campaign = 'paid-search' THEN 'retargeting'
        ELSE 'first touch'
      END AS campaign_type
  FROM campaign_purchases
)
--------------------------------- query  
campaign_purchase_type as (
SELECT
    campaign,
    source,
    campaign_type,
    COUNT(*) AS 'Number of Purchases'
FROM campaign_purchase_type
GROUP BY 1
ORDER BY 4 DESC;
