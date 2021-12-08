num = (1,)

@webapp.route('/carts')
def carts():
    db_connection = connect_to_database()
    query = "SELECT game_id FROM gr6_games_carts WHERE cart_id = %s"
    result = execute_query(db_connection, query, num).fetchall()
    print(result)
    return render_template('carts.html')

@webapp.route('/game_library')
def library():
    db_connection = connect_to_database()
    query = "SELECT game_title FROM gr6_games INNER JOIN gr6_library ON gr6_games.game_id = gr6_library.game_id INNER JOIN gr6_customers ON gr6_library.customer_id = gr6_customers.customer_id  WHERE gr6_customers.customer_id = %s"
    result = execute_query(db_connection, query, num).fetchall()
    print(result)
    return render_template('game_library.html')

@webapp.route('/gamepage')
def gamepage():
    db_connection = connect_to_database()
    query = "SELECT game_id FROM gr6_games"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('gamepage.html')

@webapp.route('/order_page')
def order_page():
    db_connection = connect_to_database()
    query = "SELECT order_number FROM gr6_orders"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('order_page.html')

@webapp.route('/user_profile') #, methods=['POST', 'GET'])
def user_profile():
    # if request.method == "POST":
    #     fname = request.form['fname']
    #     lname = request.form['lname']
    #     handle = request.form['handle']
    #     card = request.form['credit_card']
    #     state = request.form['state']
    #     city = request.form['city']
    #     street = request.form['street']
    #     street_number = request.form['street_number']

    db_connection = connect_to_database()
    query1 = "SELECT fname, lname, handle, credit_card, state, city, street, street_number FROM gr6_customers WHERE customer_id = %s"
    #     query2 = 'INSERT INTO gr6_customers (/*customer_id*/, fname, lname, handle, credit_card, state, city, street, street_number) VALUES (/*%s*/, %s, %s, %s, %s, %s, %s, %s, %s)'
    #     query3 = 'UPDATE gr6_customers SET fname=%s, lanme=%s, handle=%s, /*credit_card=%s*/, state=%s, city=%s, street=%s, street_number=%s WHERE customer_id=%s'

    #     data = (fname, lname, handle, card, state, city, street, street_number)
    result = execute_query(db_connection, query1, num).fetchall()
    #     result = execute_query(db_connection, query2)

    #     customer_id = result.fetchall()
    #     profile = (fname, lname, handle, card, state, city, street, street_number)
    #     result = execute_query(db_connection, query3, data)
    print(result)
    # return render_template('user_profile.html', profile = profile)

    return render_template('user_profile.html')
