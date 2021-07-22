resource "aws_apigatewayv2_api" "submit_cake" {
  name          = local.api_gateway_name
  protocol_type = "HTTP"
}