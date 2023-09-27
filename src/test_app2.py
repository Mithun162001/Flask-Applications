from flask import Flask, render_template, request, redirect, url_for, flash
import paramiko
import os

app = Flask(__name__)
@app.route('/test-ssh', methods=['GET'])
def test_ssh():
    username = 'root'
    password = '162001'
    ip_address = '172.23.226.203'

    ssh_client = ssh_connect(username, password, ip_address)

    if ssh_client:
        print('SSH Connection Successful')
    else:
        return 'SSH Connection Failed'
