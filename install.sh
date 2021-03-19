installDependencies(){
    sudo apt update
    sudo apt-get -y install mosquitto
    sudo apt-get -y install openvpn
    sudo apt-get -y install python3-pip
    sudo apt-get -y install sqlite3
    sudo -H pip3 install prometheus-client
    sudo -H pip3 install paho-mqtt
    sudo -H pip3 install psutil
}

installApplication(){
    sudo rm -rf /usr/bin/api-gateway
    sudo mkdir /usr/bin/api-gateway
    sudo cp -ra * /usr/bin/api-gateway
    sudo chown -R root:root /usr/bin/api-gateway
}

createOpenVPNService(){
    sudo cp -ra client.ovpn /etc/openvpn/client.conf
    sudo systemctl enable openvpn@client.service
    sudo service openvpn@client start
}

createGatewayService(){
    echo "[Unit]" > gateway.service
    echo "Description=Gateway Service" >> gateway.service
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
    sudo systemctl start gateway
}

deleteTemporaryFiles(){
    rm -rf gateway.service
}

main(){
    installDependencies
    installApplication
    createOpenVPNService
    createGatewayService
    deleteTemporaryFiles
}

main