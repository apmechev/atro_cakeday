module "process_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.4.0"

  function_name = local.lambda_function_name
  description   = "The Lambda function that creates the ical files"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  source_path = "./lambdas/cakedays_process/"

  }