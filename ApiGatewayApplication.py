import sys

from consumer.MosquittoConsumer import MosquittoConsumer
from consumer.monitoring.MonitoringMosquittoConsumer import MonitoringMosquittoConsumer
from consumer.logging.LoggingMosquittoConsumer import LoggingMosquittoConsumer
from consumer.handling.ExceptionHandlingMosquittoConsumer import ExceptionHandlingMosquittoConsumer

from consumer.CoatiConsumer import CoatiConsumer
from consumer.monitoring.MonitoringCoatiConsumer import MonitoringCoatiConsumer
from consumer.logging.LoggingCoatiConsumer import LoggingCoatiConsumer
from consumer.handling.ExceptionHandlingCoatiConsumer import ExceptionHandlingCoatiConsumer

from proxy.FiwareOrionProxy import FiwareOrionProxy
from proxy.monitoring.MonitoringFiwareOrionProxy import MonitoringFiwareOrionProxy
from proxy.logging.LoggingFiwareOrionProxy import LoggingFiwareOrionProxy
from proxy.handling.ExceptionHandlingFiwareOrionProxy import ExceptionHandlingFiwareOrionProxy

from consumer.RequestConsumer import RequestConsumer
from consumer.monitoring.MonitoringResponseConsumer import MonitoringResponseConsumer
from consumer.logging.LoggingResponseConsumer import LoggingResponseConsumer
from consumer.handling.ExceptionHandlingResponseConsumer import ExceptionHandlingResponseConsumer

from consumer.ResponseConsumer import ResponseConsumer
from consumer.monitoring.MonitoringRequestConsumer import MonitoringRequestConsumer
from consumer.logging.LoggingRequestConsumer import LoggingRequestConsumer
from consumer.handling.ExceptionHandlingRequestConsumer import ExceptionHandlingRequestConsumer

from producer.ResponseProducer import ResponseProducer
from producer.monitoring.MonitoringResponseProducer import MonitoringResponseProducer
from producer.logging.LoggingResponseProducer import LoggingResponseProducer
from producer.handling.ExceptionHandlingResponseProducer import ExceptionHandlingResponseProducer

from repository.RequestRepository import RequestRepository
from repository.monitoring.MonitoringRequestRepository import MonitoringRequestRepository
from repository.logging.LoggingRequestRepository import LoggingRequestRepository
from repository.handling.ExceptionHandlingRequestRepository import ExceptionHandlingRequestRepository

from service.IoTService import IoTService
from service.monitoring.MonitoringIoTService import MonitoringIoTService
from service.logging.LoggingIoTService import LoggingIoTService
from service.handling.ExceptionHandlingIoTService import ExceptionHandlingIoTService

from service.FiwareOrionService import FiwareOrionService
from service.monitoring.MonitoringFiwareOrionService import MonitoringFiwareOrionService
from service.logging.LoggingFiwareOrionService import LoggingFiwareOrionService
from service.handling.ExceptionHandlingFiwareOrionService import ExceptionHandlingFiwareOrionService

from service.RequestService import RequestService
from service.monitoring.MonitoringRequestService import MonitoringRequestService
from service.logging.LoggingRequestService import LoggingRequestService
from service.handling.ExceptionHandlingRequestService import ExceptionHandlingRequestService

from service.ResponseService import ResponseService
from service.monitoring.MonitoringResponseService import MonitoringResponseService
from service.logging.LoggingResponseService import LoggingResponseService
from service.handling.ExceptionHandlingResponseService import ExceptionHandlingResponseService


class ApiGatewayApplication(object):
    def main(self):
        iotService = IoTService()
        iotService = LoggingIoTService( iotService )
        iotService = MonitoringIoTService( iotService )
        iotService = ExceptionHandlingIoTService( iotService )

        fiwareOrionProxy = FiwareOrionProxy()
        fiwareOrionProxy = LoggingFiwareOrionProxy( fiwareOrionProxy )
        fiwareOrionProxy = MonitoringFiwareOrionProxy( fiwareOrionProxy )
        fiwareOrionProxy = ExceptionHandlingFiwareOrionProxy( fiwareOrionProxy )

        responseProducer = ResponseProducer()
        responseProducer = LoggingResponseProducer( responseProducer )
        responseProducer = MonitoringResponseProducer( responseProducer )
        responseProducer = ExceptionHandlingResponseProducer( responseProducer )

        requestRepository = RequestRepository()
        requestRepository = LoggingRequestRepository( requestRepository )
        requestRepository = MonitoringRequestRepository( requestRepository )
        requestRepository = ExceptionHandlingRequestRepository( requestRepository )

        fiwareOrionService = FiwareOrionService( fiwareOrionProxy, responseProducer )
        fiwareOrionService = LoggingFiwareOrionService( fiwareOrionService )
        fiwareOrionService = MonitoringFiwareOrionService( fiwareOrionService )
        fiwareOrionService = ExceptionHandlingFiwareOrionService( fiwareOrionService )

        requestService = RequestService( requestRepository, fiwareOrionService )
        requestService = LoggingRequestService( requestService )
        requestService = MonitoringRequestService( requestService )
        requestService = ExceptionHandlingRequestService( requestService )

        responseService = ResponseService( requestService, iotService )
        responseService = LoggingResponseService( responseService )
        responseService = MonitoringResponseService( responseService )
        responseService = ExceptionHandlingResponseService( responseService )

        responseConsumer = ResponseConsumer( responseService )
        responseConsumer = LoggingResponseConsumer( responseConsumer )
        responseConsumer = MonitoringResponseConsumer( responseConsumer )
        responseConsumer = ExceptionHandlingResponseConsumer( responseConsumer )
        
        requestConsumer = RequestConsumer( requestService )
        requestConsumer = LoggingRequestConsumer( requestConsumer )
        requestConsumer = MonitoringRequestConsumer( requestConsumer )
        requestConsumer = ExceptionHandlingRequestConsumer( requestConsumer )

        mosquittoConsumer = MosquittoConsumer()
        mosquittoConsumer = LoggingMosquittoConsumer( mosquittoConsumer )
        mosquittoConsumer = MonitoringMosquittoConsumer( mosquittoConsumer )
        mosquittoConsumer = ExceptionHandlingMosquittoConsumer( mosquittoConsumer )

        coatiConsumer = CoatiConsumer()
        coatiConsumer = LoggingCoatiConsumer( coatiConsumer )
        coatiConsumer = MonitoringCoatiConsumer( coatiConsumer )
        coatiConsumer = ExceptionHandlingCoatiConsumer( coatiConsumer )

        coatiConsumer.consume()
        requestConsumer.consume()
        responseConsumer.consume()
        mosquittoConsumer.consume()
        

if __name__ == "__main__":
    apiGatewayApplication = ApiGatewayApplication()
    apiGatewayApplication.main()