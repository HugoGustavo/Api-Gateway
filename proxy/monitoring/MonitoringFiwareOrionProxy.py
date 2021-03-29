import time
import psutil

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.Monitor import MetricType
from proxy.logging.LoggingFiwareOrionProxy import LoggingFiwareOrionProxy

class MonitoringFiwareOrionProxy(object):
    def __init__(self, fiwareOrionProxy):
        self.__fiwareOrionProxy = fiwareOrionProxy


    def read(self, request):
        request.setDepartureTime( time.time() )
        
        metric = Monitor.getInstance().findByName( 'app_http_get_request_processing_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_get_request_processing_seconds_total' )
        metric.setDescription( 'Total GET request processing time' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = request.getDepatureTime() - request.getArriveTime()
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        startUploadDownload = psutil.net_io_counters(pernic=True)
        start = time.time()
        self.__fiwareOrionProxy.read(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network upload throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][0] - startUploadDownload[nic][0] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network download throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][1] - startUploadDownload[nic][1] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_get_fiware_orion_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_get_fiware_orion_seconds_total' )
        metric.setDescription( 'Round-Trip Time (RTT) total for HTTP GET to Fiware Orion Broker in seconds' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = end - start
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_get_fiware_orion_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_get_fiware_orion_success_total' )
        metric.setDescription( 'Total number HTTP GET successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1)
        Monitor.getInstance().save( metric )


    def create(self, request):
        request.setDepartureTime( time.time() )

        metric = Monitor.getInstance().findByName( 'app_http_post_request_processing_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_post_request_processing_seconds_total' )
        metric.setDescription( 'Total POST request processing time' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = request.getDepartureTime() - request.getArriveTime()
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        startUploadDownload = psutil.net_io_counters(pernic=True)
        start = time.time()
        self.__fiwareOrionProxy.create(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network upload throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][0] - startUploadDownload[nic][0] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network download throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][1] - startUploadDownload[nic][1] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )


        metric = Monitor.getInstance().findByName( 'app_http_post_fiware_orion_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_post_fiware_orion_seconds_total' )
        metric.setDescription( 'Round-Trip Time (RTT) total for HTTP POST to Fiware Orion Broker in seconds' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = end - start
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_post_fiware_orion_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_post_fiware_orion_success_total' )
        metric.setDescription( 'Total number HTTP POST successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1)
        Monitor.getInstance().save( metric )
    
    def update(self, request):
        request.setDepartureTime(time.time())

        metric = Monitor.getInstance().findByName( 'app_patch_request_processing_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_patch_request_processing_seconds_total' )
        metric.setDescription( 'Total PATCH request processing time' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = request.getDepatureTime() - request.getArriveTime()
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        startUploadDownload = psutil.net_io_counters(pernic=True)
        start = time.time()
        self.__fiwareOrionProxy.update(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network upload throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][0] - startUploadDownload[nic][0] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network download throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload.keys() ]
        labels = [ ( nic, ( endUploadDownload[nic][1] - startUploadDownload[nic][1] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_patch_fiware_orion_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_patch_fiware_orion_seconds_total' )
        metric.setDescription( 'Round-Trip Time (RTT) total for HTTP PATCH to Fiware Orion Broker in seconds' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_patch_fiware_orion_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_patch_fiware_orion_success_total' )
        metric.setDescription( 'Total number HTTP PATCH successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1)
        Monitor.getInstance().save( metric )


    def delete(self, request):
        request.setDepartureTime( time.time() )

        metric = Monitor.getInstance().findByName( 'app_delete_request_processing_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_delete_request_processing_seconds_total' )
        metric.setDescription( 'Total DELETE request processing time' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = request.getDepatureTime() - request.getArriveTime()
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        startUploadDownload = psutil.net_io_counters(pernic=True)
        start = time.time()
        self.__fiwareOrionProxy.delete(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network upload throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][0] - startUploadDownload[nic][0] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network download throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        labels = [ nic for nic in endUploadDownload ]
        labels = [ ( nic, ( endUploadDownload[nic][1] - startUploadDownload[nic][1] ) / ( end - start ) ) for nic in labels ]
        metric.setLabels( labels )    
        metric.setValue( 1.0 )
        Monitor.getInstance().save( metric )
        
        metric = Monitor.getInstance().findByName( 'app_http_delete_fiware_orion_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_delete_fiware_orion_seconds_total' )
        metric.setDescription( 'Round-Trip Time (RTT) total for HTTP DELETE to Fiware Orion Broker in seconds' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = end - start
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_http_delete_fiware_orion_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_http_delete_fiware_orion_success_total' )
        metric.setDescription( 'Total number HTTP DELETE successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1)
        Monitor.getInstance().save( metric )