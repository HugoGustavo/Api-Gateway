import sys
from consumer.RequestConsumer import RequestConsumer
from consumer.ResponseConsumer import ResponseConsumer
from service.ArduinoService import ArduinoService

class ApiGatewayApplication(object):
    def main(self):
        arduinoService = ArduinoService()        
        requestConsumer = RequestConsumer()
        responseConsumer = ResponseConsumer()
        
        arduinoService.consume()
        requestConsumer.consume()
        responseConsumer.consume()

if __name__ == "__main__":
    apiGatewayApplication = ApiGatewayApplication()
    apiGatewayApplication.main()