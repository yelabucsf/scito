from scito_count.ProcessSettings import *

'''
Class to pull pieces of tables of content from s3, sort, deduplicate
'''

class ContentTable(object):
    __slots__ = 'content_table'
    def __init__(self, s3_settings):
        ...