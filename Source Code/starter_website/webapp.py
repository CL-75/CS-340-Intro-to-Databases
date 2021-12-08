# _____________________________________________________________________________
#
#   Project Group 6 CS340 - 401 Introduction to Databases
#
#   Project by Jamie Chaisson   chaissoj@oregonstate.edu
#           and Casey Levy      levyca@oregonstate.edu
#
#   Group6Games is a mockup of a Steam like game service
#______________________________________________________________________________

from flask import Flask, render_template, session, flash
from flask import request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

webapp.config['SECRET_KEY'] = 'Supersecrectkey' # needed for flash messages and session data

# function which returns all games from the gr6_games database table
def getgames():
    print("Getting Our Games")
    db_connection = connect_to_database()
    query = "SELECT game_id, game_title FROM gr6_games"
    return execute_query(db_connection, query).fetchall()

# Index Route *************************************

@webapp.route('/')
def index():
    flash('Our Featured Game')
    return redirect('/gamepage/1')

# search and filter games by thier critic rating

@webapp.route('/search', methods = ['GET', 'POST'])
def search():
    print('Search')
    if request.method == 'POST':
        critic_rating = request.form['critic_rating']
        db_connection = connect_to_database()
        query = "SELECT game_id, game_title FROM gr6_games WHERE critic_rating >= %s"
        game_list = execute_query(db_connection, query, critic_rating).fetchall()
        return render_template('search.html', game_list = game_list)
    else:
        return render_template('search.html', game_list = getgames())

# Cart Routes *************************************

@webapp.route('/cart')
def cart():
    print("Route Cart")
    if 'cart_id' in session and 'handle' in session:
        handle = session['handle']
        cart_id = session['cart_id']
        db_connection = connect_to_database()
        query = "SELECT gr6_games.game_id, gr6_games.game_title, gr6_games.sell_price, gr6_games_carts.cart_id \
            FROM gr6_games \
            JOIN gr6_games_carts ON gr6_games.game_id = gr6_games_carts.game_id \
            JOIN gr6_carts ON gr6_games_carts.cart_id = gr6_carts.cart_id \
            WHERE gr6_carts.cart_id = %s"
        cart = execute_query(db_connection, query, (cart_id,))
        total = 0
        for item in cart:
            total = total + item[2]

        return render_template('/cart.html', handle = handle, cart = cart, cart_id=cart_id, total=total, game_list = getgames())
    else:
        flash('Add a game from Our Games to create a Cart')
        return redirect("/")

# Add additional games to a cart *********************************************

@webapp.route('/append_cart', methods = ['POST'])
def append_cart():
    print("Route Append Cart")
    cart_id = request.form['cart_id']
    customer_id = request.form['customer_id']
    customer_id = customer_id
    game_id = request.form['game_id']

    db_connection = connect_to_database()
    if cart_id == 'None':
        query = "INSERT INTO gr6_carts (customer_id) VALUES (%s)"
        execute_query(db_connection, query, (customer_id,))

        query = "SELECT cart_id FROM gr6_carts WHERE customer_id = %s ORDER BY cart_id DESC LIMIT 1"
        cart_id = execute_query(db_connection, query, (customer_id,)).fetchone()
        cart_id = cart_id[0]
        session['cart_id'] = cart_id
        session['item_number'] = 0  # pop when order is complete or user logs off
    
    # Query tests if a game already exist in the cart and redirect if 
    query = "SELECT game_id FROM gr6_games_carts WHERE cart_id = %s"
    record = execute_query(db_connection, query, (cart_id,)).fetchall()

    for game in record:
        game = game[0]
        if int(game) == int(game_id):
            flash('A cart may only contain one copy of a game.')
            return redirect('/cart')

    item_number = session['item_number'] + 1
    session['item_number'] = item_number 
    data = (cart_id, int(game_id), item_number)
    query = "INSERT INTO gr6_games_carts (cart_id, game_id, item_number) VALUE (%s, %s, %s)"
    execute_query(db_connection, query, data)
    flash('Your cart has been updated')
    return redirect('/cart')

# Remove a game from a cart *********************************************

@webapp.route('/remove_from_cart', methods = ['POST'])
def appen_cart():
    print("Remove Item From Cart")
    cart_id = request.form['cart_id']
    game_id = request.form['game_id']

    # Query deletes a game from a cart.
    db_connection = connect_to_database()
    query = "DELETE FROM gr6_games_carts WHERE cart_id = %s AND game_id = %s"
    data = (cart_id, game_id)
    print(f"Data is: {data}")
    execute_query(db_connection, query, data)
    flash('Your cart has been updated.')

    # Query deletes an cart if there are no longer any games in the cart
    query = "SELECT cart_id FROM gr6_games_carts WHERE cart_id = %s"
    result = execute_query(db_connection, query, (cart_id,)).fetchall()
    if not result:
        query = "DELETE FROM gr6_carts WHERE cart_id = %s"
        execute_query(db_connection, query, (cart_id,))
        session.pop('cart_id', None)
        print("Cart Deleted!")

    return redirect('/cart')

# Order Routes *************************************************

@webapp.route('/place_order', methods= ['GET', 'POST'])
def place_order():
    print("Placing Order")
    
    if request.method == 'POST':
        handle = session['handle']
        cart_id = session['cart_id']
        db_connection = connect_to_database()

        # Query retrieves current user's customer_id
        query = "SELECT customer_id FROM gr6_customers WHERE handle = %s"
        customer_id = execute_query(db_connection, query, (handle,)).fetchone()

        # Query loads all games in the users current cart 
        query = "SELECT game_id FROM gr6_games_carts WHERE cart_id = %s"
        games = execute_query(db_connection, query, (cart_id,)).fetchall()

        # Query loads all games already in the library
        query = "SELECT game_id FROM gr6_library WHERE customer_id = %s"
        library = execute_query(db_connection, query, (customer_id,)).fetchall()

        # If a game is already in the user library, the route is redirected back to the cart.
        for game in games:
            for item in library:
                if item == game:
                    flash('You cannot have duplicate games in your library')
                    return redirect('/cart')

        # Query adds games from the user cart to his/her library
        query = "INSERT INTO gr6_library (customer_id, game_id) VALUES (%s, %s)"
        for game in games:
            execute_query(db_connection, query, (customer_id, game))

        # The cart is poped from the session and the reciept is generated
        session.pop('cart_id', None)
        result = []
        subtotal = 0

        # Query gathers information to calculate data for recipt
        query = "SELECT game_id, game_title, sell_price FROM gr6_games WHERE game_id = %s"
        for game in games:
            data = execute_query(db_connection, query, game).fetchone()
            result.append(data)
            subtotal = subtotal + data[2]
        subtotal = float(subtotal)
        tax = round(float(subtotal * .095))
        total = round(subtotal + tax, 2)
        data = (cart_id, tax, total)

        # Query records the order in the database
        query = "INSERT INTO gr6_orders (cart_id, tax, total) VALUES (%s, %s, %s)"
        execute_query(db_connection, query, data)

        #Query retrieves the order_number of the purchase to print on the reciept
        query = "SELECT order_number FROM gr6_orders WHERE cart_id = %s"
        order_number = execute_query(db_connection, query, (cart_id,)).fetchone()
        order_number = order_number[0]

        # Query retrieves a customers order history to display at the bottom of the page
        query = "SELECT gr6_orders.order_number, gr6_orders.tax, gr6_orders.total FROM gr6_orders \
            JOIN gr6_carts ON gr6_orders.cart_id = gr6_carts.cart_id \
            WHERE gr6_carts.customer_id = %s"
        order_history = execute_query(db_connection, query, customer_id).fetchall()

        return render_template('reciept.html', order_number=order_number, handle=handle, result=result, \
            subtotal=subtotal, tax=tax, total=total, order_history=order_history)
    else:
        flash('Redirected: Something has gone wrong')
        return redirect('/cart')

# Profile Route *************************************

@webapp.route('/user_profile') 
def user_profile():
    print('Profile page')
    if 'handle' in session:
        handle = session['handle']
        db_connection = connect_to_database() 
        query = 'SELECT fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number FROM gr6_customers WHERE handle = %s' 
        result = execute_query(db_connection, query, (handle,)).fetchone()
        return render_template('user_profile.html', result = result)
    else: 
        flash('Please Login')   
        return redirect('/')

# Update user profile *****************************************

@webapp.route('/update_user', methods = ['GET', 'POST'])
def update_user():
    print("Update user Profile")
    if request.method == 'POST' and 'handle' in session:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        handle = request.form['handle']
        credit_card = request.form['credit_card']
        zip_code = request.form['zip_code']
        state = request.form['state']
        city = request.form['city']
        street = request.form['street']
        street_number = request.form['street_number']

        key = session['handle']
        db_connection = connect_to_database()
        query = 'SELECT customer_id FROM gr6_customers WHERE handle = %s'
        key = execute_query(db_connection, query, (key,)).fetchone()
        data = (fname, lname, handle, email, credit_card, zip_code, state, city, street, street_number, key[0])

        query = 'UPDATE gr6_customers SET fname = %s, lname = %s, handle = %s, email = %s, credit_card = %s, zip_code = %s, state = %s, city = %s, street = %s, street_number = %s WHERE customer_id = %s;'
        execute_query(db_connection, query, data)
        session.pop('handle', None)
        session['handle'] = handle
        flash('Your file has been updated.')
        return redirect('/user_profile')
    else:
        flash('Redirected: Something has gone wrong')
        return redirect('/')

# Create Profile Route *************************************

@webapp.route('/new_user_profile', methods = ['GET', 'POST'])
def new_user_profile():
    print('Adding New User')
    session.pop('handle', None)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        handle = request.form['handle']

        session['handle'] = handle
        credit_card = request.form['credit_card']
        zip_code = request.form['zip_code']
        state = request.form['state']
        city = request.form['city']
        street = request.form['street']
        street_number = request.form['street_number']

        data = (fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number)
        db_connection = connect_to_database()
        query = 'INSERT INTO gr6_customers (fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        execute_query(db_connection, query, data)
        user = handle
        flash('Welcome to G6Games!')
        return redirect('/user_profile')
    else:
        return render_template('new_user_profile.html')

# Route Logs Customer into thier Profile ********************************************

@webapp.route('/login', methods=['POST','GET'])
def login():
    print('Logging In')
    session.pop('handle', None)
    if request.method == 'POST':
        handle = request.form['user_id']
        db_connection = connect_to_database()
        query = 'SELECT handle FROM gr6_customers WHERE handle = %s'
        result = execute_query(db_connection, query, (handle,)).fetchone()
        if result:
            session['handle'] = handle
            flash('Welcome Back!')
            return redirect('/user_profile')
        flash('Check your username or create a New User.')    
        return redirect('/')
    flash('Redirected: Something has gone wrong')
    return redirect('/')

# Route logs user out of account **************************************************

@webapp.route('/logout')
def logout():
    print('Logging Out')
    session.pop('handle', None)
    session.pop('cart_id', None)
    flash('Good-Bye!')
    return redirect('/')

# Route provides a user a means to delete thier account **************************   

@webapp.route('/delete_user', methods = ['POST'])
def delete_user():
    print('Deleting User')
    db_connection = connect_to_database()
    if 'handle' in session:
        handle = session['handle']
        query = 'DELETE FROM gr6_customers WHERE handle = %s'
        execute_query(db_connection, query, (handle,))
        session.pop('handle', None)
    else:
        customer_id = request.form['customer_id']
        query = 'DELETE FROM gr6_customers WHERE customer_id = %s'
        execute_query(db_connection, query, (customer_id,))
    flash('Sorry to see you go!')
    return redirect('/')
    
# Game Page Route *************************************

@webapp.route('/gamepage/<game_id>')
def gamepage(game_id):
    print('Game Page')
    db_connection = connect_to_database()
    if 'handle' in session:
        handle = session['handle']
        query = "SELECT customer_id FROM gr6_customers WHERE handle = %s"
        customer_id = execute_query(db_connection, query, (handle,)).fetchone()
        customer_id = customer_id[0]
    else:
        handle = None
        customer_id = None
    if 'cart_id' in session:
        cart_id = session['cart_id']
    else:
        cart_id = None

    query = "SELECT game_id, game_title, sell_price, discount, critic_rating, info FROM gr6_games WHERE game_id = %s"
    result = execute_query(db_connection, query, (game_id,)).fetchone()
    rating = int(result[4])
    return render_template('gamepage.html', \
        result = result, \
        rating = rating, \
        handle = handle, \
        customer_id = customer_id, \
        cart_id = cart_id, \
        game_list = getgames())

# Order Page Route *************************************

@webapp.route('/order_page')
def order_page():
    print('Order Page')
    db_connection = connect_to_database()
    query = "SELECT order_number FROM gr6_orders"
    result = execute_query(db_connection, query).fetchall()
    return render_template('order_page.html') #, order_number=order_number, sell_price=sell_price, total=total)

# Game Library Route *************************************

@webapp.route('/game_library')
def game_library():
    print('Game Library')
    if 'handle' in session:
        handle = session['handle']
        db_connection = connect_to_database()
        query = "SELECT customer_id FROM gr6_customers WHERE handle = %s"
        customer_id = execute_query(db_connection, query, (handle,)).fetchone()
        query = "SELECT gr6_customers.handle, gr6_customers.customer_id, gr6_games.game_title, gr6_games.game_id FROM gr6_games \
            INNER JOIN gr6_library ON gr6_games.game_id = gr6_library.game_id \
            INNER JOIN gr6_customers ON gr6_library.customer_id = gr6_customers.customer_id  \
            WHERE gr6_customers.customer_id = %s"
        library = execute_query(db_connection, query, customer_id).fetchall()
        return render_template('game_library.html', library=library, game_list = getgames())
    else:
        flash('Login to view your library!')
        return redirect('/')

# Add Game to Catalog gr6_games **************************************************

@webapp.route('/addgame', methods = ['GET', 'POST'])
def addgame():
    print('Add Game')
    game_title = request.form['game_title']
    sell_price = request.form['sell_price']
    discount = request.form['discount']
    critic_rating = request.form['critic_rating']
    info = request.form['info']
    data = (game_title, sell_price, discount, critic_rating, info)
    db_connection = connect_to_database()
    query = "INSERT INTO gr6_games (game_title, sell_price, discount, critic_rating, info) VALUES (%s, %s, %s, %s, %s)"
    execute_query(db_connection, query, data)
    query = "SELECT game_id FROM gr6_games WHERE game_title = %s"
    game_id = execute_query(db_connection, query, (game_title,)).fetchone()
    game_id = game_id[0]
    flash('Game Added')
    return redirect(f'/gamepage/{game_id}')

# Update a Game **************************************************************

@webapp.route('/updategame', methods = ['POST'])
def updategame():
    print('Updataing Game')
    game_id = request.form['game_id']
    game_title = request.form['game_title']
    sell_price = request.form['sell_price']
    discount = request.form['discount']
    critic_rating = request.form['critic_rating']
    info = request.form['info']
    data = (game_title, sell_price, discount, critic_rating, info, game_id)
    db_connection = connect_to_database()
    query = "UPDATE gr6_games SET game_title = %s, sell_price = %s, discount = %s, critic_rating = %s, info = %s WHERE game_id = %s"
    execute_query(db_connection, query, data)
    query = "SELECT game_id FROM gr6_games WHERE game_title = %s"
    game_id = execute_query(db_connection, query, (game_title,)).fetchone()
    game_id = game_id[0]
    flash('Game Updated')
    return redirect(f'gamepage/{game_id}')

# Delete a game *************************************************************

@webapp.route('/deletegame', methods = ['POST'])
def deletegame():
    print('Deleting Game')
    game_id = request.form['game_id']
    db_connection = connect_to_database()
    query = 'DELETE FROM gr6_games WHERE game_id = %s'
    execute_query(db_connection, query, (game_id,))
    flash('Game Deleted')
    return redirect('admin_page')

# Admin Page Route ************************************************************

@webapp.route('/admin_page')
def admin_page():
    print('Adimin Page')
    session.pop('handle', None)
    db_connection = connect_to_database()

    # Admin add game to catalog
    query = "SELECT game_id, game_title, sell_price, discount, critic_rating, info FROM gr6_games"
    games = execute_query(db_connection, query).fetchall()

    # Admin Update/Delete customer table
    query = "SELECT customer_id, fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number FROM gr6_customers"
    customers = execute_query(db_connection, query).fetchall()

    # Admin Delete game from library table
    query = "SELECT gr6_customers.handle, gr6_customers.customer_id, gr6_games.game_title, gr6_games.game_id FROM gr6_customers \
        JOIN gr6_library ON gr6_customers.customer_id = gr6_library.customer_id \
        JOIN gr6_games ON gr6_library.game_id = gr6_games.game_id \
        ORDER BY gr6_customers.handle, gr6_games.game_title"
    library = execute_query(db_connection, query).fetchall()

    # Admin Insert cart table
    query =  "SELECT cart_id, handle FROM gr6_carts JOIN gr6_customers ON gr6_carts.customer_id = gr6_customers.customer_id ORDER BY cart_id DESC"
    carts = execute_query(db_connection, query).fetchall()

    # Admin insert a game into a cart
    query = "SELECT gr6_carts.cart_id, gr6_customers.handle, gr6_games.game_title FROM gr6_customers \
        JOIN gr6_carts ON gr6_customers.customer_id = gr6_carts.customer_id \
        JOIN gr6_games_carts ON gr6_carts.cart_id = gr6_games_carts.cart_id \
        JOIN gr6_games ON gr6_games_carts.game_id = gr6_games.game_id ORDER BY cart_id DESC"
    games_carts = execute_query(db_connection, query).fetchall()

    # Admin turn a cart to an order.
    query = "SELECT gr6_games_carts.cart_id FROM gr6_games_carts \
        LEFT JOIN gr6_orders USING (cart_id) \
        WHERE gr6_orders.order_number IS NULL"
    tup = execute_query(db_connection, query).fetchall()
    tuporder=[]
    
    for each in tup:
        tuporder.append(each[0]) 
    order = tuple(tuporder)
    
    print(f"The Order is: {order[0]}")

    return render_template('admin_page.html', \
        games = games, customers = customers, \
        library = library, carts=carts, \
        games_carts=games_carts, order=order)

# Admin route *************************************************************************

@webapp.route('/admin_update_user', methods = ['GET', 'POST'])
def admin_update_user():
    print("Admin Update Profile")
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        handle = request.form['handle']
        credit_card = request.form['credit_card']
        zip_code = request.form['zip_code']
        state = request.form['state']
        city = request.form['city']
        street = request.form['street']
        street_number = request.form['street_number']

        db_connection = connect_to_database()    
        data = (fname, lname, email, handle, credit_card, zip_code, state, city, street, street_number, customer_id)
        query = 'UPDATE gr6_customers SET fname = %s, lname = %s, email = %s, handle = %s, credit_card = %s, zip_code = %s, state = %s, city = %s, street = %s, street_number = %s WHERE customer_id = %s'
        execute_query(db_connection, query, data)
        return redirect('/admin_page')
    else:
        flash('Redirected: Something has gone wrong')
        return redirect('/')

# Admin route **************************************************************************

@webapp.route('/admin_insert_cart', methods=['GET', 'POST'])
def admin_insert_cart():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        db_connection = connect_to_database()
        query = "INSERT INTO gr6_carts (customer_id) VALUES (%s)"
        execute_query(db_connection, query, (customer_id,))

    return redirect('/admin_page')

# Admin route ***********************************************************************

@webapp.route('/admin_orders', methods = ['GET', 'POST'])
def admin_orders():
    
    if request.method == 'POST':
        db_connection = connect_to_database()
        
        cart_id = request.form['cart_id']
        
        query = "SELECT gr6_games_carts.cart_id, gr6_games.sell_price FROM gr6_games \
            JOIN gr6_games_carts USING (game_id) \
            LEFT JOIN gr6_orders USING (cart_id) \
            WHERE gr6_orders.order_number IS NULL"
        order = execute_query(db_connection, query).fetchall()
        print(f"ORDER : {order}")
        total = 0
        for each in order:
            total = total + each[1]

        tax = round(float(total) * float(.095), 2)  
        data = (cart_id, tax, total)  
        
        query = "INSERT INTO gr6_orders (cart_id, tax, total) VALUES (%s, %s, %s)"
        execute_query(db_connection, query, data)
    return redirect('/admin_page')

# Admin route ***********************************************************************

@webapp.route('/admin_add_game', methods = ['GET', 'POST'])
def admin_add_game():
    if request.method == 'POST':
        cart_id = request.form['cart_id']
        game_id = request.form['game_id']
        db_connection = connect_to_database()
        data = (cart_id, game_id)
        query = "INSERT INTO gr6_games_carts (cart_id, game_id) VALUES (%s, %s)"
        execute_query(db_connection, query, data)
    return redirect('/admin_page')

# Admin Route *************************************************************************

@webapp.route('/delete_library', methods = ['GET', 'POST'])
def delete_library():
    print('Delete Library item')
    customer_id = request.form['customer_id']
    game_id = request.form['game_id']

    db_connection = connect_to_database()
    data = (customer_id, game_id)
    query = 'DELETE FROM gr6_library WHERE customer_id = %s AND game_id = %s'
    execute_query(db_connection, query, data)
    flash('Game Removed from Library')
    if 'handle' in session:
        return redirect('/game_library')
    else:
        return redirect('/admin_page')


########################################################################################
################# THE END ############################################################
########################################################################################

#.........................,::::+++++++++I+?=+I+I+++++++=.........................
#....................::::::::::+++++++++++++++++++++++++.........................
#..............::::::::::::::::+++++++++++++++++++++++++.........................
#.........:::::::::::::::::::::+++++++++++++++++++++++?+.........................
#.........:::::::::::::::::::::+++++++++++++++++++++++?+.........................
#.........:::::::::::::::::::::=++++++++++?++?+?=+++?+?+.........................
#.........:::::::::::::::::::,,,,,,,,,,,,,,,,,,,,,,,,,...........................
#.........::::::::::::::::,,,,,,,,,,,,,,,,,,,,,,,,,..............................
#.........:::::::::::::,,,,,,,,,,,,,,,,,,,,,,,,,.................................
#.........::::::::::::==========================.................................
#.........::::::::::::===,,,,,,,,,,,,,,,,,,,,,==.................................
#.........,::::::::::::==:,,,,,,,,,,,,,,,,,,,,,+~................................
#.........,,,::::::::::+++,,,,,,,,,,,,,,,,,,,,,++................................
#.........,,,,:::::::::~++,,,,,,,,,,,,,,,,,,,,,++................................
#.........,,,,,:::::::::++:,,,,,,,,,,,,,,,,,,,,:+~...............................
#.........,,,,,,::::::::+++,,,,,,,,,,,,,,,,,,,,,++...............................
#.........,,,,,,,:::::::~++,,,,,,,,,,,,,,,,,==:,++...............................
#.........,,,,,,,,:::::::++,,,,,,:=+++++++++?=++++=..............................
#.........,,,,,,,,:::::::+++++++++++=~~~~~~??~=?=~~~~............................
#.........,,,,,,,,,::::::::~~~~~~~~+??~~,..I,.~~~?+~~~~~,........................
#.........,,,,,,,,,:::::::::::~~~~~~~:???~~~~~~~~~:~~::,,,.......................
#.........,,,,,,,,,::::::::::::::~~~~~~:,,,,,,,,,,,,,,,,,........................
#.........,,,,,,,,,,::::::::::::::,,,,,,,,,,,,,,,,,,,,,..........................
#.........,,,,,,,,,,::::::::::::,,,,,,,,,,,,,,~=====.............................
#.........,,,,,,,,,,::::::::::,,,,:=========++++++++.............................
#.........,,,,,,,,,,:::::::=======+++++++++++++++~.+.............................
#.........,,,,,,,,,,:::::::+++++++++++++++++++++=,,=.............................
#.........,,,,,,,,,,:::::::++++++++++++++++++++++,,:.............................
#.........,,,,,,,,,,:::::::++++++++++++++++++++++.,.=............................
#.........,,,,,,,,,,:::::::++++++++++++++++++++++=++I77777I:.....................
#.........,,,,,,,,,::::::::+++++++++++++++++++++++++?777777777777+...............
#.........,,,,,,,,,::::::::++++++++++++++++++++++++++77777777777777777?..........
#.........,,,,,,,,,::::::::=+++++++++++++++++++++++++777777777777777I............
#.........,,,,,,,,:::::::::~+++++++++++++++++++++++++77777777777777..............
#..............,,:::::::::::+++++++++++++++++++++?I77777777777777,...............
#..................,::::::::++++++++++++++IIIII7777777777777777+.................
#.......................::::=+++++?I7777777777IIIIIII77II777I7...................
#................................................................................