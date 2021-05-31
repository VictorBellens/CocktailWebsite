from tabulate import tabulate

from django.shortcuts import render, HttpResponse
from .database.databasefile import select_cocktail, select_member