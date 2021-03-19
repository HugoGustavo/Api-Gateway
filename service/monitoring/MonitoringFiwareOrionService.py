import time
import psutil
import requests

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.FiwareOrionService import FiwareOrionService

class MonitoringFiwareOrionService(object):
    def __init__(self, service):
        self.__service = service


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

        startUploadDownload = psutil.net_io_counters(pernic=True)['eth0']
        start = time.time()
        self.__service.read(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)['eth0']

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
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

        startUploadDownload = psutil.net_io_counters(pernic=True)['eth0']
        start = time.time()
        self.__service.create(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)['eth0']

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
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

        startUploadDownload = psutil.net_io_counters(pernic=True)['eth0']
        start = time.time()
        self.__service.update(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)['eth0']

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
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

        startUploadDownload = psutil.net_io_counters(pernic=True)['eth0']
        start = time.time()
        self.__service.delete(request)
        end = time.time()
        endUploadDownload = psutil.net_io_counters(pernic=True)['eth0']

        metric = Monitor.getInstance().findByName( 'app_upload_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_upload_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_download_fiware_orion_bytes_seconds' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_download_fiware_orion_bytes_seconds' )
        metric.setDescription( 'Network throughout to Fiware Orion Broker in bytes per seconds' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        value = ( endUploadDownload[0] - startUploadDownload[0] ) / ( end - start )
        if ( value != 0.0 ): metric.setValue( value )
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