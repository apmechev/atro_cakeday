resource "aws_apigatewayv2_api" "submit_cake" {
  name          = local.api_gateway_name
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["http://${local.frontend_bucket_name}", "https://${local.frontend_bucket_name}"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["access-control-allow-origin", "access-control-allow-headers", "content-type"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "submit_stage" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  name        = local.submit_stage_name
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      requestTime             = "$context.requestTime"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.submit_cake.name}"

  retention_in_days = 30
}

resource "aws_apigatewayv2_route" "bake_cake" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  route_key = "POST /bake"
  target    = "integrations/${aws_apigatewayv2_integration.bake_cake.id}"
}

resource "aws_apigatewayv2_integration" "bake_cake" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  integration_uri    = module.process_lambda.lambda_function_invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"

}

resource "aws_apigatewayv2_route" "bake_cake_OPTIONS" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  route_key = "OPTIONS /bake"
  target    = "integrations/${aws_apigatewayv2_integration.bake_cake.id}"
}

resource "aws_apigatewayv2_integration" "bake_cake_OPTIONS" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  integration_uri    = module.process_lambda.lambda_function_invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"

}
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.process_lambda.lambda_function_name

  principal  = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.submit_cake.execution_arn}/*/*"
}
