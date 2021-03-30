from unittest import TestCase

record = {
    'body': {
        'section': 'adsf',
        'config': 'ljahsdf',
        'byte_range': f'{int(1e9)}-{int(2e9)}'
    }
}

class Test(TestCase):
    def setUp(self) -> None:
        self.record = record
        self.true_split_record = ''


    def test_true_split_record(self):
        self.fail()
