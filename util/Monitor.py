import json
import enum
import threading
import prometheus_client

from util.Logger import Logger
from util.ListUtil import ListUtil
from util.StringUtil import StringUtil
from model.dao.ConfigurationDAO import ConfigurationDAO

class MetricType(enum.Enum):
   GAUGE = 1
   COUNTER = 2

class Metric(object):
    def __init__(self, name=None, description=None, type=None, labels=None, value=0.0):
        self.name = name
        self.description = description
        self.type = type
        self.labels = labels
        self.value = value

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getDescription(self):
        return self.description
    
    def setDescription(self, description):
        self.description = description
    
    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getLabels(self):
        return self.labels
  
    def setLabels(self, labels):
        self.labels = labels

    def getValue(self):
        return self.value
  
    def setValue(self, value):
        self.value = value
   
    def __str__(self):
        return StringUtil.clean( json.dumps(self.__dict__) )

class Monitor(object):
    __instance = None
    __mutexGetInstance = threading.Lock()
    
    def __init__(self):
        self.__metrics = dict()
        self.__properties = ConfigurationDAO( 'ApiGatewayMonitoring' )
        self.__mutexSave = threading.Lock()
        self.__mutexFindByName = threading.Lock()
        self.__mutexDelete = threading.Lock()
        self.__mutexDeleteAll = threading.Lock()
        port = StringUtil.toInt( self.__properties.get('port') )
        prometheus_client.start_http_server( port )
        Monitor.__instance = self

    @staticmethod
    def getInstance():
        Monitor.__mutexGetInstance.acquire()

        if Monitor.__instance == None: Monitor()
        
        Monitor.__mutexGetInstance.release()
        return Monitor.__instance

    def save(self, metric):
        self.__mutexSave.acquire()

        if metric == None: 
            self.__mutexSave.release()
            return None

        name = StringUtil.clean( metric.getName() )
        description = StringUtil.clean( metric.getDescription() )
        type = MetricType.GAUGE if metric.getType() == None else metric.getType()
        labels = ListUtil.getNoneAsEmpty( metric.getLabels() )
        labelNames = ListUtil.toTuple([ name for ( name, _ ) in labels ])
        value = StringUtil.toFloat( metric.getValue() )

        savedMetric = self.__metrics.get(name, None)
        if( savedMetric == None and type == MetricType.GAUGE ):
            savedMetric = prometheus_client.Gauge(name, description, labelNames)
        if( savedMetric == None and type == MetricType.COUNTER ):
            savedMetric = prometheus_client.Counter(name, description, labelNames)
        
        savedMetric._documentation = description

        if ListUtil.isEmpty(labels):
            savedMetric._value.set( value )        
        else:
            labels = ListUtil.toDict(labels)
            savedMetric.labels( labels )._value.set( value )

        self.__metrics[name] = savedMetric
        
        self.__mutexSave.release()
        return metric
    
    def findByName(self, name):
        self.__mutexFindByName.acquire()
        
        if name == None: 
            self.__mutexFindByName.release()
            return None
        
        metricSaved = self.__metrics.get(name, None)
        if metricSaved == None: 
            self.__mutexFindByName.release()
            return None

        metric = Metric()
        metric.setName( StringUtil.clean(name) )
        metric.setDescription( StringUtil.clean(metricSaved._documentation) )
        metric.setType( MetricType.GAUGE if isinstance(metricSaved, prometheus_client.Gauge) else MetricType.COUNTER )
        metric.setLabels( dict(zip(metricSaved._labelnames, metricSaved._labelvalues)) )
        metric.setValue( metricSaved._value.get() )
        
        self.__mutexFindByName.release()
        return metric
    
    def delete(self, metric):
        self.__mutexDelete.acquire()

        if metric == None:
            self.__mutexDelete.release()
            return
        
        name = StringUtil.clean( metric.getName() )
        metricSaved = self.__metrics.pop(name)
        metricSaved.remove()
        metricSaved.clear()

        REGISTRY.unregister( metricSaved )
        del( metricSaved )
        metricSaved = None

        self.__mutexDelete.release()
    
    def deleteAll(self, metrics=None):
        self.__mutexDeleteAll.acquire()

        metrics = self.__metrics.values() if metrics == None else metrics
        for metric in metrics: self.delete( metric )

        self.__mutexDeleteAll.release()