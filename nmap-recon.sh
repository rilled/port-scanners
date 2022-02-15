#!/bin/bash
DIR=${HOME}/recon

entry() {
    dependsCheck
    read -p "Target IP: " ip
    read -p "Target Name: " name
    echo "Running recon on ${ip} (${name})"
    mkdir -p ${DIR}/${name}
    echo "[recon] Created dir ~/${DIR}/${name}"
    echo "[recon] Starting scans!"
    nmap -sP ${ip} > ${DIR}/${name}/live
    echo "[recon] (1/3) Live server scan complete: ${DIR}/${name}/live"
    sudo nmap -O ${ip} > ${DIR}/${name}/open
    echo "[recon] (2/3) Open port scan complete: ${DIR}/${name}/open"
    sudo nmap --script vuln ${ip} > ${DIR}/${name}/vulns
    echo "[recon] (3/3) Vulnerability detection complete: ${DIR}/${name}/vulns"
}

dependsCheck() {
    if dpkg -l python3-pip >/dev/null; then
        return
    else
        sudo apt install -y python3-pip
        sudo pip3 install protonvpn-cli
    fi
    if dpkg -i nmap >/dev/null; then
        return
    else
        sudo apt install -y nmap
    fi
    if dpkg -i x11-apps >/dev/null; then
        return
    else
        sudo apt install -y x11-apps
    fi
}

entry