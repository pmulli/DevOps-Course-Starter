Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  # Open a port (port forwarding)
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update

    # Install pyenv prerequisites
    sudo apt-get -y install libedit-dev
    sudo apt-get -y install libncurses5-dev
    sudo apt-get -y install gcc

    # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  
    echo 'export PYENV_ROOT="/vagrant/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'export PATH="/vagrant:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.profile
    source ~/.profile

    pyenv install 3.9.2
    pyenv global 3.9.2
    sudo apt-get -y install python3-distutils

    # Install poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    # Install dependencies and launch
    rm -R .venv
    sed -i 's/in-project = false/in-project = false/g' /vagrant/poetry.toml
    cd /vagrant;
    poetry install;
    nohup poetry run flask run --host 0.0.0.0 > logs.txt 2>&1 &
    "}
  end
end
