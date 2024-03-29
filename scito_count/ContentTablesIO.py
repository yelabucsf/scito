from io import BytesIO
from scito_count.S3Interface import *


class ContentTablesIO(object):
    __slots__ = 'content_table', 's3_settings'

    def __init__(self, s3_settings):
        '''
        Class to pull pieces of tables of content from s3 into a ByteIO stream
        :param s3_settings: S3Settings object
        '''
        self.s3_settings = s3_settings
        self.content_table = None

    def content_table_stream(self):
        content_table_gen = self._generate_content_tables()
        self.content_table = BytesIO()
        for c_table_interface in content_table_gen:
            c_table = c_table_interface.s3_obj.get()["Body"].read()
            self.content_table.write(c_table)
        self.content_table.seek(0)

    def _generate_content_tables(self):
        prefix = self.s3_settings.object_key.split('.')[0]
        s3_interface: S3Interface = S3Interface(self.s3_settings.bucket,
                                                self.s3_settings.object_key)
        for s3_obj in s3_interface.filter_objects(prefix):
            temp_interface = S3Interface(self.s3_settings.bucket,
                                         s3_obj.key)

            if temp_interface.s3_obj.content_type != 'BLOCK_BYTE':
                continue
            yield temp_interface
