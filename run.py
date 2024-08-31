import subprocess
import requests
import toml
import os
import sys
import pathlib

url = os.getenv("ONEBOT_URL")
qqid=int(os.getenv("QQID"))
client_type = os.getenv("CLIENT_TYPE")
flag_send = bool(os.getenv("SEND_MSG"))

def send_msg(id,msg):
    data = {
        "message_type": "private",
        "user_id": id,
        "message": msg
    }
    response = requests.post(url+'/send_msg', json=data)
    return response.json()

if __name__ == '__main__':
    config = toml.load('daily.toml')
    for i in config['tasks']:
        if 'params' in i:
            if 'client_type' in i['params']:
                i['params']['client_type'] = client_type
    with open(str(pathlib.Path.home())+'/.config/maa/tasks/daily.toml', 'w') as f:
        toml.dump(config, f)

    process = subprocess.Popen("maa run daily", shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()

    msg = ""
    flag_summary = False
    for line in output.splitlines():
        line = line.decode('utf-8')
        if "Summary" in line:
            flag_summary = True
        if flag_summary:
            msg += line + "\n"
        print(line)

    process.kill()

    if flag_send:
        send_msg(qqid, msg)
