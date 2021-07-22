module "process_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.7.0"

  function_name = local.lambda_function_name
  description   = "The Lambda function that creates the ical files"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  environment_variables = {
    "SECRET_KEY" : var.SECRET_KEY,
    "BAKERY_BUCKET_NAME" : aws_s3_bucket.bakery_bucket.id
  }
  memory_size = 1024
  source_path = "./lambdas/cakedays_process/"

  layers = ["arn:aws:lambda:eu-central-1:311504692153:layer:cakedays_space_v1:7",
  "arn:aws:lambda:eu-central-1:292169987271:layer:AWSLambda-Python38-SciPy1x:29"]

  policy_json = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect   = "Allow",
          Action   = "s3:PutObject",
          Resource = "${aws_s3_bucket.bakery_bucket.arn}/*"
        }
      ]
    }
  )
  attach_policy_json = true

}

output "bakery_bucket_arn" {
  value = aws_s3_bucket.bakery_bucket.arn
}