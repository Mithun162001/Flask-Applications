from flask import Flask, render_template, request, redirect, url_for, flash
import os
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Function to establish an SSH connection to the remote server
def ssh_connect(username, password, ip_address):
    try:
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        return ssh_client
    except Exception as e:
        flash(f"Failed to connect to the remote server: {str(e)}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/connect', methods=['POST'])
def connect():
    ip_address = request.form.get('ip_address')
    return render_template('login.html', ip_address=ip_address)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_address = request.form.get('ip_address')

    ssh_client = ssh_connect(username, password, ip_address)

    if ssh_client:
        return render_template('upload.html', ip_address=ip_address, username=username, password=password)
    else:
        return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload():
    ip_address = request.form.get('ip_address')
    username = request.form.get('username')
    password = request.form.get('password')
    file = request.files['file']

    if file:
        # Save the uploaded file to a temporary location
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Perform file transfer to the remote server using the SSH connection
        ssh_client = ssh_connect(username, password, ip_address)
        if ssh_client:
            sftp = ssh_client.open_sftp()
            sftp.put(file_path, f'/root/{file.filename}')
            sftp.close()
            os.remove(file_path)  # Remove the temporary file
            flash("File upload successful!")
        else:
            flash("File upload failed. Unable to connect to the remote server.")
    else:
        flash("No file selected for upload.")

    return render_template('upload.html', ip_address=ip_address)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home2():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)