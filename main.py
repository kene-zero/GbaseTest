from libs import common
from libs import log

log = log.Log().get_logger()


def ptest():
    ssh = common.NodeSSH(ip="192.168.100.100", user="root", pwd="gbase@123")
    res = ssh.send_cmd("pwd")
    log.info(res)


if __name__ == '__main__':
    ptest()
