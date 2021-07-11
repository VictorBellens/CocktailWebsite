import sqlite3
login_key = 'Jack'


def select_cocktail(id):
    name = ' '.join(w[0].upper() + w[1:] for w in id.split())

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cocktails where drink=?;", (name, ))
        product = cursor.fetchone()
        return product


def select_member(name):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (name.lower(), ))
        member = cursor.fetchone()
        return member


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


def get_amount(id):
    if id == 0:
        result = ('', )
        return result

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT value FROM Amounts where amount_id=?", (id, ))
        result = cursor.fetchone()
        return result


def get_ingredient(id):
    if id == 0:
        result = ('', )
        return result

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient FROM Ingredients where ingredient_id=?", (id, ))
        result = cursor.fetchone()
        return result


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


def get_profile():
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (login_key, ))
        profile_results = cursor.fetchone()

        return profile_results


def browse(choice):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cocktails where ranking_id=?", (choice, ))
        browse_results = cursor.fetchall()

    return browse_results


# SECURITY

def get_username_information(username):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (username, ))
        information = cursor.fetchone()

    return information


def find_password_key(bucket_value):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT hashed_key FROM Passwords where bucket=?", (bucket_value, ))
        bucket = cursor.fetchone()

    return bucket


def find_identifier(username):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT indentifier FROM Members where name=?", (username, ))
        identifier = cursor.fetchone()

    return identifier[0]


# ADDING COCKTAILS

def get_amount_values():
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT value FROM Amounts", ())
        result = cursor.fetchall()

    return result


def get_ingredient_values():
    with sqlite3.connect('CWDatabase.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient from Ingredients", ())
        result = cursor.fetchall()

    return result


def find_amount_id(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT amount_id FROM Amounts where value=?", (combined,))
        result = cursor.fetchone()

        if result is None:
            result = (0,)

    return result


def find_ingredient_id(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT ingredient_id from Ingredients where ingredient=?", (combined,))
        result = cursor.fetchone()

        if result is None:
            result = (0,)

    return result


def add_new_combined(combined):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO Combined(amount_id, ingredient_id)'
                       'VALUES(?, ?)', (combined[1], combined[0]))
        db.commit()

        cursor.execute('SELECT combined_id from Combined where amount_id=? and ingredient_id=?', (combined[1], combined[0]))
        result = cursor.fetchone()
    return result


def add_new_cocktail(contents, meta):
    combined_list = []
    combined_id_list = []

    try:
        for combined in contents:
            combined_ids = []

            ingredient_value = find_ingredient_id(str(combined[0]))
            amount_value = find_amount_id(str(combined[1]))

            combined_ids.append(ingredient_value[0])
            combined_ids.append(amount_value[0])

            combined_list.append(combined_ids)
        print(combined_list)

        for combined in combined_list:
            combined_id_list.append(add_new_combined(combined)[0])

        print(combined_id_list)
        print(meta)

        with sqlite3.connect("CWDatabase.db") as db:
            cursor = db.cursor()

            cursor.execute("INSERT INTO Cocktails (drink, instructions, type, ranking_id, combined1, combined2, combined3, "
                           "combined4, combined5, combined6, combined7, combined8, combined9, combined10, additional_notes)"
                           "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (meta[0], meta[1], meta[2], 3, combined_id_list[0], combined_id_list[1], combined_id_list[2],
                            combined_id_list[3], combined_id_list[4], combined_id_list[5], combined_id_list[6],
                            combined_id_list[7], combined_id_list[8], combined_id_list[9], meta[3])
                           )
            db.commit()
        return True

    except SyntaxError:
        return False

    except sqlite3.IntegrityError:
        return sqlite3.IntegrityError


# PROFILE

def get_user_cocktails(identifier):
    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * from Cocktails where identifier=?", (identifier,))
        result = cursor.fetchall()

    return result
