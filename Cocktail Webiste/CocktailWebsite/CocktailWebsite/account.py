from CocktailWebsite.database.databasefile import get_usernames


class Login:
    login_token = False

    def __init__(self, username, identifier):
        self.username = username
        self.identifier = identifier

    def amend_token(self):
        self.login_token = True


class CreateAccount:
    passwords_match = False
    password_complexity = False
    username_in_database = False
    error_ids = []

    def __init__(self, username, password1, password2):
        self.username = username
        self.password1 = password1
        self.password2 = password2

        try:
            if self.error_ids[0] is not None:
                self.error_ids = []

        except IndexError:
            pass

    def check_passwords_match(self):
        if self.password1 == self.password2:
            self.passwords_match = True
        else:
            # PASSWORDS DO NOT MATCH
            self.error_ids.append(0)

        return self.passwords_match

    def check_password_complexity(self):
        character_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '`']
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        character_counter = 0
        number_counter = 0

        for character in character_list:
            if character in self.password1:
                character_counter += 1

        for number in number_list:
            if number in self.password1:
                number_counter += 1

        if character_counter >= 2 and number_counter >= 2 and len(self.password1) > 7:
            self.password_complexity = True
            return self.password_complexity

        if self.password1.isalpha():
            # PASSWORD CANNOT BE ALL CHARACTERS
            self.error_ids.append(1)

        if self.password1.isnumeric():
            # PASSWORD CANNOT BE ALL NUMBERS
            self.error_ids.append(2)

        if character_counter < 2:
            # NEEDS AT LEAST 2 UNIQUE CHARACTERS
            self.error_ids.append(3)

        if number_counter < 2:
            # NEEDS AT LEAST 2 NUMBERS
            self.error_ids.append(4)

        if len(self.password1) < 7:
            # LENGTH OF PASSWORD NOT LONG ENOUGH
            self.error_ids.append(5)

        return self.password_complexity

    def check_username_in_database(self):
        username_list = get_usernames()
        print(username_list)
        for entity in username_list:
            if self.username == entity[0]:
                # USERNAME ALREADY EXISTS
                self.error_ids.append(6)
                return self.username_in_database

        self.username_in_database = True
        return self.username_in_database

    def check_account_details(self):
        passwords_match = self.check_passwords_match()
        password_complexity = self.check_password_complexity()
        username_not_taken = self.check_username_in_database()

        if passwords_match and password_complexity and username_not_taken:
            return True

        else:
            print(self.error_ids)
            return self.error_ids
