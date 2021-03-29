from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from repository.RequestRepository import RequestRepository

class ExceptionHandlingRequestRepository(object):
    def __init__(self, requestRepository):
        self.__requestRepository = requestRepository


    def connect(self):
        result = None
        try:
            result = self.__requestRepository.connect()
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.connect'
            parameters = StringUtil.getNoneAsEmpty(None)
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result

    
    def isConnected(self):
        result = None
        try:
            result = self.__requestRepository.isConnected()
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.isConnected'
            parameters = StringUtil.getNoneAsEmpty(None)
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result


    def disconnect(self):
        result = None
        try:
            result = self.__requestRepository.disconnect()
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.disconnect'
            parameters = StringUtil.getNoneAsEmpty(None)
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

        return result


    def commit(self):
        result = None
        try:
            result = self.__requestRepository.commit()
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.commit'
            parameters = StringUtil.getNoneAsEmpty(None)
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result


    def save(self, request):
        result = None
        try:
            result = self.__requestRepository.save(request)
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.save'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean(request) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

        return result

    def findById(self, id):
        result = None
        try:
            result = self.__requestRepository.findById(id)
        
        except Exception as exception:
            classpath = 'repository.RequestRepository.findById'
            parameters = StringUtil.clean({ 'id' : StringUtil.clean(id) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER)
            metric.setValue( metric.getValue() + 1)
            Monitor.getInstance().save( metric )
        
        return result

