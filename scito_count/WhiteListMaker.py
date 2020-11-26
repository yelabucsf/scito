import numpy as np
from io import BytesIO
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *

class WhiteListMaker(object):
    def __init__(self, s3_settings: S3SettingsWhitelist):
        '''
        :param S3SettingsWhitelist: config file with cell and batch BC keys
        '''
        barcode_tuple = (s3_settings.bbc, s3_settings.cbc)
        bbc, cbc = [S3Interface(s3_settings.bucket, x, s3_settings.profile) for x in barcode_tuple]
        self.bbc, self.cbc = [self._from_stream(x) for x in [bbc, cbc]]

    def export_whitelist(self, save_name):
        self._construct_whitelist()
        np.savetxt(save_name, self.whitelist, fmt="%s", delimiter='\t', newline='\n')




    def _construct_whitelist(self):
        wl_array = np.array(np.meshgrid(self.cbc, self.bbc)).T.reshape(-1,2) # reshaping to 2 because 2 elements in string
        self.whitelist = np.array([''.join(x) for x in wl_array])

    def _from_stream(self, s3_interface):
        with BytesIO(s3_interface.s3_obj.get()["Body"].read()) as f:
            f.seek(0)
            out = np.loadtxt(f, dtype=str)
        return out