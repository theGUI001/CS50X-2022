-- Keep a log of any SQL queries you execute as you solve the mystery.

-- List all tables in dataset
.tables

-- List CREATE TABLE command used
.schema crime_scene_reports

-- Check the crime reports on July 28, 2021 in Humphrey Street
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- Check bakery logs on the day of the crime
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2021 AND hour >= 10;

-- The witnesses could be the accomplice. So, finding the names of the witnesses from the interviews table. Also, checking their interviews' transcripts.
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

-- Check plates that exit after the crime
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2021 AND hour >= 10 AND hour < 11 AND minute >= 15 AND activity = 'exit';

-- Plates
-- ! 5P2BI95 | 94KL13X | 6P58WS2 | 4328GD8 | G412CB7 | L93JTIZ | 322W7JE | 0NTHK55 | 1106N58

-- Search for owners of plates
SELECT * FROM people
WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55', '1106N58');

-- Take note of output
-- ! +--------+---------+----------------+-----------------+---------------+
-- ! |   id   |  name   |  phone_number  | passport_number | license_plate |
-- ! +--------+---------+----------------+-----------------+---------------+
-- ! | 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
-- ! | 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
-- ! | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- ! | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
-- ! | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- ! | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- ! | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- ! | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- ! | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- ! +--------+---------+----------------+-----------------+---------------+

-- Get number of bank accounts from suspects
SELECT account_number FROM bank_accounts WHERE person_id IN (SELECT id FROM people
WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55', '1106N58'));


-- See if any of suspects withdraw money after crime
SELECT atm_transactions.id, atm_transactions.account_number, atm_transactions.amount, name
FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON bank_accounts.person_id = people.id
WHERE year = 2021 AND day = 28 AND month = 7 AND transaction_type = 'withdraw'
AND atm_transactions.account_number IN (SELECT account_number FROM bank_accounts WHERE person_id IN (SELECT id FROM people
WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55', '1106N58')))
ORDER BY atm_transactions.amount DESC;

-- *+-----+----------------+--------+--------+
-- *| id  | account_number | amount |  name  |
-- *+-----+----------------+--------+--------+
-- !| 266 | 76054385       | 60     | Taylor | high withdraws (suspect)
-- !| 267 | 49610011       | 50     | Bruce  | high withdraws (suspect)
-- *| 246 | 28500762       | 48     | Luca   |
-- *| 336 | 26013199       | 35     | Diana  |
-- *| 288 | 25506511       | 20     | Iman   |
-- *+-----+----------------+--------+--------+
-- Raymond gave clues-- As leaving the bakery, they called a person and talked for less than a minute. They asked the person on the other end of the call to buy a flight ticket of the earliest flight on July 29, 2021.

-- Search suspects in flights
SELECT passengers.flight_id, passengers.passport_number, passengers.seat, people.name, flights.year, flights.month, flights.day FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day >= 28
AND passengers.passport_number IN (SELECT passport_number FROM people
WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55', '1106N58'));

 -- * +-----------+-----------------+------+---------+------+-------+-----+
 -- * | flight_id | passport_number | seat |  name   | year | month | day |
 -- * +-----------+-----------------+------+---------+------+-------+-----+
 -- * | 2         | 2963008352      | 6C   | Vanessa | 2021 | 7     | 30  |
 -- * | 11        | 8496433585      | 5D   | Luca    | 2021 | 7     | 30  |
 -- * | 18        | 3592750733      | 4C   | Diana   | 2021 | 7     | 29  |
 -- * | 20        | 2963008352      | 6B   | Vanessa | 2021 | 7     | 28  |
 -- * | 24        | 3592750733      | 2C   | Diana   | 2021 | 7     | 30  |
 -- * | 36        | 1695452385      | 3B   | Sofia   | 2021 | 7     | 29  |
 -- ! | 36        | 5773159633      | 4A   | Bruce   | 2021 | 7     | 29  | same flight? weird
 -- * | 36        | 8294398571      | 6C   | Kelsey  | 2021 | 7     | 29  |
 -- ! | 36        | 1988161715      | 6D   | Taylor  | 2021 | 7     | 29  | same flight? weird
 -- * | 36        | 8496433585      | 7B   | Luca    | 2021 | 7     | 29  |
 -- * | 48        | 8496433585      | 7C   | Luca    | 2021 | 7     | 30  |
 -- * | 54        | 3592750733      | 6C   | Diana   | 2021 | 7     | 30  |
 -- * +-----------+-----------------+------+---------+------+-------+-----+

SELECT * FROM flights WHERE id = 36;

-- * +----+-------------------+------------------------+------+-------+-----+------+--------+
-- * | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
-- * +----+-------------------+------------------------+------+-------+-----+------+--------+
-- * | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     |
-- * +----+-------------------+------------------------+------+-------+-----+------+--------+

SELECT * FROM airports WHERE id IN (4,8);

-- * +----+--------------+-----------------------------+---------------+
-- * | id | abbreviation |          full_name          |     city      |
-- * +----+--------------+-----------------------------+---------------+
-- ! | 4  | LGA          | LaGuardia Airport           | New York City |
-- ! | 8  | CSF          | Fiftyville Regional Airport | Fiftyville    |
-- * +----+--------------+-----------------------------+---------------+

-- Check call records

-- Searching for calers
SELECT name, phone_calls.duration FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60 ORDER BY phone_calls.duration;

--* +---------+----------+
--* |  name   | duration |
--* +---------+----------+
--* | Kelsey  | 36       |
--* | Carina  | 38       |
--* | Taylor  | 43       |
--! | Bruce   | 45       |
--* | Diana   | 49       |
--* | Kelsey  | 50       |
--* | Sofia   | 51       |
--* | Benista | 54       |
--* | Kenny   | 55       |
--* | Kathryn | 60       |
--* +---------+----------+

-- Searching for receivers
SELECT name, phone_calls.duration FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60 ORDER BY phone_calls.duration;

-- *+------------+----------+
-- *|    name    | duration |
-- *+------------+----------+
-- *| Larry      | 36       |
-- *| Jacqueline | 38       |
-- *| James      | 43       |
-- ! | Robin      | 45       |
-- *| Philip     | 49       |
-- *| Melissa    | 50       |
-- *| Jack       | 51       |
-- *| Anna       | 54       |
-- *| Doris      | 55       |
-- *| Luca       | 60       |
-- *+------------+----------+

-- ! Bruce is the thief and he run away for New York and Robin must be the accomplience because Bruce called him