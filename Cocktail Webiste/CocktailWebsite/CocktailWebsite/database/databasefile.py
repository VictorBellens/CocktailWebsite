import sqlite3
import ast

login_key = 'Jack'


# selects a ccoktail given drink name
def select_cocktail(id):
    name = ' '.join(w[0].upper() + w[1:] for w in id.split())

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cocktails where drink=?;", (name, ))
        product = cursor.fetchone()
        return product


# selects a member given username
def select_member(name):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (name.lower(), ))
        member = cursor.fetchone()
        return member


# gets amount and ingredient id based on combined id, relates directly to cocktails table
def get_text(id):
    combined_list = []
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT amount_id FROM Combined where combined_id=?", (id, ))
        amount = cursor.fetchone()

        cursor.execute("SELECT ingredient_id FROM Combined where combined_id=?", (id, ))
        ingredient = cursor.fetchone()

        combined_list.append(get_amount(amount))
        combined_list.append(get_ingredient(ingredient))
        return combined_list


# gets the value from Amounts table given the amount id
def get_amount(id):
    if id == 0:
        result = ('', )
        return result

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT value FROM Amounts where amount_id=?", (id, ))
        result = cursor.fetchone()
        return result


# gets the ingredient from Ingredients table given the ingredient id
def get_ingredient(id):
    if id == 0:
        result = ('', )
        return result

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient FROM Ingredients where ingredient_id=?", (id, ))
        result = cursor.fetchone()
        return result


# fetches amounts and ingredient ids from combined table
def get_combined(id):
    result = []
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT amount_id FROM Combined where combined_id=?", (id, ))
        amount_result = cursor.fetchone()

        cursor.execute("SELECT ingredient_ID FROM Combined where combined_id=?", (id, ))
        ingredient_result = cursor.fetchone()

        result.append(amount_result[0])
        result.append(ingredient_result[0])
        return result


# initial fetch of user information, used when create the Login object
def get_profile():
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (login_key, ))
        profile_results = cursor.fetchone()

        return profile_results


# selects all cocktails with a specific ranking id (1, 2, 3)
def browse(choice):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cocktails where ranking_id=?", (choice, ))
        browse_results = cursor.fetchall()

    return browse_results


# SECURITY

# selects username information given the username
def get_username_information(username):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (username, ))
        information = cursor.fetchone()

    return information


# selects the encrypted password from the Passwords table given a bucket value (found in profile table)
def find_password_key(bucket_value):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT hashed_key FROM Passwords where bucket=?", (bucket_value, ))
        bucket = cursor.fetchone()

    return bucket


# finds the identifier from the Members table given the username
def find_identifier(username):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT indentifier FROM Members where name=?", (username, ))
        identifier = cursor.fetchone()

    return identifier[0]


# gets all the usernames from the members table
def get_usernames():
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM Members", ())
        names = cursor.fetchall()

    return names


# ADDING COCKTAILS

# selects all the values from the Amounts table
def get_amount_values():
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT value FROM Amounts", ())
        result = cursor.fetchall()

    return result


# selects all the ingredients from the Ingredients table
def get_ingredient_values():
    with sqlite3.connect('CWDatabase.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient from Ingredients", ())
        result = cursor.fetchall()

    return result


# selects the amount id from the Amounts table given the amount name
def find_amount_id(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT amount_id FROM Amounts where value=?", (combined,))
        result = cursor.fetchone()

        if result is None:
            result = (0,)

    return result


# selects the ingredient id from the Ingredients table given the amount name
def find_ingredient_id(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient_id from Ingredients where ingredient=?", (combined,))
        result = cursor.fetchone()

        if result is None:
            result = (0,)

    return result


# adds a new combined value in the Combined table
def add_new_combined(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO Combined(amount_id, ingredient_id)'
                       'VALUES(?, ?)', (combined[1], combined[0]))
        db.commit()

        cursor.execute('SELECT combined_id from Combined where amount_id=? and ingredient_id=?', (combined[1], combined[0]))
        result = cursor.fetchone()
    return result


# adds a new cocktail when inputted information from user
def add_new_cocktail(contents, meta):
    combined_list = []
    combined_id_list = []

    try:
        for combined in contents:
            combined_ids = []

            ingredient_value = find_ingredient_id(str(combined[0])) # changing amounts and ingredients into ids
            amount_value = find_amount_id(str(combined[1]))

            combined_ids.append(ingredient_value[0]) # creating new combined values with the amounts and ingredients
            combined_ids.append(amount_value[0])

            combined_list.append(combined_ids)
        print(combined_list) # for console use only

        for combined in combined_list:
            combined_id_list.append(add_new_combined(combined)[0])

        print(combined_id_list)
        print(meta)

        with sqlite3.connect("CWDatabase.db") as db: # connects to db and executes below statement, adding a new cocktial with all the information required
            cursor = db.cursor()

            cursor.execute("INSERT INTO Cocktails (drink, instructions, type, ranking_id, identifier, combined1, combined2, "
                           "combined3, combined4, combined5, combined6, combined7, combined8, combined9, combined10,"
                           "additional_notes)"
                           "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (meta[0], meta[1], meta[2], 3, meta[4], combined_id_list[0], combined_id_list[1],
                            combined_id_list[2], combined_id_list[3], combined_id_list[4], combined_id_list[5],
                            combined_id_list[6], combined_id_list[7], combined_id_list[8], combined_id_list[9], meta[3])
                           ) # if the cocktail does not have 10 combined values, it appends 0 combined id which means no ingreident nor amount
            db.commit()
        return True

    except SyntaxError: # returns False raising an expected error because of invalid input (i.e image inputted instead of text)
        return False

    except sqlite3.IntegrityError: # returns sqlite3 unique name error meaning cocktail already exists.
        return sqlite3.IntegrityError


# PROFILE

# selects all the users cocktails given the users unique identifier
def get_user_cocktails(identifier):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * from Cocktails where identifier=?", (identifier,))
        result = cursor.fetchall()

    return result


# adds a new user to the database
def add_user_to_members(username, bucket, hidden):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO Members (name, bucket, private)' # private is the privacy option
                       'VALUES(?, ?, ?)', (username, bucket, hidden))
        db.commit()


# adds new password and key into the Passwords table
def add_to_passwords(username, password_key_pair, bucket):
    dictionary = {username: password_key_pair}

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT hashed_key from Passwords where bucket=?", (bucket,)) # fetches the contents from the bucket with pre-calculated bucket value
        bucket_contents = cursor.fetchone()

        final_bucket = ast.literal_eval(bucket_contents[0]) # adds password and key dictionary to the rest of the other passwords
        final_bucket.append({username: password_key_pair})
        print(final_bucket)

        cursor.execute("UPDATE Passwords SET hashed_key=? WHERE bucket=?", (str(final_bucket), bucket)) # puts the bucket back but now contains the new password
        db.commit()
