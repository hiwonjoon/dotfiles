#!/bin/bash

install_essential_packages() {
    local -a packages; packages=( \
        build-essential \
        vim zsh curl \
        python-software-properties software-properties-common \
        cmake cmake-data ctags \
        terminator htop \
        silversearcher-ag \
        openssh-server mosh \
        )

    sudo apt-get install -y ${packages[@]}
}

install_ppa_git() {
    # https://launchpad.net/~git-core/+archive/ubuntu/ppa
    sudo add-apt-repository -y ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install -y git-all git-extras
}

install_ppa_tmux() {
    # https://launchpad.net/~pi-rho/+archive/ubuntu/dev
    sudo add-apt-repository -y ppa:pi-rho/dev
    sudo apt-get update
    sudo apt-get install -y tmux
}

install_ppa_nginx() {
    # https://launchpad.net/~nginx/+archive/ubuntu/stable
    sudo add-apt-repository -y ppa:nginx/stable
    sudo apt-get update
    sudo apt-get install -y nginx
}

install_neovim() {
    sudo add-apt-repository -y ppa:neovim-ppa/unstable
    sudo apt-get update
    sudo apt-get install -y neovim
    sudo /usr/bin/pip install neovim
    sudo /usr/bin/pip3 install neovim
}

install_all() {
    # TODO dependency management: duplicated 'apt-get update'?
    install_essential_packages
    install_ppa_tmux
    install_ppa_git
    install_ppa_nginx
}

install_python_settings() {
    sudo apt-get install python-dev
    sudo apt-get install python-pip python-virtualenv
    sudo pip install virtualenvwrapper
}

install_nvidia_drivers() {
    sudo add-apt-repository ppa:graphics-drivers/ppa
    sudo apt-get update && sudo apt-get install nvidia-352
}

install_java() {
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java8-installer
}

# entrypoint script
if [ `uname` != "Linux" ]; then
    echo "Run on Linux (not on Mac OS X)"; exit 1
fi
if [ -n "$1" ]; then
    $1
else
    echo "Usage: $0 [command], where command is one of the following:"
    declare -F | cut -d" " -f3
fi
