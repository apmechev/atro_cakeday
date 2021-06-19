module "process_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.4.0"

  function_name = local.lambda_function_name
  description   = "The Lambda function that creates the ical files"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  environment_variables = {
    "SECRET_KEY": var.SECRET_KEY
  }
  memory_size  = 1024
  source_path = "./lambdas/cakedays_process/"
 
  layers =["arn:aws:lambda:eu-central-1:311504692153:layer:cakedays_space_v1:7",
           "arn:aws:lambda:eu-central-1:292169987271:layer:AWSLambda-Python38-SciPy1x:29"]

  }