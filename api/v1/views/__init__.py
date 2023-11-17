#!/usr/bin/python3
'''Imports Blueprints, creates the variable-instance
of Blueprint and imports everything from index package'''
from flask import Blueprint


app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')


from api.v1.views.index import *