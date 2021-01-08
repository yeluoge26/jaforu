
sudo yum install -y curl && curl -sL https://rpm.nodesource.com/setup_12.x | sudo bash -

sudo yum install -y gcc-c++ make mongodb-org nodejs

sudo yum install -y epel-release && sudo yum install -y GraphicsMagick

sudo npm install -g inherits n && sudo n 12.18.4


curl -L https://releases.rocket.chat/latest/download -o /tmp/rocket.chat.tgz

tar -xzf /tmp/rocket.chat.tgz -C /tmp

cd /tmp/bundle/programs/server && npm install
sudo mv /tmp/bundle /opt/Rocket.Chat

sudo useradd -M rocketchat && sudo usermod -L rocketchat
sudo chown -R rocketchat:rocketchat /opt/Rocket.Chat
