from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .database.databasefile import *
from .security import *
from .account import *
import ast


from tabulate import tabulate

# URL REDIRECTS


def search(request):
    return render(request, 'search.html')


def menu(request):
    global user

    if user.login_token:
        print(user.username)
        return render(request, 'menu.html')
    else:
        print('Please log in to use this feature')


def browseurl(request):
    browse_cocktails(request)


def login(request):
    return render(request, 'login.html')


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
            return render(request, 'error.html')

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

            }

            return render(request, "csearchresults.html", context=context)

        except TypeError:
            return render(request, 'error.html')


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


# LOGIN FUNCTIONS

def create_user():
    global user

    try:
        print(user.login_token)

    except NameError:
        user = Login('', 0)


def verifylogin(request):
    global total_bucket, final_bucket

    create_user()

    username = request.GET.get('username')
    password = request.GET.get('password')

    bucket_value = get_username_information(username)[3]
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


# CREATE COCKTAIL FUNCTIONS


def add_user_cocktail(request):
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

        if combined1[0] is None:
            return render(request, 'addcocktail.html', {'data': data})

        else:
            print(add_new_cocktail(combined_list, meta))


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
