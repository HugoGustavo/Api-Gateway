from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from repository.RequestRepository import RequestRepository

class MonitoringRequestRepository(object):
    def __init__(self, repository):
        self.__repository = repository


    def connect(self):
        result = self.__repository.connect()

        metric = Monitor.getInstance().findByName( 'app_sqlite_avaliable_info' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_sqlite_avaliable_info' )
        metric.setDescription( 'SQLite is available' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        metric.setValue( 1 if self.isConnected() else 0 )
        Monitor.getInstance().save( metric )

        return result


    def isConnected(self):
        result = self.__repository.isConnected()
        
        return result


    def disconnect(self):
        result = self.__repository.disconnect()
        
        return result


    def commit(self):
        result = self.__repository.commit()

        return result


    def save(self, request):
        result = self.__repository.save( request )
        
        return result


    def findById(self, id):
        result = self.__repository.findById( id )
        
        return result
