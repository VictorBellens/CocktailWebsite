from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .database.databasefile import *
from .security import *
from .account import *
import ast
import sqlite3


from tabulate import tabulate

# URL REDIRECTS


def search(request):
    return render(request, 'search.html')


def menu(request):
    global user

    try:
        user.login_token

    except NameError:
        return render(request, 'login.html', context={'bypass_fault': True})

    if user.login_token:
        return render(request, 'menu.html')
    else:
        print('Please login to use this feature.')
        # return render(request, 'requestLogin.html')



def browseurl(request):
    browse_cocktails(request)


def login(request):
    return render(request, 'login.html')


def redirect_account(request):
    return render(request, 'new_account.html')


# SEARCH FUNCTIONS


def smembers(request):
    if request.method == 'GET':
        return render(request, 'smembers.html')


def scocktails(request):
    if request.method == 'GET':
        return render(request, 'scocktails.html')


def searchmembers(request):
    if request.method == 'GET':
        search = request.GET.get('searchmembers')

        contents = select_member(search)

        if contents is None:
            return render(request, 'smembers.html', context={'user_does_not_exist': True})

        context = {
            'identifier': contents[0],
            'name': contents[1],
            'image': contents[2],
            'bucket': contents[3]
        }

        return render(request, 'msearchresults.html', context=context)


def searchcocktails(request):
    if request.method == 'GET':
        search = request.GET.get('searchcocktails')

        try:
            contents = select_cocktail(search)
            context = {
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

        except TypeError:
            return render(request, "scocktails.html", context={'does_not_exist': True})


# BROWSE FUNCTIONS


def browse_cocktails(request):

    if request.method == "GET":
        option = request.GET.get('drop1')

        values = []
        contents = browse(option)
        context = {}

        number_of_cocktails = 0

        for cocktail in contents:
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
        context['all'] = contents
        context['values'] = values

        context['option'] = option

        return render(request, 'browse.html', context=context)


# LOGIN / CREATE ACCOUNT FUNCTIONS

def create_user():
    global user

    try:
        print(user.login_token)

    except NameError:
        user = Login('', 0)

# get_username_information(username)[3]


def verifylogin(request):
    global total_bucket, final_bucket

    create_user()

    username = request.GET.get('username')
    password = request.GET.get('password')

    bucket_value = find_bucket_value(username, password)
    total_bucket = find_password_key(bucket_value)
    final_bucket = ast.literal_eval(total_bucket[0])

    for dictionary in final_bucket:
        if dec_message(dictionary, username) == password:
            global user

            print('Successfully signed in.')
            user = Login(username, find_identifier(username))
            user.amend_token()

            return render(request, 'menu.html')

        elif dec_message(dictionary, username) != password:
            print('Incorrect information, please try agian.')

        else:
            print('Error')


def create_account(request):
    username = request.GET.get('username')
    password1 = request.GET.get('password1')
    password2 = request.GET.get('password2')

    new_account = CreateAccount(username, password1, password2)
    checked = new_account.check_account_details()

    if checked is True:
        # ACCOUNT IS VALID
        print('valid account')

        password_key_pair = enc_message(new_account.password1)
        bucket = find_bucket_value(new_account.username, new_account.password1)

        add_to_passwords(new_account.username, password_key_pair, bucket)
        add_user_to_members(new_account.username, bucket)

        return render(request, 'login.html', context={'account_created': True})



    elif type(checked) is list:
        print('errors creating account')
        string = 'error'
        context = {}

        for error in checked:
            error_name = string + str(error)
            context[error_name] = True

        return render(request, 'new_account.html', context=context)


# CREATE COCKTAIL FUNCTIONS


def add_user_cocktail(request):
    global user
    meta = []

    amounts = get_amount_values()
    ingredients = get_ingredient_values()

    if request.method == 'GET':
        data = {
            'amounts': amounts,
            'ingredients': ingredients,
        }

        combined1 = [request.GET.get('ingredient1'), request.GET.get('amount1')]
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

        if combined1[0] is None:
            return render(request, 'addcocktail.html', {'data': data})

        else:
            success_boolean = add_new_cocktail(combined_list, meta)

            if success_boolean is True:
                return render(request, 'menu.html')


            elif success_boolean is False:
                error_message = 1
                'syntax error'

            elif success_boolean is sqlite3.IntegrityError:
                error_message = 2
                'unique name error'

            else:
                error_message = 3
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
        context['personal_information'] = personal_information
        context['personal_cocktails'] = personal_cocktails

        print(context)

        return render(request, 'profile.html', context=context)
