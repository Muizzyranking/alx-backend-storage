#!/usr/bin/env python3
"""
10-update_topics.py

This script defines a function to update all topics of a school
document based on the school's name in a MongoDB collection.

Prototype: def update_topics(mongo_collection, name, topics):
- mongo_collection will be the pymongo collection object.
- name (string) will be the school name to update.
- topics (list of strings) will be the list
of topics approached in the school.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the list of topics for a school document
    in the collection based on the school's name.

    Parameters:
    mongo_collection (Collection): The pymongo collection
    object containing the school documents.
    name (str): The name of the school whose
    topics are to be updated.
    topics (List[str]): The new list of topics to
    set for the school document.

    Returns:
    None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
