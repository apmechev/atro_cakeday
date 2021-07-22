resource "aws_apigatewayv2_api" "submit_cake" {
  name          = local.api_gateway_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "submit_stage" {
  api_id = aws_apigatewayv2_api.submit_cake.id

  name        = local.api_gateway_stage_name
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

  integration_uri    = module.process_lambda.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"

  depends_on = [module.process_lambda]
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.process_lambda.name
  principal     = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.submit_cake.execution_arn}/*/*"

  depends_on = [module.process_lambda]
}