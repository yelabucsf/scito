from unittest import TestCase
from scito_count.SQSInterface import *
from scito_count.ProcessSettings import *


s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")


class TestSQSInterface(TestCase):
    def setUp(self) -> None:
        self.sqs_interface = SQSInterface(s3_set2,'unitTest')
