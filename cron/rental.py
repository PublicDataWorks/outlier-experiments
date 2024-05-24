from subprocess import PIPE, Popen


def fetch_data():
    try:
        process = Popen(["./cron/rental.sh"], shell=True, stdin=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stdout:
            print("STDOUT:{}".format(stdout.decode()))
        if stderr:
            print("STDERR:{}".format(stderr.decode()))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    fetch_data()
