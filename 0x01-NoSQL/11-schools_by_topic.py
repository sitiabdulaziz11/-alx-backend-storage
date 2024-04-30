#!/usr/bin/env python3
"""Module that return list of school"""


def schools_by_topic(mongo_collection, topic):
    """
    Python function that returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})
