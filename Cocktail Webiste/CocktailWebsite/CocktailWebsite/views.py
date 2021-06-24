from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .database.databasefile import *
from .security import *
import ast

from tabulate import tabulate

# URL REDIRECTS


def search(request):
    return render(request, 'search.html')


def menu(request):
    return render(request, 'menu.html')


def profile(request):
    return render(request, 'profile.html')


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

        contents = browse(option)
        context = {}

        number_of_cocktails = 0
        string = 'list'

        for cocktail in contents:
            number_of_cocktails += 1
            final_string = string + str(number_of_cocktails)
            context[final_string] = cocktail

        context['number_of_cocktails'] = number_of_cocktails
        context['all'] = contents
        context['option'] = option

        return render(request, 'browse.html', context=context)


# LOGIN FUNCTIONS


def verifylogin(request):
    global total_bucket, final_bucket

    username = request.GET.get('username')
    password = request.GET.get('password')

    bucket_value = get_username_information(username)[3]
    total_bucket = find_password_key(bucket_value)
    final_bucket = ast.literal_eval(total_bucket[0])

    for dictionary in final_bucket:
        if dec_message(dictionary, username) == password:
            print('Successfully signed in.')
            with open('LoginToken.txt', 'w') as f:
                f.write('true')

            return render(request, 'menu.html')


# CREATE COCKTAIL FUNCTIONS


def add_user_cocktail(request):

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


        if combined1[0] is None:
            return render(request, 'addcocktail.html', {'data': data})

        else:
            print(combined_list)
            add_new_cocktail(combined_list)
