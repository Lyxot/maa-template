import subprocess
import toml
import os
import pathlib

client_type = os.getenv("CLIENT_TYPE")

config = toml.load('daily.toml')
for i in config['tasks']:
    if 'params' in i:
        if 'client_type' in i['params']:
            i['params']['client_type'] = client_type
with open(str(pathlib.Path.home())+'/.config/maa/tasks/daily.toml', 'w') as f:
    toml.dump(config, f)

process = subprocess.Popen("maa run daily", shell=True, stdout=subprocess.PIPE)
output, error = process.communicate()

log = ""
summary = ""
flag_summary = False
for line in output.splitlines():
    line = line.decode('utf-8')
    if flag_summary:
        summary += line + "\n"
    if "Summary" in line:
        flag_summary = True
    print(line)
    log += line + "\n"
process.kill()

summary_md = "# Summary\n" + summary
summary_md += "\n\n# Log\n```\n" + log + "```\n"
os.system('echo "' + summary_md + '" > "$GITHUB_STEP_SUMMARY"')

summary_list = summary.splitlines()
summary_msg = ""
for i in range(len(summary_list)):
    line = summary_list[i]
    if line.count('-') > len(line)*0.75:
        summary_msg += summary_list[i+1] + "\n"
with open('msg', 'w') as f:
    f.write(summary_msg)
