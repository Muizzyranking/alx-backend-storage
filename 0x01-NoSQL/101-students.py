#!/usr/bin/env python3
"""
101-students.py

This script defines a function to return all students
sorted by their average score in a MongoDB collection.

Prototype: def top_students(mongo_collection):
- mongo_collection will be the pymongo collection object.
- The average score must be part of each
item returned with the key 'averageScore'.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    Parameters:
    mongo_collection (Collection): The pymongo collection
    object containing the student documents.

    Returns:
    List[dict]: A list of dictionaries representing the
    student documents sorted by their average score.
    Each dictionary will include an additional key
    'averageScore' representing the average score.
    """
    # Use the aggregate method to calculate the average
    # score for each student and sort the results
    # 1. Use `$project` to calculate the average score of each student.
    #    - `name`: Pass through the 'name' field
    #       from the original document.
    #    - `averageScore`: Calculate the average of
    #       the 'score' field within the 'topics' array.
    # 2. Use `$sort` to sort the documents by the
    #   calculated `averageScore` in descending order.
    students = mongo_collection.aggregate([
        {
            "$project": {
                # Include the 'name' field in the output.
                "name": 1,
                # Calculate and include 'averageScore'.
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            # Sort the documents by 'averageScore' in descending order.
            "$sort": {"averageScore": -1}
        }
    ])

    # Convert the cursor returned by aggregate() to a list and return it.
    # return list(students)
    return [student for student in students]
