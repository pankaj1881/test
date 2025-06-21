from flask import Flask, jsonify
import os
import paramiko

app = Flask(__name__)

# === Configuration ===
SOURCE_FOLDER = r"data"  # Local Windows path
REMOTE_HOST = "13.233.137.66"
REMOTE_PORT = 22
REMOTE_USER = "ec2-user"
REMOTE_KEY_PATH = r"test.pem"
REMOTE_DEST_PATH = "/home/ec2-user/upload_files"
# if upload_files folder dont have permission to write then run this cmd -------------- chmod 755 ~/uploaded_file


@app.route('/upload', methods=['POST'])
def upload_static_folder():
    if not os.path.exists(SOURCE_FOLDER):
        return jsonify({"error": "Source folder does not exist"}), 400

    try:
        key = paramiko.RSAKey.from_private_key_file(REMOTE_KEY_PATH)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, port=REMOTE_PORT, username=REMOTE_USER, pkey=key)

        sftp = ssh.open_sftp()

        for root, dirs, files in os.walk(SOURCE_FOLDER):
            rel_path = os.path.relpath(root, SOURCE_FOLDER)
            remote_dir = os.path.join(REMOTE_DEST_PATH, rel_path).replace("\\", "/")
            
            # Create remote directory if it doesn't exist
            try:
                sftp.chdir(remote_dir)
            except IOError:
                try:
                    sftp.mkdir(remote_dir)
                except:
                    pass  

            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_dir, file).replace("\\", "/")
                sftp.put(local_file, remote_file)

        sftp.close()
        ssh.close()

        return jsonify({"status": "Files transferred successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=6000, debug=True)
