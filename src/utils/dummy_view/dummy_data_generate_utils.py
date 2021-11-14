from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3
from src.constants.secrets import ACCESS_KEY, SECRET_KEY
from src.constants.constants import ELASTIC_SEARCH, AWS_REGION
from requests_aws4auth import AWS4Auth
from src.utils.utils import convert_to_dict
from src.model.snippet_snapshot import SnippetSnapshot

SERVICE = "es"
creds = boto3.Session(ACCESS_KEY, SECRET_KEY, region_name=AWS_REGION).get_credentials()

awsauth = AWS4Auth(creds.access_key, creds.secret_key, AWS_REGION, SERVICE, session_token=creds.token)


es = OpenSearch([ELASTIC_SEARCH],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection)


def populate_elastic_search():
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

    res1 = es.index(index="user1", doc_type='snippet', body=convert_to_dict(user1_snippet_1))
    res2 = es.index(index="user1", doc_type='snippet', body=convert_to_dict(user1_snippet_2))

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

    res1 = es.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_1))
    res2 = es.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_2))
    res3 = es.index(index="user2", doc_type='snippet', body=convert_to_dict(user2_snippet_3))

    print(res1)
    print(res2)
    print(res3)


