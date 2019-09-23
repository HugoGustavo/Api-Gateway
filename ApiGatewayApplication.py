import sys
from consumer.RequestConsumer import RequestConsumer
from consumer.ResponseConsumer import ResponseConsumer

class ApiGatewayApplication(object):
    def main(self):
        requestConsumer = RequestConsumer()
        responseConsumer = ResponseConsumer()
        requestConsumer.consume()
        responseConsumer.consume()

if __name__ == "__main__":
    apiGatewayApplication = ApiGatewayApplication()
    apiGatewayApplication.main()