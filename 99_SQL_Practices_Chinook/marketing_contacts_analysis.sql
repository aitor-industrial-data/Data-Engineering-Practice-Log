/*
================================================================================
File: marketing_contacts_analysis.sql
Role: Data Analyst - Snowflake Marketing Analytics
Objective: Identify contact email addresses that satisfy two specific conditions:
           1. Had a marketing touch for three or more consecutive weeks.
           2. Had at least one marketing touch of type 'trial_request'.

--------------------------------------------------------------------------------
TABLE SCHEMAS & EXAMPLES:

1. marketing_touches
--------------------------------------------------------------------------------
Column Name  | Type    | Notes
-------------+---------+--------------------------------------------------------
event_id     | integer | Unique identifier for the event
contact_id   | integer | Foreign key referencing crm_contacts
event_type   | string  | e.g., 'webinar', 'conference_registration', 'trial_request'
event_date   | date    | Date of interaction (MM/DD/YYYY)

Example Input:
+----------+------------+-------------------------+------------+
| event_id | contact_id | event_type              | event_date |
+----------+------------+-------------------------+------------+
| 1        | 1          | webinar                 | 4/17/2022  |
| 2        | 1          | trial_request           | 4/23/2022  |
| 3        | 1          | whitepaper_download     | 4/30/2022  |
| 4        | 2          | handson_lab             | 4/19/2022  |
| 5        | 2          | trial_request           | 4/23/2022  |
| 6        | 2          | conference_registration | 4/24/2022  |
| 7        | 3          | whitepaper_download     | 4/30/2022  |
| 8        | 4          | trial_request           | 4/30/2022  |
| 9        | 4          | webinar                 | 5/14/2022  |
+----------+------------+-------------------------+------------+

2. crm_contacts
--------------------------------------------------------------------------------
Column Name  | Type    | Notes
-------------+---------+--------------------------------------------------------
contact_id   | integer | Primary key
email        | string  | Contact email address

Example Input:
+------------+--------------------------+
| contact_id | email                    |
+------------+--------------------------+
| 1          | andy.markus@att.net      |
| 2          | rajan.bhatt@capitalone.com |
| 3          | lissa_rogers@jetblue.com |
| 4          | kevinliu@square.com      |
+------------+--------------------------+

--------------------------------------------------------------------------------
EXPECTED OUTPUT FORMAT:
+--------------------+
| email              |
+--------------------+
| andy.markus@att.net|
+--------------------+
================================================================================
*/

WITH trial_request_contact AS (
    SELECT DISTINCT contact_id
    FROM marketing_touches
    WHERE event_type = 'trial_request'
),

distinct_weeks AS (
    -- Desduplicamos para tener 1 fila por contacto/semana/año
    SELECT DISTINCT
        contact_id,
        EXTRACT(YEAR FROM event_date) AS year_number,
        EXTRACT(WEEK FROM event_date) AS week_number
    FROM marketing_touches
),

week_contact AS (
    SELECT 
        contact_id,
        week_number,
        LAG(week_number, 1) OVER (
            PARTITION BY contact_id, year_number 
            ORDER BY week_number
        ) AS prev_week,
        LAG(week_number, 2) OVER (
            PARTITION BY contact_id, year_number 
            ORDER BY week_number
        ) AS prev_prev_week
    FROM distinct_weeks
)

SELECT DISTINCT
    c.email
FROM week_contact w
INNER JOIN trial_request_contact t ON w.contact_id = t.contact_id
INNER JOIN crm_contacts c ON w.contact_id = c.contact_id
WHERE w.prev_week = w.week_number - 1 
  AND w.prev_prev_week = w.week_number - 2;