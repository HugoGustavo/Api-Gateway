# Instalando dependencias
sudo apt update
sudo apt-get -y install mosquitto
sudo apt-get -y install openvpn
sudo apt-get -y install python3-pip
sudo apt-get -y install sqlite3
pip3 install paho-mqtt

#Configurando arquivo de inicializacao automatica
echo "sudo openvpn --config $(pwd)/conf/client.ovpn --daemon openvpn-gateway" >> init.sh
echo "nohup python3 $(pwd)/ApiGatewayApplication.py &" >> init.sh
sudo cp -ra init.sh /etc/init.d/
sudo chmod 777 /etc/init.d/init.sh
sudo chown root:root /etc/init.d/init.sh

# Permissao para criar nohup da aplicacao
sudo chmod +x ApiGatewayApplication.py