import unittest
from src.model.snippet import Snippet
from src.utilities.snippet_utils import merge_snippet

class TestSnippetUtils(unittest.TestCase):
    """
    Test class for Snippet related CRUD Services
    """

    def setUp(self):
        pass

    def test_snippet_utils_copy_success(self):
        old_snpt = Snippet(
            uri="www.sample.s3.uri.com/sample-uri",
            desc="Code for doing locality sensitive hashing",
            id="abcd-efgh-ijkl-mnop",
            tags=["search"],
            author="nmw",
            shares=[],
            audit={
                "last_upd_date": "2021-12-10",
                "last_upd_user": "nmw",
                "creation_date": "2021-12-10",
                "creation_user": "nmw"
            },
            lang="py"
        )
        new_snpt = Snippet(
            uri="www.sample.s3.uri.com/sample-uri/cpp-code",
            desc="Code for doing locality sensitive hashing",
            id="abcd-efgh-ijkl-mnop",
            tags=["search"],
            author="nmw",
            shares=[],
            audit={
                "last_upd_date": "2021-12-10",
                "last_upd_user": "nmw",
                "creation_date": "2021-12-10",
                "creation_user": "nmw"
            },
            lang="cpp"
        )
        old_snpt = merge_snippet(old_snpt, new_snpt)
        self.assertEqual(old_snpt.lang, "cpp")
        self.assertEqual(old_snpt.uri, "www.sample.s3.uri.com/sample-uri/cpp-code")

if __name__=="__main__":
    unittest.main()