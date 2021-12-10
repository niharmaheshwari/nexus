'''
Linting Manager
'''
from subprocess import Popen, PIPE
from src.manager.snippet_manager import SnippetManager
from src.model.message_format import MessageFormat
import src.utilities.logging as log

logger = log.get_logger(__name__)

# def run_python_script(uri):
#     '''Function that runs pylint and returns the stdout'''
#     logger.info("running python script...")
#     with Popen(['bash','./src/manager/linting/python_lint.sh', uri],
#                stdout=PIPE, stderr=PIPE) as session:
#         stdout, _ = session.communicate()
#         return stdout.decode('utf-8')

def run_python_script(uri):
    '''Function that runs pylint and returns the stdout'''
    logger.info("running python script...")
    session = Popen(['bash','./src/manager/linting/python_lint.sh', uri], stdout=PIPE, stderr=PIPE)
    stdout, _ = session.communicate()
    return stdout.decode('utf-8')
    
print(run_python_script('https://snippets-s.s3.us-east-2.amazonaws.com/binary_search.py'))

def run_cpp_script(uri):
    '''function that runs cpplint and returns the stderr'''
    logger.info("running cpp script...")
    with Popen(['bash','./src/manager/linting/cpp_lint.sh', uri],
     stdout=PIPE, stderr=PIPE) as session:
        _, stderr = session.communicate()
        return stderr.decode('utf-8')

def run_java_script(uri):
    '''function that runs javac and returns the stderr'''
    logger.info("running java script...")
    with Popen(['bash','./src/manager/linting/java_compile.sh', uri],
    stdout=PIPE, stderr=PIPE) as session:
        _, stderr = session.communicate()
        return stderr.decode('utf-8')

def run_linter(lang, uri):
    '''function that determines which linter to use and calls it'''
    if lang in ('Python', 'python'):
        rsp = run_python_script(uri)
    elif lang in ('C++', 'c++'):
        rsp = run_cpp_script(uri)
    else: # lang is java
        rsp = run_java_script(uri)
    return rsp

def get_lint_output(snippet_id):
    '''function that returns lint output for a snippetID and error'''
    manager = SnippetManager()
    snippet = manager.get_snippet(snippet_id)
    if snippet is None:
        return None, MessageFormat().error_message("snippet does not exist")
    accepted_langs = ['Python', 'python', 'C++', 'c++', 'java', 'Java']
    if snippet.lang not in accepted_langs:
        msg = "snippet language not supported for linting"
        return None, MessageFormat().error_message(msg)
    rsp = run_linter(snippet.lang, snippet.uri)
    return rsp, None
