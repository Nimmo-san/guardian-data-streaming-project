resource "aws_s3_bucket" "ingestion_bucket" {
    bucket_prefix = "${var.ingestion_bucket_prefix}"
    tags = {
      name = "ingestion_bucket"
    }
}