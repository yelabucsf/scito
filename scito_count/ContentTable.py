from scito_count.ContentTablesIO import *
import numpy as np

'''
Class to take ContentTablesIO stream, sort, deduplicate and send to BlockCatalog
'''

class ContentTable(object):
    def __init__(self, content_tables_io):
        if content_tables_io.content_table == None:
            raise AttributeError('ContentTable(): content_tables_io.content_table has not been generated.'
                                 'Run content_table_stream() on the instance of content_tables_io')
        unsorted_arr = np.frombuffer(content_tables_io.content_table.read(), ('int64', (2)))
        self.content_table_arr = np.unique(unsorted_arr, axis=0)


