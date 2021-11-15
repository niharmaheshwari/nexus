"""Utils to generate dummy data for elastic search and dynamo db"""
import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from requests_aws4auth import AWS4Auth
from src.constants.secrets import ACCESS_KEY, SECRET_ACCESS_KEY
from src.constants.constants import ELASTIC_SEARCH, AWS_REGION, SNIPPET_TABLE
from src.utils.utils import convert_to_dict
from src.model.snippet_snapshot import SnippetSnapshot
from src.model.snippet import Snippet
from src.model.audit import Audit


def create_es_session():
    """
    Generate elastic search session
    Returns: ES session object

    """
    service = "es"
    creds = boto3.Session(ACCESS_KEY,
                          SECRET_ACCESS_KEY,
                          region_name=AWS_REGION).get_credentials()

    awsauth = AWS4Auth(creds.access_key,
                       creds.secret_key,
                       AWS_REGION,
                       service,
                       session_token=creds.token)

    return OpenSearch([ELASTIC_SEARCH],
                    http_auth=awsauth,
                    use_ssl=True,
                    verify_certs=True,
                    connection_class=RequestsHttpConnection)


def create_dynamo_session():
    """
    Generate dynamodb session
    Returns: DynamoDB session object

    """
    service = "dynamodb"
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    dynamodb = session.resource(service, region_name=AWS_REGION)
    return dynamodb


def populate_elastic_search():
    """
    Generate random elastic search data
    """
    elastic = create_es_session()
    # User 1
    user1_snippet_1 = SnippetSnapshot(
        "user1-snippit-1",
        ["binary search"],
        "perform binary search",
        "c++"
    )
    user1_snippet_2 = SnippetSnapshot(
        "user1-snippit-2",
        ["quick sort"],
        "randomized quick sort",
        "python"
    )

    res1 = elastic.index(index="user1", doc_type='snippet', body=convert_to_dict(user1_snippet_1))
    res2 = elastic.index(index="user1", doc_type='snippet', body=convert_to_dict(user1_snippet_2))

    print(res1)
    print(res2)

    # User 2
    user2_snippet_1 = SnippetSnapshot(
        "user2-snippit-1",
        ["binary search"],
        "find upper bound using binary search",
        "c++"

    )
    user2_snippet_2 = SnippetSnapshot(
        "user2-snippit-2",
        ["quick sort"],
        "quick sort with pivot",
        "java"
    )

    user2_snippet_3 = SnippetSnapshot(
        "user2-snippit-3",
        ["binary search"],
        "find lower bound using binary search",
        "python"
    )

    res1 = elastic.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_1))
    res2 = elastic.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_2))
    res3 = elastic.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_3))

    print(res1)
    print(res2)
    print(res3)


def populate_dynamo_db():
    """
    Generate dynamodb data
    """
    dynamodb = create_dynamo_session()
    table = dynamodb.Table(SNIPPET_TABLE)

    user1_snippet1 = Snippet("s3-url",
                             "perform binary search",
                             "user1-snippit-1",
                             ["binary search"],
                             "user1",
                             [],
                             Audit(str(datetime.datetime.now()),
                                   "user1",
                                   str(datetime.datetime.now()),
                                   "user1"),
                             "c++")

    user1_snippet2 = Snippet("s3-url",
                             "randomized quick sort",
                             "user1-snippit-2",
                             ["quick sort"],
                             "user1",
                             [],
                             Audit(str(datetime.datetime.now()),
                                   "user1",
                                   str(datetime.datetime.now()),
                                   "user1"),
                             "python")
    user2_snippet1 = Snippet("s3-url",
                             "find upper bound using binary search",
                             "user2-snippit-1",
                             ["binary search"],
                             "user2",
                             [],
                             Audit(str(datetime.datetime.now()),
                                   "user2",
                                   str(datetime.datetime.now()),
                                   "user2"),
                             "c++")

    user2_snippet2 = Snippet("s3-url",
                             "quick sort with pivot",
                             "user2-snippit-2",
                             ["quick sort"],
                             "user2",
                             [],
                             Audit(str(datetime.datetime.now()),
                                   "user2",
                                   str(datetime.datetime.now()),
                                   "user2"),
                             "java")

    user2_snippet3 = Snippet("s3-url",
                             "find lower bound using binary search",
                             "user2-snippit-3",
                             ["binary search"],
                             "user2",
                             [],
                             Audit(str(datetime.datetime.now()),
                                   "user2",
                                   str(datetime.datetime.now()),
                                   "user2"),
                             "python")

    res1 = table.put_item(Item=convert_to_dict(user1_snippet1))
    res2 = table.put_item(Item=convert_to_dict(user1_snippet2))
    res3 = table.put_item(Item=convert_to_dict(user2_snippet1))
    res4 = table.put_item(Item=convert_to_dict(user2_snippet2))
    res5 = table.put_item(Item=convert_to_dict(user2_snippet3))
    print(res1)
    print(res2)
    print(res3)
    print(res4)
    print(res5)
