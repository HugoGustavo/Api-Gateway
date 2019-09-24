# Instalando dependencias
# sudo apt update
# sudo apt-get -y install mosquitto
# sudo apt-get -y install openvpn
# sudo apt-get -y install python3-pip
# sudo apt-get -y install sqlite3
# pip3 install paho-mqtt 


#Configurando arquivo de inicializacao automatica
echo "#!/bin/bash" > gateway.sh
echo "service mosquitto start" >> gateway.sh
echo "openvpn --config /usr/bin/api-gateway/conf/client.ovpn --daemon openvpn-gateway" >> gateway.sh
echo "nohup /usr/bin/python3 /usr/bin/api-gateway/ApiGatewayApplication.py 2>/dev/null &" >> gateway.sh
sudo chmod +x gateway.sh

# Criando o servico
echo "[Unit]" > gateway.service
echo "Description=Gateway service" >> gateway.service
echo "" >> gateway.service
echo "[Service]" >> gateway.service
echo "Type=simple" >> gateway.service
echo "ExecStart=/usr/bin/python3 /usr/bin/api-gateway/ApiGatewayApplication.py" >> gateway.service
echo "" >> gateway.service
echo "[Install]" >> gateway.service
echo "WantedBy=multi-user.target" >> gateway.service
sudo cp -ra gateway.service /etc/systemd/system/gateway.service
sudo chmod 644 /etc/systemd/system/gateway.service
sudo systemctl enable gateway

# Permissao para criar nohup da aplicacao
sudo chmod +x ApiGatewayApplication.py

#Copiando arquivos para /usr/bin/
sudo rm -rf /usr/bin/api-gateway
sudo mkdir /usr/bin/api-gateway
sudo cp -ra * /usr/bin/api-gateway
sudo chown -R root:root /usr/bin/api-gateway

# Apagando arquivos temporarios
rm -rf gateway.service
rm -rf gateway.sh
