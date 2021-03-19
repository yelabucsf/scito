# SCITO-seq: single-cell combinatorial indexed cytometry sequencing

Package to deploy on serverless Lambda. Potentially containerized.

## Structure of serverless counting pipeline (SCITO-count)  
0. User uploads data to S3 before any processing takes place.
1. User creates a config file and pushes it to S3.
2. **Lambda 1:** Receives an S3 event. Splits FASTQ files in 1Gb chunks. Creates SQS queue and sends byte ranges there.   
   Creates **Lambda 2**.  
   Creates a 0 Byte *composite trigger* file with a process name in S3. *Composite trigger* should be **12 bytes** to 
   trigger **Lambda 3**.
3. **Lambda 2:** concurrent lambda. SQS triggers download of a byte range and creation of the "content table" of inflatable
   BGZF chunks. Monitors SQS depth. If no messages, SQS is destroyed and **Lambda 3** is invoked.
4. **Lambda 3:** Destroys all instances of **Lambda 2**. Pulls content tables describing BGZF blocks of FASTQ files for 
   each read-file for the sample. Combines them and deduplicates.  
   This process creates a single content table for each read FASTQ file. The content ables are going through series of 
   binary splits generating a catalog of inflatable BGZF chunks of roughly similar number of FASTQ blocks (each block is
   a 4-line FASTQ entry). Each entry of a catalog is a group of BGZF chunks and is represented by start byte offset of 
   the first chung of the group and the end offset of the last chunk of the group.
   Also a new SQS and **Lambda 4** are created. SQS receives messages with byte offsets.
5. **Lambda 4:** concurrent lambda. SQS triggers download of a byte range of FASTQ files (based on the offset catalog)
   multiple-read FASTQ files are synchronized to match the read pairs. Then it constructs BUS files (filter, deduplicate)
   and outputs them to EFS. Then it monitors SQS depth and terminates SQS if no messages are left. Then invokes **Lambda 5**.
6. **Lambda 5**. Merges all BUS files (filter deduplicate) and creates a count matrix. Outputs it to S3.
