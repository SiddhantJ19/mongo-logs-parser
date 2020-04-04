import sys
import subprocess
import shlex
import tempfile

def main():
    mongo_log_file = str(sys.argv[1])
    if mongo_log_file.split('.')[1] != 'log':
        print("Invalid log file")
        return
    tail = subprocess.Popen(["tail", "-f", './mongo.log'], stdout=subprocess.PIPE, universal_newlines=True)
    buffer = []
    with open('parsed-logs-2.txt', 'w+') as f:
        while(True):
            buffer.append(tail.stdout.readline())
            if len(buffer) == 5:
                temp = tempfile.TemporaryFile(mode='w+t')
                temp.writelines(buffer)
                temp.seek(0)
                CMD = shlex.split("mlogfilter  --json --shorten=50 --human --no-progressbar " )
                parser = subprocess.Popen(CMD, stdin=temp ,stdout=f)
                buffer = []
                temp.close()

if __name__ == "__main__":
    main()