from scito_count.S3BlockSplit import *

# Trigger - with pattern "split"
s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "FULL R2 UPLOAD TEST")
fileR1 = S3BlockSplit(s3_set)
fileR1.generate_blocks()