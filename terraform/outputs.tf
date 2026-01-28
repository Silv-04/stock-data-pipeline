output "raw_bucket" {
  value = var.raw_bucket
}

output "analytics_bucket" {
  value = var.analytics_bucket
}

output "kinesis_stream_name" {
  value = aws_kinesis_stream.sales_stream.name
}
