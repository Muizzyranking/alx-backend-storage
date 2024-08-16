#!/usr/bin/env python3
"""
Write a Python script that provides some
stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the
number of documents in this collection
second line: Methods:
5 lines with the number of documents with the
method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
"""

from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
    mongo_collection: The MongoDB collection containing the Nginx logs.

    Displays:
    - The total number of logs.
    - The count of logs for each HTTP method in the
    list ["GET", "POST", "PUT", "PATCH", "DELETE"].
    - The number of logs where method is "GET" and path is "/status".
    """
    # Print the total number of logs
    print(f"{mongo_collection.estimated_document_count()} logs")

    # Print the number of logs for each method
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count and print the number of logs
    # where method is "GET" and path is "/status"
    number_of_gets = mongo_collection.count_documents({"method": "GET",
                                                       "path": "/status"})
    print(f"{number_of_gets} status check")


if __name__ == "__main__":
    # Connect to the MongoDB server and access the
    # 'nginx' collection within the 'logs' database
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    # Call the function to display the Nginx log stats
    log_nginx_stats(mongo_collection)
