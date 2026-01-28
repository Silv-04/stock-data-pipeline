resource "aws_glue_crawler" "sales_crawler" {
  name          = "jl-sales-crawler"
  database_name = "sales"
  role          = var.glue_role_name

  s3_target {
    path = "s3://${var.raw_bucket}/"
  }

  table_prefix = "raw_"
  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "LOG"
  }
}

resource "aws_glue_crawler" "stock_crawler" {
  name          = "jl-stock-crawler"
  database_name = "sales"
  role          = var.glue_role_name

  s3_target {
    path = "s3://${var.analytics_bucket}/stock_risk/"
  }

  table_prefix = "stock_"
  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "LOG"
  }
}
