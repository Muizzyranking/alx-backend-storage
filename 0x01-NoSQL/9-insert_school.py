#!/usr/bin/env python3
"""
Insert a new document into a MongoDB
collection based on keyword arguments.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the given MongoDB
    collection based on the provided keyword arguments.

    Parameters:
    mongo_collection (Collection): The pymongo collection object
                                    into which the document will be inserted.
    **kwargs (Any): Keyword arguments representing the fields
                    and values of the document to be inserted.

    Returns:
    str: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)

    # Return the _id of the newly inserted document
    # return str(result.inserted_id)
    return result.inserted_id
