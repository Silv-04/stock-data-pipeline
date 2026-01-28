resource "aws_kinesis_stream" "sales_stream" {
  name        = "jl-sales-stream"
  shard_count = 1
}
