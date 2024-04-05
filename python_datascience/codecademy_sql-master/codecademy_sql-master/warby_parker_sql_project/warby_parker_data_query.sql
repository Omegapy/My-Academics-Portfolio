
/*-------------------------------------------------------------------------*
 *																		   *
 *  Codecademy Data Science course SQL Analyze real Data with SQL section  *
 *  Usage Funnels with Warby Parker                                        *
 *                                                                         *
 *-------------------------------------------------------------------------*/

--1. survey Table

SELECT *
FROM survey
LIMIT 10;

--2. What is the number of responses for each question?

SELECT question, 
       COUNT(DISTINCT user_id) AS 'responses'
FROM survey
GROUP BY 1;

--4. Which question(s) of the quiz have a lower completion rates?

  -- Tables quiz, home_try_on and purshase
  
SELECT *
FROM quiz
LIMIT 5;

SELECT *
FROM home_try_on
LIMIT 5;

SELECT *
FROM purchase
LIMIT 5;

  -- Numbers of 5 and 3 pairs try-on

SELECT 
    -- Number of customers that received 5 pairs try-on
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '5 pairs' THEN user_id
          END) AS 'number_of_5_pairs_try_on',
    -- Number of customers that received 3 pairs try-on     
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '3 pairs' THEN user_id
          END) AS 'number_of_3_pairs_try_on',
    -- Total number of customers that received pairs try-on      
    COUNT (*) AS 'total_number_of_pairs_try_on'
FROM home_try_on;

  -- Percentages of of 5 and 3 pairs try-on

WITH pairs_users_totals AS (
    SELECT 
      -- Number of customers that received 5 pairs try-on
      COUNT(DISTINCT CASE
              WHEN  number_of_pairs = '5 pairs' THEN user_id
            END) AS 'number_of_5_pairs_try_on',
      -- Number of customers that received 3 pairs try-on
      COUNT(DISTINCT CASE
              WHEN  number_of_pairs = '3 pairs' THEN user_id
            END) AS 'number_of_3_pairs_try_on',
      -- Total number of customers that received pairs try-on
      COUNT (*) AS 'total_number_of_pairs_try_on'
    FROM home_try_on)
-- Decimal percentages computations  
SELECT ROUND(1.0 * number_of_5_pairs_try_on * 100 / total_number_of_pairs_try_on, 2) AS '%_of_users_that_got_5_pairs',
       ROUND(1.0 * number_of_3_pairs_try_on * 100 / total_number_of_pairs_try_on, 2) AS '%_users_that_got_3_pairs'
FROM pairs_users_totals;

--5. Use a LEFT JOIN to combine quize, home_try_on and purchase tables

SELECT DISTINCT q.user_id,
    -- try-on true or false
    CASE
      WHEN h.user_id IS NOT NULL THEN 'True'
      ELSE 'False'
    END AS 'is_home_try_on',
    -- 5 pairs, 3 pairs or NULL
    CASE 
      WHEN h.number_of_pairs = '5 pairs' THEN '5'
      WHEN h.number_of_pairs = '3 pairs' THEN '3'
      ELSE 'NULL'
    END AS 'number_of_pairs',
    -- purchase true or false
    CASE
      WHEN p.user_id IS NOT NULL THEN 'True'
      ELSE 'False'
    END AS 'is_purchase'
FROM quiz q
LEFT JOIN home_try_on h
  ON q.user_id = h.user_id
LEFT JOIN purchase p
  ON p.user_id = q.user_id
LIMIT 10;

--6. Analize data

  -- Code query ouput use to aggregat the columns.
        /* The following code ouput allows to simplify the aggregat code query by using the sum() aggregate function, see ouput query result for the code */

SELECT DISTINCT q.user_id,
   h.user_id IS NOT NULL AS 'is_home_try_on', -- will output a 1 if not NULL or a 0 if NULL
   h.number_of_pairs, -- will output the symbol ? if no "5 pairs" or "3 pairs" input, see Query Results
   p.user_id IS NOT NULL AS 'is_purchase'-- will output a 1 if not NULL or a 0 if NULL
FROM quiz q
LEFT JOIN home_try_on h
   ON q.user_id = h.user_id
LEFT JOIN purchase p
   ON p.user_id = q.user_id
LIMIT 10;

 -- Numbers query of the Warby Parker’s purchase funnel
 
WITH funnel AS (  
   SELECT DISTINCT q.user_id,
       h.user_id IS NOT NULL AS 'is_home_try_on',
       h.number_of_pairs,
       p.user_id IS NOT NULL AS 'is_purchase'
FROM quiz q
LEFT JOIN home_try_on h
   ON q.user_id = h.user_id
LEFT JOIN purchase p
   ON p.user_id = q.user_id)     
SELECT COUNT(*) AS 'number_of_quiz',
    SUM(is_home_try_on) AS 'total_number_of_pairs_try_on',  
    -- Total purchases
    SUM(is_purchase) AS 'number_of_purchases',
    -- Number of 5 pairs try-on
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '5 pairs' THEN user_id
          END) AS 'number_of_5_pairs_try_on',
     -- Number of 3 pairs try-on
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '3 pairs' THEN user_id
          END) AS 'number_of_3_pairs_try_on',   
    -- Nummber of purchase with 5 pairs try-on
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '5 pairs' AND  is_purchase = 1 THEN user_id
          END) AS 'number_of_purchases_with_5_pairs_try_on',
    -- Nummber of purchase with 3 pairs try-on
    COUNT(DISTINCT CASE
            WHEN  number_of_pairs = '3 pairs' AND  is_purchase = 1 THEN user_id
          END) AS 'number_of_purchases_with_3_pairs_try_on'
FROM funnel;

  -- Funnel conversion rate from  quiz -> Home Try-on -> purchace

WITH funnel AS (
   SELECT DISTINCT q.user_id,
       h.user_id IS NOT NULL AS 'is_home_try_on',
       h.number_of_pairs,
       p.user_id IS NOT NULL AS 'is_purchase'
FROM quiz q
LEFT JOIN home_try_on h
   ON q.user_id = h.user_id
LEFT JOIN purchase p
   ON p.user_id = q.user_id)     
SELECT COUNT(*) AS 'number_of_quiz',
    -- Conversion rate in percentages of quiz to home try-on and home try-on to purchase
    -- Multiplying by 1.0 will output a decimal number 
    ROUND(1.0 * SUM(is_home_try_on) * 100 / COUNT(*), 2) AS '%_quiz_to_home_try_on',
    ROUND(1.0 * SUM(is_purchase) * 100 / SUM(is_home_try_on), 2) AS '%_home_try_on_to_purchase',
    -- Conversion rate in percentages of 5 pairs try-on to purchase
    ROUND(1.0 * COUNT(DISTINCT CASE -- Number of purchase by customers that got 5 pairs
                          WHEN  number_of_pairs = '5 pairs' AND  is_purchase = 1 THEN user_id
                      END) * 100 / COUNT(DISTINCT CASE -- Number of customers that got 5 pairs
                                           WHEN  number_of_pairs = '5 pairs' THEN user_id
                                          END), 2) AS '%_5_pairs_try_on_to_purchase',
      -- Conversion rate in percentages of 3 pairs try-on to purchase           
     ROUND(1.0 * COUNT(DISTINCT CASE -- Number of purchase by customers that got 3 pairs
                          WHEN  number_of_pairs = '3 pairs' AND  is_purchase = 1 THEN user_id
                        END) * 100 / COUNT(DISTINCT CASE -- Number of customers that got 3 pairs
                                            WHEN  number_of_pairs = '3 pairs' THEN user_id
                                          END), 2) AS '%_3_pairs_try_on_to_purchase'                           
FROM funnel; 

  -- Funnel conversion rate from  quiz -> purchase , quiz -> purchase 5 pairs try-on , quiz -> purchase 3 pairs try-on

WITH funnel AS (
   SELECT DISTINCT q.user_id,
       h.user_id IS NOT NULL AS 'is_home_try_on',
       h.number_of_pairs,
       p.user_id IS NOT NULL AS 'is_purchase'
FROM quiz q
LEFT JOIN home_try_on h
   ON q.user_id = h.user_id
LEFT JOIN purchase p
   ON p.user_id = q.user_id)     
SELECT COUNT(*) AS 'number_of_quiz',
     -- Conversion rate in percentages of quiz to purchase
     -- Multiplying by 1.0 will output a decimal number 
    ROUND(1.0 * SUM(is_purchase) * 100 / COUNT(*), 2) AS '%_quiz_to_purchase',
    -- Conversion rate in percentages of quiz to purchase for customers that got 5 pairs try-on 
    ROUND(1.0 * COUNT(DISTINCT CASE -- Number of purchase by customers that got 5 pairs
                          WHEN  number_of_pairs = '5 pairs' AND  is_purchase = 1 THEN user_id
                      END)  * 100 / (COUNT(*) / (100 / ROUND(1.0 * COUNT(DISTINCT CASE -- Number of customers that got 5 pairs
                                                                              WHEN  number_of_pairs = '5 pairs' THEN user_id
                                                                          END) * 100 / SUM(is_home_try_on), 2))), 2) AS '%_quiz_to_purchase_5_pairs_try_on',    
    -- Conversion rate in percentages of quiz to purchase for customers that got 3 pairs try-on                   
    ROUND(1.0 * COUNT(DISTINCT CASE -- Number of purchase by customers that got 5 pairs
                          WHEN  number_of_pairs = '3 pairs' AND  is_purchase = 1 THEN user_id
                      END)  * 100 / (COUNT(*) / (100 / ROUND(1.0 * COUNT(DISTINCT CASE -- Number of customers that got 3 pairs
                                                                              WHEN  number_of_pairs = '3 pairs' THEN user_id
                                                                          END) * 100 / SUM(is_home_try_on), 2))), 2) AS '%_quiz_to_purchase_3_pairs_try_on'    
FROM funnel;

  -- The most common results of the style quiz
  
SELECT COUNT(DISTINCT user_id) AS 'number_of_common_types',
    style, 
    fit, 
    shape,
    color   
FROM quiz
GROUP BY 2, 3, 4, 5
ORDER by 1 DESC
LIMIT 3;

  -- Conversion rates for common styles

WITH number_of_common_results AS (
    SELECT COUNT(DISTINCT user_id) AS 'total_number_of_quiz',
        COUNT(DISTINCT CASE -- Number of Women's styles
                    WHEN style = 'Women''s Styles' THEN user_id
              END) AS 'num_style_women',
        COUNT(DISTINCT CASE -- Number of Men's styles
                    WHEN style = 'Men''s Styles' THEN user_id
              END) AS 'num_style_men',
        COUNT(DISTINCT CASE -- Number of Men's styles Narrow Rectangular Tortoise
                    WHEN style = 'Men''s Styles' 
                      AND fit = 'Narrow' 
                      AND shape = 'Rectangular' 
                      AND color = 'Tortoise' 
                    THEN user_id
              END) AS 'num_style_men_narrow_rec_tortoise',
        COUNT(DISTINCT CASE -- Number of Women's styles Narrow Rectangular Black
                    WHEN style = 'Women''s Styles' 
                      AND fit = 'Narrow' 
                      AND shape = 'Rectangular' 
                      AND color = 'Black' 
                    THEN user_id
              END) AS 'num_style_women_narrow_rec_black',
      COUNT(DISTINCT CASE -- Number of Women's styles Narrow Rectangular Tortoise
                    WHEN style = 'Women''s Styles' 
                      AND fit = 'Narrow' 
                      AND shape = 'Rectangular' 
                      AND color = 'Tortoise' 
                      THEN user_id
            END) AS 'num_style_women_narrow_rec_tortoise' 
    FROM quiz)
SELECT total_number_of_quiz,
    -- Conversion rates in percentages
    -- Multiplying by 1.0 will output a decimal number 
    ROUND(1.0 * num_style_women * 100 / total_number_of_quiz, 2) AS '%_style_women',
    ROUND(1.0 * num_style_men * 100 / total_number_of_quiz, 2) AS '%_style_men',
    ROUND(1.0 * num_style_men_narrow_rec_tortoise * 100 / num_style_men, 2) AS '%_men_narrow_rec_tortoise',
    ROUND(1.0 * num_style_women_narrow_rec_black * 100 / num_style_women, 2) AS '%_women_narrow_rec_black',
    ROUND(1.0 * num_style_women_narrow_rec_tortoise * 100 / num_style_women, 2) AS '%_women_narrow_rec_tortoise'
FROM number_of_common_results;

  -- The most common types of purchase 

SELECT COUNT(DISTINCT user_id) AS 'number_of_purchases',
    product_id, 
    style, 
    model_name, 
    color, 
    price       
FROM purchase
GROUP BY 3, 4, 5, 6
ORDER by 1 DESC
LIMIT 2;

 -- Conversion rates for common types of purchase

WITH number_of_common_purchases AS (
    SELECT COUNT(DISTINCT user_id) AS 'total_number_of_purchase',
        COUNT(DISTINCT CASE -- Number of Women's styles purchases
                    WHEN style = 'Women''s Styles' THEN user_id
              END) AS 'num_style_women_purchases',
        COUNT(DISTINCT CASE -- Number of Men's styles purchases
                    WHEN style = 'Men''s Styles' THEN user_id
              END) AS 'num_style_men_purchases',
        COUNT(DISTINCT CASE -- Number of Men's styles Dawes Driftwood Fade purchases
                    WHEN product_id = 3 
                      AND style = 'Men''s Styles' 
                      AND model_name = 'Dawes' 
                      AND color = 'Driftwood Fade' 
                      AND price = 150 
                    THEN user_id
              END) AS 'num_men_product_id_3_purchases',
        COUNT(DISTINCT CASE -- Number of Women's styles Eugene Narrow Rosewood Tortoise purchases
                    WHEN product_id = 10 
                      AND style = 'Women''s Styles' 
                      AND model_name = 'Eugene Narrow' 
                      AND color = 'Rosewood Tortoise' 
                      AND price = 95
                    THEN user_id
              END) AS 'num_women_product_id_10_purchases'
    FROM purchase)
SELECT total_number_of_purchase,
    -- Conversion rates in percentages
    -- Multiplying by 1.0 will output a decimal number 
   ROUND(1.0 * num_style_women_purchases * 100 / total_number_of_purchase, 2) AS '%_style_women_purchases',
   ROUND(1.0 * num_style_men_purchases * 100 / total_number_of_purchase, 2) AS '%_style_men_purchases',
   ROUND(1.0 * num_men_product_id_3_purchases * 100 / num_style_men_purchases, 2) AS '%_men_product_id_3_purchases',
   ROUND(1.0 * num_women_product_id_10_purchases * 100 / num_style_women_purchases, 2) AS '%_women_product_id_10_purchases'
FROM number_of_common_purchases;
