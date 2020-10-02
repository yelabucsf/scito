from unittest import TestCase
from scito_count.S3Interface import S3Interface


class TestS3Interface(TestCase):
    def setUp(self) -> None:
        self.s3_interface = S3Interface(bucket="ucsf-genomics-prod-project-data",
        object_key="anton/scito/mock/fastq/downsamp/seed100_ADT_own_S19_L003_R2_001.fastq.gz",
        profile="gvaihir")

    def test_obj_size(self):
        print(self.s3_interface.obj_size())
        self.assertEqual(self.s3_interface.obj_size(), 9945950)



