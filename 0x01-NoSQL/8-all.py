#!/usr/bin/env python3
"""
8-all.py

Function to list all documents in a collection.

This script defines a function to list
all documents in a MongoDB collection.
The function returns an empty list if
there are no documents in the collection.
"""


def list_all(mongo_collection):
    """
    List all documents in the given MongoDB collection.

    Parameters:
    mongo_collection (Collection): The pymongo collection object from
                                    which to list/retrieve documents.

    Returns:
    List[Dict]: A list of dictionaries representing all
                the documents in the collection.
                Returns an empty list if the collection is
                empty, has no documents or not provided.
    """
    if mongo_collection is None or mongo_collection.count_documents({}) == 0:
        return []

    documents = mongo_collection.find()

    return [document for document in documents]
