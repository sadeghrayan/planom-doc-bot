#!/bin/bash 

# Install docker requirements 
function docker_install(){
    echo "Installing docker ..." 
    chmod +x ./Scripts/docker_install.sh 
    bash ./Scripts/docker_install.sh 
    echo "Docker installation completed!" 
}

# Install Ollama Server
function ollama_install(){
echo "Installing Ollama Server ..." 
chmod +x ./Scripts/ollama.sh
bash ./Scripts/ollama.sh
#curl -fsSL https://ollama.com/install.sh | sh
echo "Downloading tinyllama model ..."
ollama pull tinyllama
echo "Ollama Server installation completed!" 
}

# Install Elastic Stack 
function elastic_install(){
    echo "Installing Elastic Stack ..."
    chmod +x ./Elastic/crack_and_install.sh
    bash ./Elastic/crack_and_install.sh
    echo "Elastic Stack installation completed!"
}

function chatbot_install(){
    echo "Installing Chatbot ..."
    echo "Building Docker file ..."
    docker build -f ./chatbot-rag-app/Dockerfile -t chatbot-rag-app ./chatbot-rag-app
    echo "Ingesting data ..."
    docker run --rm --env-file ./chatbot-rag-app/.env chatbot-rag-app flask create-index 
    echo "Running chat system ..." 
    docker run --rm -p 4000:4000 --env-file ./chatbot-rag-app/.env -d chatbot-rag-app 
}

function chatbot_run(){
    echo "Running chat system ..." 
    docker run --rm -p 4000:4000 --env-file ./chatbot-rag-app/.env -d chatbot-rag-app 
}

function webserver_install(){
    echo "Building Docker file ..."
    docker build -t nginx ./Nginx 
    echo "Running nginx image ..."
    docker run --env-file ./Nginx/.env -d -p 80:80 -p 443:443 --name nginx-chat nginx 

}

function show_menu(){
    echo "Please select from the list"
    echo "1) Full Installation (Not Available)"
    echo "2) Install docker" 
    echo "3) Install Ollama server"
    echo "4) Install Elastic Stack" 
    echo "5) Install Chatbot"
    echo "5.1) Just run Chatbot"
    echo "6) Install Webserver"
    echo "7) Exit"
    echo -n "Enter your choice: "
    read choice
}
    
while true; do
    show_menu
    case $choice in
        2) docker_install;;
        3) ollama_install;;
        4) elastic_install;;
        5) chatbot_install;;
        5.1) chatbot_run;;
        6) webserver_install;;
        7) echo "Goodbye!"; exit 0;;
        *) echo "Invalid choise, please try again.";;
    esac
    echo ""
done     