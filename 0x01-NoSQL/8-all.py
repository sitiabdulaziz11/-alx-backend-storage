#!/usr/bin/env python3
"""
Module that list all document in
mongodb by python script
"""


def list_all(mongo_collection):
    """
    Python function that lists all
    documents in a collection:
    """
    return mongo_collection.find()
