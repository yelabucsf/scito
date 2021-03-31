from scito_count.S3Interface import S3Interface
import os


class S3InterfaceGen(object):
    def __init__(self, s3_settings, file_type, misc_id=''):
        '''
        Class to generate new S3 interface to store data. Produces key of type {original_key}.{misc_id}
        :param s3_settings: S3Settings object
        :param misc_id: Additional identifier like file part
        '''
        self.s3_settings = s3_settings
        self.file_type = file_type
        self.misc_id = misc_id

    def new_key(self, **kwargs):
        basename = os.path.basename(self.s3_settings.object_key).split(".")[0]
        if self.misc_id == '':
            new_basename = '.'.join([basename, self.file_type.upper()])
        else:
            new_basename = '.'.join([basename, self.file_type.upper(), self.misc_id])
        new_s3_key = os.path.join(os.path.dirname(self.s3_settings.object_key), new_basename)
        s3_interface: S3Interface = S3Interface(self.s3_settings.bucket, new_s3_key, **kwargs)

        return s3_interface
