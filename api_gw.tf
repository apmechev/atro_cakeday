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
