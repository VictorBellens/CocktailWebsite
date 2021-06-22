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
    name = ' '.join(w[0].upper() + w[1:] for w in name.split())

    with sqlite3.connect("CWDatabase.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members where name=?", (name, ))
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
