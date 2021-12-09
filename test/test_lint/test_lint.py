'''
Testing linting functionality
'''
import unittest
from unittest import mock, TestCase
from src.model.snippet import Snippet
import src.manager.linting.linting_manager as lint

class TestLinting(TestCase):
    '''Class to test linting functionality '''
     # pylint: disable=unused-argument
    get_snippet_location = 'src.manager.linting.linting_manager.SnippetManager.get_snippet'

    @mock.patch(get_snippet_location, return_value=None)
    def test_get_lint_output_no_snippet(self, mock1):
        '''testing linting output when an incorrect snippet ID is passed'''
        rsp, err = lint.get_lint_output('123')
        self.assertTrue(err['error'])
        self.assertIsNone(rsp)

    @mock.patch(get_snippet_location, return_value=Snippet(lang='Ruby'))
    def test_lint_unsupported_lang(self, mock1):
        '''testing snippet where language is not supported for linting'''
        rsp, err = lint.get_lint_output('123')
        self.assertTrue(err['error'])
        self.assertIsNone(rsp)

    @mock.patch(get_snippet_location, 
    return_value=Snippet(lang='python', uri='http://www.binarySearch.py'))
    @mock.patch('src.manager.linting.linting_manager.run_python_script',
    return_value='pylint output')
    def test_happy_path_python(self, mock1, mock2):
        '''testing linting in python'''
        rsp, err = lint.get_lint_output('123')
        self.assertIsNone(err)
        self.assertIsNotNone(rsp)

    @mock.patch(get_snippet_location, 
    return_value=Snippet(lang='c++', uri='http://www.binarySearch.cpp'))
    @mock.patch('src.manager.linting.linting_manager.run_cpp_script', return_value='cpp output')
    def test_happy_path_cpp(self, mock1, mock2):
        '''testing linting in cpp'''
        rsp, err = lint.get_lint_output('123')
        self.assertIsNone(err)
        self.assertIsNotNone(rsp)
    
    @mock.patch(get_snippet_location, 
    return_value=Snippet(lang='java', uri='http://www.binarySearch.java'))
    @mock.patch('src.manager.linting.linting_manager.run_cpp_script', return_value='java output')
    def test_happy_path_java(self, mock1, mock2):
        '''testing static analysis in java'''
        rsp, err = lint.get_lint_output('123')
        self.assertIsNone(err)
        self.assertIsNotNone(rsp)


if __name__=="__main__":
    unittest.main()
