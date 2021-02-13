# API Gateway - Raspberry PI

Um API Gateway recebe todas as solicitações de API de um ou vários usuários, determinando e provendo de forma transparente serviços em rede.

O API Gateway no Raspberry PI recebe todas as chamadas de API dos Arduinos e as encaminha para o serviço apropriado fazendo uma tradução de protocolo entre MQTT e NGSIv2. 

# Utilizando o API Gateway
## Pré-Requisitos
+ Distribuição Linux Ubuntu
+ Python 3.X
+ [Mosquitto Broker](https://mosquitto.org/)
+ [Fiware Orion Broker](https://fiware-orion.readthedocs.io/en/master/index.html)

## Download
Para fazer o download, basta clonar o repositório git localmente em um local desejado.

## Instalação
Para fazer a instalação, basta executar o script `install.sh`.

## Configuração
Uma vez clonado e instalado, há um arquivo de configuração: `conf/apigateway.conf` . Dentro do arquivo de configuração, é possível configurar onde entrará cada uma das filas utilizadas
pelo API Gateway, a saber: fila request, e fila response. Ambas as filas podem estar dentro de um mesmo broker, ou em brokers diferentes. Basta configurar o IP e a porta de funcionamento. O terceiro item presente é o local onde está instalado o Fiware-Orion-Context Broker, utilizado para armazenar as informações enviado pelo Arduino e redirecionado pelo Raspberry PI.

## Execução
Para executar o programa, basta entrar no diretório clonado, e executar o seguinte comando:

`python3 ApiGatewayApplication.py`

## Mensagem
### Request

Abaixo está o formato de envio de uma requisição de enviado pelo Arduino. Os campos podem ser entendidos da seguinte forma:
+ replyHost: em qual endereco do broker deve ser enviado a resposta da requisicao;
+ replyPort: em qual porta o broker que receberá a mensagem de resposta atende;
+ replyChannel: em qual fila do broker receberá a mensagem;
+ method: o método HTTP que a [API do Fiware-Orion-Broker](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html) receberá. Nesse caso, pode ser:
    + **GET**: Para recuperação das informações presentes do Fiware-Orion-Broker
    + **POST**: Para criacao de recurso novas informações
    + **PATCH**: Para atualização de recursos
    + **DELETE** Para exclusão de recursos.
+ uri: a URI que o Fiware-Orion-Broker atenderá
+ body: O corpo da mensagem que deve ser ou não enviado para a URI anteriormente definida.

    	{
			"replyHost": "192.168.2.6", 
			"replyPort": 1883, 
			"replyChannel": "arduino", 
			"method": "POST", 
			"uri": "/v2/entities", 
			"header": {}, 
			"body": {
				"id": "waterQualityObserved-Arduino-2457163", 
				"type": "WaterQualityObserved", 
				"dateObserved": { 
					"type": "DateTime", 
					"value": "2019-08-29T14:56:24.571630"
				},
				"temperature": { 
					"value": 38
				},
				"NO3": {
					"value": 76
				},
				"location": {
					"type": "geo:json",
					"value": { 
						"type": "Point",
						"coordinates": [34, 41]
					}
				},
				"pH": {
					"value": 57
				},
				"measurand": {
					"value": ["NO3, 0.01, M1, Concentration of Nitrates"]}, 
					"conductivity": {
						"value": 101
		    		}
			}
		}

### Response
Abaixo está o formato de resposta de uma requisição de enviado pelo Arduino. Os campos podem ser entendidos da seguinte forma:
+ versionProtocol: qual o protocolo de resposta do Fiware-Orion-Broker, isto é, HTTP/1.0 ou HTTP/1.1.
+ statusCode: o código de resposta HTTP enviada pelo Fiware Orion Broker.
+ statusMessage: a mensagem de resposta HTTP enviada pelo Fiware Orion Broker.
+ header: é um dicionário com o cabeçalho de resposta HTTP enviada pelo Fiware Orion Broker.
+ body: o corpo da mensagem de resposta que pode conter informações ou não.

        {
            "versionProtocol": "HTTP/1.1",
            "statusCode": 200, 
            "statusMessage": "OK", 
            "header": {
                "Connection": "Keep-Alive", 
                "Content-Length": "11402", 
                "Content-Type": "application/json", 
                "Fiware-Correlator": "0a5a5f40-ca87-11e9-b648-0242ac110003", 
                "Date": "Thu, 29 Aug 2019 18:01:35 GMT"
            },
            "body": [
                {
                    "id":"waterQualityObserved:Arduino:54648.648",
                    "type":"WaterQualityObserved",
                    "NO3": {
                        "type":"Number",
                        "value":74,
                        "metadata":{}
                    },
                    "conductivity":{
                        "type":"Number",
                        "value":61,
                        "metadata":{}
                    },
                    "dateObserved":{
                        "type":"DateTime",
                        "value":"2019-08-22T17:05:54.00Z",
                        "metadata":{}
                    },
                    "location":{
                        "type":"geo:json",
                        "value":{
                            "type":"Point",
                            "coordinates":[80,4]
                        },
                        "metadata":{}
                    },
                    "measurand":{
                        "type":"StructuredValue",
                        "value":["NO3, 0.01, M1, Concentration of Nitrates"],
                        "metadata":{}
                    },
                    "pH": {
                        "type":"Number",
                        "value":41,
                        "metadata":{}
                    },
                    "temperature":{
                        "type":"Number",
                        "value":33,
                        "metadata":{}
                    }
                }
            ]
        }