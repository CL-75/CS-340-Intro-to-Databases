-- DML/Manipulaition Queries 
-- These queries are also within webapp.py file with their corresponding routes

-- SEARCH PAGE -- 
SELECT game_id, game_title FROM gr6_games WHERE critic_rating >= %s

--  CREATE PROFILE PAGE  --
-- New Profile 
INSERT INTO gr6_customers (fname, lname, handle, email, credit_card, zip_code, state, city, street, street_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

-- Logging in user
SELECT handle FROM gr6_customers WHERE handle = %s


--  PROFILE PAGE  --
-- Displays the user's profile and their information with options to update or delete their profile
SELECT fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number FROM gr6_customers WHERE handle = %s

-- Update Profile
SELECT customer_id FROM gr6_customers WHERE handle = %s
UPDATE gr6_customers SET fname = %s, lname = %s, handle = %s, email = %s, credit_card = %s, zip_code = %s, state = %s, city = %s, street = %s, street_number = %s WHERE customer_id = %s

-- Delete Profile
DELETE FROM gr6_customers WHERE handle = %s
-- or
DELETE FROM gr6_customers WHERE customer_id = %s


--  LIBRARY PAGE  --
-- Displaying the user's game library
SELECT customer_id FROM gr6_customers WHERE handle = %s
SELECT gr6_customers.handle, gr6_customers.customer_id, gr6_games.game_title, gr6_games.game_id FROM gr6_games \
            INNER JOIN gr6_library ON gr6_games.game_id = gr6_library.game_id \
            INNER JOIN gr6_customers ON gr6_library.customer_id = gr6_customers.customer_id  \
            WHERE gr6_customers.customer_id = %s


--  CART PAGE  --
-- Displaying user's cart of games to purchase or remove
SELECT gr6_games.game_id, gr6_games.game_title, gr6_games.sell_price, gr6_games_carts.cart_id \
            FROM gr6_games \
            JOIN gr6_games_carts ON gr6_games.game_id = gr6_games_carts.game_id \
            JOIN gr6_carts ON gr6_games_carts.cart_id = gr6_carts.cart_id \
            WHERE gr6_carts.cart_id = %s
INSERT INTO gr6_carts (customer_id) VALUES (%s)
SELECT cart_id FROM gr6_carts WHERE customer_id = %s ORDER BY cart_id DESC LIMIT 1

-- Test query to check if a game is already in the cart 
SELECT game_id FROM gr6_games_carts WHERE cart_id = %s

INSERT INTO gr6_games_carts (cart_id, game_id, item_number) VALUE (%s, %s, %s)
DELETE FROM gr6_games_carts WHERE cart_id = %s AND game_id = %s

-- Query deletes a cart if all games are removed
SELECT cart_id FROM gr6_games_carts WHERE cart_id = %s

DELETE FROM gr6_carts WHERE cart_id = %s


--  GAME PAGE  --
-- Displays various games and their information such as title, price, etc. 
SELECT customer_id FROM gr6_customers WHERE handle = %s
SELECT game_id, game_title, sell_price, discount, critic_rating, info FROM gr6_games WHERE game_id = %s



--  ORDER PAGE  --
-- Displays a user's order and also their order history --
SELECT order_number FROM gr6_orders

-- Query retrieves current user's customer_id
SELECT customer_id FROM gr6_customers WHERE handle = %s

-- Query loads all games in the users current cart
SELECT game_id FROM gr6_games_carts WHERE cart_id = %s

-- Query loads all games already in the library
SELECT game_id FROM gr6_library WHERE customer_id = %s

-- Query adds games from the user cart to his/her library
INSERT INTO gr6_library (customer_id, game_id) VALUES (%s, %s)

-- Query gathers information to calculate data for reciept
SELECT game_id, game_title, sell_price FROM gr6_games WHERE game_id = %s

-- Query records the order in the database
INSERT INTO gr6_orders (cart_id, tax, total) VALUES (%s, %s, %s)

-- Query retrieves the order_number of the purchase to print on the reciept
SELECT order_number FROM gr6_orders WHERE cart_id = %s

-- Query retrieves a customers order history to display at the bottom of the page
SELECT gr6_orders.order_number, gr6_orders.tax, gr6_orders.total FROM gr6_orders \
            JOIN gr6_carts ON gr6_orders.cart_id = gr6_carts.cart_id \
            WHERE gr6_carts.customer_id = %s


--  ADMIN PAGE  --
-- Add New game
INSERT INTO gr6_games (game_title, sell_price, discount, critic_rating, info) VALUES (%s, %s, %s, %s, %s)
SELECT game_id FROM gr6_games WHERE game_title = %s

-- Update Games
UPDATE gr6_games SET game_title = %s, sell_price = %s, discount = %s, critic_rating = %s, info = %s WHERE game_id = %s
SELECT game_id FROM gr6_games WHERE game_title = %s

-- Delete Games
DELETE FROM gr6_games WHERE game_id = %s

-- Add game to catalog
SELECT game_id, game_title, sell_price, discount, critic_rating, info FROM gr6_games

-- Update/Delete Customers
SELECT customer_id, fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number FROM gr6_customers
UPDATE gr6_customers SET fname = %s, lname = %s, email = %s, handle = %s, credit_card = %s, zip_code = %s, state = %s, city = %s, street = %s, street_number = %s WHERE customer_id = %s
DELETE FROM gr6_customers WHERE customer_id = %s

-- Delete Libraries
SELECT gr6_customers.handle, gr6_customers.customer_id, gr6_games.game_title, gr6_games.game_id FROM gr6_customers \
        JOIN gr6_library ON gr6_customers.customer_id = gr6_library.customer_id \
        JOIN gr6_games ON gr6_library.game_id = gr6_games.game_id \
        ORDER BY gr6_customers.handle, gr6_games.game_title
DELETE FROM gr6_library WHERE customer_id = %s AND game_id = %s

-- Update/Delete Orders
SELECT gr6_games_carts.cart_id, gr6_games.sell_price FROM gr6_games \
            JOIN gr6_games_carts USING (game_id) \
            LEFT JOIN gr6_orders USING (cart_id) \
            WHERE gr6_orders.order_number IS NULL
INSERT INTO gr6_orders (cart_id, tax, total) VALUES (%s, %s, %s)
DELETE FROM gr6_orders WHERE order_number = %s
