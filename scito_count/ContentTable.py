from scito_count.ContentTablesIO import *
import numpy as np

'''
Class to take ContentTablesIO stream, sort, deduplicate and send to BlockCatalog
'''

class ContentTable(object):
    def __init__(self, content_tables_io):
        unsorted_arr = np.frombuffer(content_tables_io.content_table, ('int64', (2)))
        self.content_table_arr = np.unique(unsorted_arr, axis=0)


