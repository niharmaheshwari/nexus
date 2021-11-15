'''
Utility methods to work with Snippet Objects
'''
from src.model.snippet import Snippet

def merge_snippet(old_snip: Snippet, new_snip: Snippet):
    '''
    Fixed code to compare two Snippets, apply new snippets changes onto
    the old snippet and return the updated Snippet object
    Arguments:
        old_snip    : Old Snippet Object
        new_snip    : New Snippet Object
    '''
    if new_snip.id is not None:
        old_snip.id = new_snip.id
    if new_snip.uri is not None:
        old_snip.uri = new_snip.uri
    if new_snip.audit is not None:
        old_snip.audit['last_upd_date'] = new_snip.audit['last_upd_date']
        old_snip.audit['last_upd_user'] = new_snip.audit['last_upd_user']
    if new_snip.desc is not None:
        old_snip.desc = new_snip.desc
    if new_snip.shares is not None:
        old_snip.shares = new_snip.shares
    if new_snip.lang is not None:
        old_snip.lang = new_snip.lang
    if new_snip.tags is not None:
        old_snip.tags = new_snip.tags
    return old_snip
