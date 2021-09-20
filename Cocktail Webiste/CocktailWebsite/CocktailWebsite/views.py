from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .database.databasefile import *
from .security import *
from .account import *
import ast
import sqlite3


from tabulate import tabulate

# URL REDIRECTS

# Login function, makes sure that the user does not bypass the website by manually typing in the URL


def menu(request):
    global user

    try:
        user.login_token # Checks if the 'account.py' file has initialized

    except NameError:
        return render(request, 'login.html', context={'bypass_fault': True}) # Means the user tried to bypass the login

    if user.login_token:
        return render(request, 'menu.html') # Log in successful
    else:
        print('Please login to use this feature.') # For console use
        # return render(request, 'requestLogin.html')


# Below are redirects to other functions
def browseurl(request):
    browse_cocktails(request)


def login(request):
    return render(request, 'login.html')


def redirect_account(request):
    return render(request, 'new_account.html')


# SEARCH FUNCTIONS

# Brings up the member and cocktail search templates
def search(request):
    return render(request, 'search.html')


def smembers(request):
    if request.method == 'GET':
        return render(request, 'smembers.html')


def scocktails(request):
    if request.method == 'GET':
        data = {
            'ingredients' : get_ingredient_values()
        }

        return render(request, 'scocktails.html', context={'data' : data})


# Takes the username and searches for it in the database
def searchmembers(request):
    if request.method == 'GET':
        context = {}

        req = request.GET.get('searchmembers') #req = name of user being searched for

        contents = select_member(req) # this function is in 'databasefile.py' and locates the information pertaining to that username
        personal_cocktails = get_user_cocktails(contents[0]) # fetches the cocktails relating to the user's information
        personal_information = select_member(req)

        if request.method == 'GET':
            if contents[4] == 'False': # Checks to see if the user's account is private
                number_of_cocktails = 0
                values = []

                context['personal_information'] = personal_information
                context['personal_cocktails'] = personal_cocktails

                for cocktail in personal_cocktails: # Re-formats all the cocktails
                    value_amounts = []
                    cocktail = list(cocktail)
                    i = 6

                    value_amounts.append(cocktail[0])
                    while i < 16:
                        combined = []
                        combined_ids = get_combined(cocktail[i])
                        combined.append(get_ingredient(combined_ids[1]))
                        combined.append(get_amount(combined_ids[0]))

                        cocktail[i] = combined

                        value_amounts.append(combined)

                        i += 1

                    number_of_cocktails += 1

                    values.append(value_amounts)

                context['number_of_cocktails'] = number_of_cocktails
                context['values'] = values

                print(context)

            elif contents[4] == 'True': # Means the user has a private account
                context['error1'] = 'True'

            return render(request, 'msearchresults.html', context=context)


def searchcocktails(request):
    if request.method == 'GET':
        search = request.GET.get('searchcocktails')

        try:
            contents = select_cocktail(search)
            context = { # Re-formatting the cocktail
                'name': contents[0],
                'directions': contents[1],
                'type': contents[2],
                'image': contents[3],
                'ranking_id': contents[4],
                'identifier': contents[5],
                'amount1': get_amount(get_combined(contents[6])[0])[0],
                'amount2': get_amount(get_combined(contents[7])[0])[0],
                'amount3': get_amount(get_combined(contents[8])[0])[0],
                'amount4': get_amount(get_combined(contents[9])[0])[0],
                'amount5': get_amount(get_combined(contents[10])[0])[0],
                'amount6': get_amount(get_combined(contents[11])[0])[0],
                'amount7': get_amount(get_combined(contents[12])[0])[0],
                'amount8': get_amount(get_combined(contents[13])[0])[0],
                'amount9': get_amount(get_combined(contents[14])[0])[0],
                'amount10': get_amount(get_combined(contents[15])[0])[0],
                'ingredient1': get_ingredient(get_combined(contents[6])[1])[0],
                'ingredient2': get_ingredient(get_combined(contents[7])[1])[0],
                'ingredient3': get_ingredient(get_combined(contents[8])[1])[0],
                'ingredient4': get_ingredient(get_combined(contents[9])[1])[0],
                'ingredient5': get_ingredient(get_combined(contents[10])[1])[0],
                'ingredient6': get_ingredient(get_combined(contents[11])[1])[0],
                'ingredient7': get_ingredient(get_combined(contents[12])[1])[0],
                'ingredient8': get_ingredient(get_combined(contents[13])[1])[0],
                'ingredient9': get_ingredient(get_combined(contents[14])[1])[0],
                'ingredient10': get_ingredient(get_combined(contents[15])[1])[0],
                'additional_notes': contents[16],
                'exists' : True

            }

            return render(request, "csearchresults.html", context=context)

        except TypeError: # means the drink with the given name does not exist
            return render(request, "scocktails.html", context={'does_not_exist': True})


def filter_search(request):
    if request.method == 'GET':
        filter_ingredient = request.GET.get('filter_ingredient')
        filter_type = request.GET.get('filter_type')



# BROWSE FUNCTIONS


def browse_cocktails(request):

    if request.method == "GET":
        option = request.GET.get('drop1')

        values = []
        contents = browse(option) # yields all the cocktails from the database
        context = {}

        number_of_cocktails = 0

        for cocktail in contents: # iterates through all the cocktails
            value_amounts = []
            cocktail = list(cocktail)
            i = 6

            value_amounts.append(cocktail[0])
            while i < 16:
                combined = []
                combined_ids = get_combined(cocktail[i])
                combined.append(get_ingredient(combined_ids[1])) # splitting up the amounts and the ingredients from the combined table
                combined.append(get_amount(combined_ids[0]))

                cocktail[i] = combined

                value_amounts.append(combined)

                i += 1

            number_of_cocktails += 1

            values.append(value_amounts)

        context['number_of_cocktails'] = number_of_cocktails
        context['all'] = contents
        context['values'] = values

        context['option'] = option

        return render(request, 'browse.html', context=context)


# LOGIN / CREATE ACCOUNT FUNCTIONS

def create_user():
    global user

    try:
        print(user.login_token) # if not already logged in

    except NameError:
        user = Login('', 0) # then create a default object

# get_username_information(username)[3]


def verifylogin(request):
    global total_bucket, final_bucket

    create_user()

    username = request.GET.get('username')
    password = request.GET.get('password')

    bucket_value = find_bucket_value(username, password) # Finds what bucket the password is in based on a formula
    total_bucket = find_password_key(bucket_value) # locates the password based on the user's bucket
    final_bucket = ast.literal_eval(total_bucket[0]) # yields the key and encrypted password

    for dictionary in final_bucket:
        if dec_message(dictionary, username) == password:
            global user

            print('Successfully signed in.')
            user = Login(username, find_identifier(username)) # initializes the users login information
            user.amend_token() # changes the login_token to True

            return render(request, 'menu.html')

        elif dec_message(dictionary, username) != password:
            print('Incorrect information, please try agian.') # passwords do not match

        else:
            print('Error')


def create_account(request):
    global hidden

    username = request.GET.get('username')
    password1 = request.GET.get('password1')
    password2 = request.GET.get('password2')
    hidden = request.GET.get('private')

    if bool(hidden) is not True:
        hidden = False

    new_account = CreateAccount(username, password1, password2) # creates an object containing the information
    checked = new_account.check_account_details() # password complexity checker, makes sure the password is complex enough

    if checked is True:
        # ACCOUNT IS VALID
        print('valid account')

        password_key_pair = enc_message(new_account.password1) # encrypts the password
        bucket = find_bucket_value(new_account.username, new_account.password1) # finds a bucket for the information using a formula

        add_to_passwords(new_account.username, password_key_pair, bucket) # adds to database
        add_user_to_members(new_account.username, bucket, hidden)

        return render(request, 'login.html', context={'account_created': True}) # account creation is successful

    elif type(checked) is list: # means that the password did not pass the criteria
        print('errors creating account')
        string = 'error'
        context = {}

        for error in checked:
            error_name = string + str(error)
            context[error_name] = True # returns which error it is in terms of numbers for the template

        return render(request, 'new_account.html', context=context)


# CREATE COCKTAIL FUNCTIONS


def add_user_cocktail(request):
    global user
    meta = []

    amounts = get_amount_values() # gets amounts and ingredients from the database
    ingredients = get_ingredient_values()

    if request.method == 'GET':
        data = {
            'amounts': amounts,
            'ingredients': ingredients,
        }

        combined1 = [request.GET.get('ingredient1'), request.GET.get('amount1')] # gets all the information necessary to create a cocktail
        combined2 = [request.GET.get('ingredient2'), request.GET.get('amount2')]
        combined3 = [request.GET.get('ingredient3'), request.GET.get('amount3')]
        combined4 = [request.GET.get('ingredient4'), request.GET.get('amount4')]
        combined5 = [request.GET.get('ingredient5'), request.GET.get('amount5')]
        combined6 = [request.GET.get('ingredient6'), request.GET.get('amount6')]
        combined7 = [request.GET.get('ingredient7'), request.GET.get('amount7')]
        combined8 = [request.GET.get('ingredient8'), request.GET.get('amount8')]
        combined9 = [request.GET.get('ingredient9'), request.GET.get('amount9')]
        combined10 = [request.GET.get('ingredient10'), request.GET.get('amount10')]
        name = request.GET.get('name')
        instructions = request.GET.get('instructions')
        type = request.GET.get('type')
        additional_notes = request.GET.get('additional_notes')

        combined_list = [combined1, combined2, combined3, combined4, combined5, combined6, combined7, combined8,
                         combined9, combined10]

        meta.append(name)
        meta.append(instructions)
        meta.append(type)
        meta.append(additional_notes)
        meta.append(user.identifier)

        print(meta)
        print(combined_list)

        if combined1[0] is None:
            return render(request, 'addcocktail.html', {'data': data}) # means the user didn't enter any values

        else:
            success_boolean = add_new_cocktail(combined_list, meta) # adds the cocktail to the database, returns errors if not added
            if success_boolean is True:
                return render(request, 'menu.html')  # means it was successful

            elif success_boolean is False: # means there was a syntax error
                error_message = 1
                'syntax error'

            elif success_boolean is sqlite3.IntegrityError: # means the cocktail already exists in the database
                error_message = 2
                'unique name error'

            else:
                error_message = 3 # something else went wrong
                'unknown error'

            return render(request, 'error.html', {'error_number': error_message})


# PROFILE


def profile(request):
    print(user.identifier)
    print(user.username)

    context = {}
    personal_cocktails = get_user_cocktails(user.identifier)
    personal_information = select_member(user.username)

    if request.method == 'GET':
        number_of_cocktails = 0
        values = []

        context['personal_information'] = personal_information
        context['personal_cocktails'] = personal_cocktails

        for cocktail in personal_cocktails: # re-formats the user's cocktails
            value_amounts = []
            cocktail = list(cocktail)
            i = 6

            value_amounts.append(cocktail[0])
            while i < 16:
                combined = []
                combined_ids = get_combined(cocktail[i])
                combined.append(get_ingredient(combined_ids[1])) # iterates through combined values and locates amount and ingredients
                combined.append(get_amount(combined_ids[0]))

                cocktail[i] = combined

                value_amounts.append(combined)

                i += 1

            number_of_cocktails += 1

            values.append(value_amounts)

        context['number_of_cocktails'] = number_of_cocktails # contextualizing the cocktail information
        context['values'] = values

        print(context)

        return render(request, 'profile.html', context=context)
