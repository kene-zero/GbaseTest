#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/28 14:51
# @Author  : zhaodongz
# @Site    :
# @File    : yml.py
# @Software: PyCharm
"""项目描述：生成yml"""

from tkinter import *
from tkinter.ttk import Combobox
import os
import yaml
import ipaddress

# 定义窗体变量
lb1, inp1, lb2, comb, lb3, comb1, lb6, comb2, lb4, inp4, lb5, inp5, lb0 = '', '', '', '', '', '', '', '', '', '', '', '', ''
yaml.dump()
ipaddress.ip_address('277.0.0.1')
yaml_dict = {"gha_server":[]}


def gha_server(ip):
    writeyml(f'''gha_server:
  - gha_server1:
      host: {ip}
      port: 20001
''')


def dcs(ip):
    writeyml(f'''  - host: {ip}
    port: 2379''')


def gtm(ip, ver, dataidr):
    if ver == 2:
        writeyml(f'''  - gtm1:
      host: {ip}
      agent_host: {ip}
      role: primary
      port: 6666
      agent_port: 8001
      work_dir: {dataidr}/gtm/gtm1
      # - gtm2:
 #     host: {ip}
 #     agent_host: {ip}
 #     role: standby
 #     port: 6660
 #     agent_port: 8002
 #     work_dir: {dataidr}/gtm/gtm2
''')
    else:
        pass


def coordinator(ip, ver, dataidr, n):
    if ver == 2:
        writeyml(f'''  - cn{n}:
      host: {ip}
      agent_host: {ip}
      role: primary
      port: 5432
      agent_port: 8003
      work_dir: {dataidr}/coord/cn{n}''')
    else:
        pass


def datanode0(ip, num, dataidr, n):
    # if num == 0:
    writeyml(f'''      - dn{n}_1:
          host: {ip}
          agent_host: {ip}
          role: primary
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_1
''')


def datanode1(ip1, ip2, num, dataidr, n):
    # if num == 1:
    writeyml(f'''       - dn{n}_1:
          host: {ip1}
          agent_host: {ip1}
          role: primary
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_1
      - dn{n}_2:
          host: {ip2}
          agent_host: {ip2}
          role: standby
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_2
''')


def datanode2(ip1, ip2, ip3, num, dataidr, n):
    # if num == 2:
    writeyml(f'''      - dn{n}_1:
          host: {ip1}
          agent_host: {ip1}
          role: primary
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_1
      - dn{n}_2:
          host: {ip2}
          agent_host: {ip2}
          role: standby
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_2
      - dn{n}_3:
          host: {ip3}
          agent_host: {ip3}
          role: standby
          port: {15432 + 10 * (n - 1)}
          agent_port: {8005 + n - 1}
          work_dir: {dataidr}/dn{n}/dn{n}_3''')


def env(version, num):
    if int(version[-1]) % 2 == 0 and num == 2:
        writeyml(f'''env:
  # cluster_type allowed values: multiple-nodes, single-inst, default is multiple-nodes
  cluster_type: multiple-nodes
  pkg_path: /home/gbase/deploy
  prefix: /home/gbase/gbase_db
  version: V5_S3.0.0{version}
  user: gbase
  port: 22''')
    elif int(version[-1]) % 2 == 1 and num < 2:
        writeyml(f'''env:
    # cluster_type allowed values: multiple-nodes, single-inst, default is multiple-nodes
    cluster_type: single-inst
    pkg_path: /home/gbase/deploy
    prefix: /home/gbase/gbase_db
    version: V5_S3.0.0{version}
    user: gbase
    port: 22'''
                 )
    else:
        return False
    return True


def run1():
    try:
        a = str(inp1.get())
        ipaddr = a.strip().split(',')
        ip_result = [isip(i) for i in ipaddr]
        if False in ip_result:
            raise ValueError("ip格式不正确")
        if len(ipaddr) != len(set(ipaddr)):
            raise ValueError("IP地址重复")
        s = '%s\n' % (ipaddr)
        v1 = comb.current()  # 获取某种形态
        v2 = comb1.current()  # 获取多少个备机
        v3 = str(inp4.get()).strip()  # 获取版本号
        v4 = str(inp5.get()).strip()  # 获取安装路径
        v5 = comb1.current() + 1  # 获取DN组的数量
        v5 = v5 if v5 else 1  # 获取DN组的数量
        if v3[0] != 'B':
            raise ValueError("版本号格式应为B01、B02等")
        if v1 != 2 and v5 != 1:
            raise ValueError("非分布式DN组数量应为1.")
        if v5 > 10:
            raise ValueError("DN组超过最大值，请修改.")
        if v5 > len(ipaddr):
            raise ValueError("DN组超过IP的个数，请修改.")
        # print(v5)
        if os.path.exists('gbase.yml'):
            removeyml()
        # print(ipaddr)
        # print(v1, v2, v3, v4, v5)
        gha_server(ipaddr[0])
        writeyml('dcs:')
        for i in ipaddr:
            dcs(i)
        if v1 == 2:
            writeyml('gtm:')
            gtm(ipaddr[0], v1, v4)
            writeyml('coordinator:')
            for i in range(1, len(ipaddr)):
                coordinator(ipaddr[i], v1, v4, i)
        else:
            pass
        writeyml('datanode:')
        if v1 == 0 or (v1 == 1 and v2 == 0):
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
        elif v1 == 1 and v2 == 1:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
        elif v1 == 1 and v2 == 2:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
        elif v1 == 2 and v2 == 0 and v5 == 1:
            writeyml('  - dn1:')
            datanode0(ipaddr[1], v1, v4, 1)
        elif v1 == 2 and v2 == 0 and v5 == 2:
            writeyml('  - dn1:')
            datanode0(ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[2], v1, v4, 2)
        elif v1 == 2 and v2 == 0 and v5 == 3:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
        elif v1 == 2 and v2 == 0 and v5 == 4:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[-1], v1, v4, 4)
        elif v1 == 2 and v2 == 0 and v5 == 5:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[-1], v1, v4, 5)
        elif v1 == 2 and v2 == 0 and v5 == 6:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[4], v1, v4, 5)
            writeyml('  - dn6:')
            datanode0(ipaddr[-1], v1, v4, 6)
        elif v1 == 2 and v2 == 0 and v5 == 7:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[4], v1, v4, 5)
            writeyml('  - dn6:')
            datanode0(ipaddr[5], v1, v4, 6)
            writeyml('  - dn7:')
            datanode0(ipaddr[-1], v1, v4, 7)
        elif v1 == 2 and v2 == 0 and v5 == 8:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[4], v1, v4, 5)
            writeyml('  - dn6:')
            datanode0(ipaddr[5], v1, v4, 6)
            writeyml('  - dn7:')
            datanode0(ipaddr[6], v1, v4, 7)
            writeyml('  - dn8:')
            datanode0(ipaddr[-1], v1, v4, 8)
        elif v1 == 2 and v2 == 0 and v5 == 9:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[4], v1, v4, 5)
            writeyml('  - dn6:')
            datanode0(ipaddr[5], v1, v4, 6)
            writeyml('  - dn7:')
            datanode0(ipaddr[6], v1, v4, 7)
            writeyml('  - dn8:')
            datanode0(ipaddr[7], v1, v4, 8)
            writeyml('  - dn9:')
            datanode0(ipaddr[-1], v1, v4, 9)
        elif v1 == 2 and v2 == 0 and v5 == 10:
            writeyml('  - dn1:')
            datanode0(ipaddr[0], v1, v4, 1)
            writeyml('  - dn2:')
            datanode0(ipaddr[1], v1, v4, 2)
            writeyml('  - dn3:')
            datanode0(ipaddr[2], v1, v4, 3)
            writeyml('  - dn4:')
            datanode0(ipaddr[3], v1, v4, 4)
            writeyml('  - dn5:')
            datanode0(ipaddr[4], v1, v4, 5)
            writeyml('  - dn6:')
            datanode0(ipaddr[5], v1, v4, 6)
            writeyml('  - dn7:')
            datanode0(ipaddr[6], v1, v4, 7)
            writeyml('  - dn8:')
            datanode0(ipaddr[7], v1, v4, 8)
            writeyml('  - dn9:')
            datanode0(ipaddr[8], v1, v4, 9)
            writeyml('  - dn10:')
            datanode0(ipaddr[-1], v1, v4, 10)
        elif v1 == 2 and v2 == 1 and v5 == 1:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
        elif v1 == 2 and v2 == 1 and v5 == 2:
            writeyml('  - dn1:')
            datanode1(ipaddr[2], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[0], v1, v4, 2)
        elif v1 == 2 and v2 == 1 and v5 == 3:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
        elif v1 == 2 and v2 == 1 and v5 == 4:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
        elif v1 == 2 and v2 == 1 and v5 == 5:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
        elif v1 == 2 and v2 == 1 and v5 == 6:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
            writeyml('  - dn6:')
            datanode1(ipaddr[-1], ipaddr[4], v1, v4, 6)
        elif v1 == 2 and v2 == 1 and v5 == 7:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
            writeyml('  - dn6:')
            datanode1(ipaddr[-1], ipaddr[4], v1, v4, 6)
            writeyml('  - dn7:')
            datanode1(ipaddr[-1], ipaddr[5], v1, v4, 7)
        elif v1 == 2 and v2 == 1 and v5 == 8:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
            writeyml('  - dn6:')
            datanode1(ipaddr[-1], ipaddr[4], v1, v4, 6)
            writeyml('  - dn7:')
            datanode1(ipaddr[-1], ipaddr[5], v1, v4, 7)
            writeyml('  - dn8:')
            datanode1(ipaddr[-1], ipaddr[6], v1, v4, 8)
        elif v1 == 2 and v2 == 1 and v5 == 9:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
            writeyml('  - dn6:')
            datanode1(ipaddr[-1], ipaddr[4], v1, v4, 6)
            writeyml('  - dn7:')
            datanode1(ipaddr[-1], ipaddr[5], v1, v4, 7)
            writeyml('  - dn8:')
            datanode1(ipaddr[-1], ipaddr[6], v1, v4, 8)
            writeyml('  - dn9:')
            datanode1(ipaddr[-1], ipaddr[7], v1, v4, 9)
        elif v1 == 2 and v2 == 1 and v5 == 9:
            writeyml('  - dn1:')
            datanode1(ipaddr[0], ipaddr[1], v1, v4, 1)
            writeyml('  - dn2:')
            datanode1(ipaddr[1], ipaddr[2], v1, v4, 2)
            writeyml('  - dn3:')
            datanode1(ipaddr[2], ipaddr[0], v1, v4, 3)
            writeyml('  - dn4:')
            datanode1(ipaddr[3], ipaddr[1], v1, v4, 4)
            writeyml('  - dn5:')
            datanode1(ipaddr[-1], ipaddr[3], v1, v4, 5)
            writeyml('  - dn6:')
            datanode1(ipaddr[-1], ipaddr[4], v1, v4, 6)
            writeyml('  - dn7:')
            datanode1(ipaddr[-1], ipaddr[5], v1, v4, 7)
            writeyml('  - dn8:')
            datanode1(ipaddr[-1], ipaddr[6], v1, v4, 8)
            writeyml('  - dn9:')
            datanode1(ipaddr[-1], ipaddr[8], v1, v4, 10)
        elif v1 == 2 and v2 == 2 and v5 == 1:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
        elif v1 == 2 and v2 == 2 and v5 == 2:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[2], ipaddr[0], v2, v4, 2)
        elif v1 == 2 and v2 == 2 and v5 == 3:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
        elif v1 == 2 and v2 == 2 and v5 == 4:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[-1], ipaddr[1], ipaddr[0], v2, v4, 4)
        elif v1 == 2 and v2 == 2 and v5 == 5:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[-1], ipaddr[3], ipaddr[2], v2, v4, 5)
        elif v1 == 2 and v2 == 2 and v5 == 6:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[4], ipaddr[3], ipaddr[2], v2, v4, 5)
            writeyml('  - dn6:')
            datanode2(ipaddr[-1], ipaddr[4], ipaddr[3], v2, v4, 5)
        elif v1 == 2 and v2 == 2 and v5 == 7:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[4], ipaddr[3], ipaddr[2], v2, v4, 5)
            writeyml('  - dn6:')
            datanode2(ipaddr[5], ipaddr[4], ipaddr[3], v2, v4, 6)
            writeyml('  - dn7:')
            datanode2(ipaddr[-1], ipaddr[5], ipaddr[4], v2, v4, 7)
        elif v1 == 2 and v2 == 2 and v5 == 8:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[4], ipaddr[3], ipaddr[2], v2, v4, 5)
            writeyml('  - dn6:')
            datanode2(ipaddr[5], ipaddr[4], ipaddr[3], v2, v4, 6)
            writeyml('  - dn7:')
            datanode2(ipaddr[6], ipaddr[5], ipaddr[4], v2, v4, 7)
            writeyml('  - dn8:')
            datanode2(ipaddr[-1], ipaddr[6], ipaddr[5], v2, v4, 7)
        elif v1 == 2 and v2 == 2 and v5 == 9:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[4], ipaddr[3], ipaddr[2], v2, v4, 5)
            writeyml('  - dn6:')
            datanode2(ipaddr[5], ipaddr[4], ipaddr[3], v2, v4, 6)
            writeyml('  - dn7:')
            datanode2(ipaddr[6], ipaddr[5], ipaddr[4], v2, v4, 7)
            writeyml('  - dn8:')
            datanode2(ipaddr[7], ipaddr[6], ipaddr[5], v2, v4, 8)
            writeyml('  - dn9:')
            datanode2(ipaddr[-1], ipaddr[7], ipaddr[6], v2, v4, 9)
        elif v1 == 2 and v2 == 2 and v5 == 10:
            writeyml('  - dn1:')
            datanode2(ipaddr[0], ipaddr[1], ipaddr[2], v2, v4, 1)
            writeyml('  - dn2:')
            datanode2(ipaddr[1], ipaddr[0], ipaddr[2], v2, v4, 2)
            writeyml('  - dn3:')
            datanode2(ipaddr[2], ipaddr[1], ipaddr[0], v2, v4, 3)
            writeyml('  - dn4:')
            datanode2(ipaddr[3], ipaddr[2], ipaddr[1], v2, v4, 4)
            writeyml('  - dn5:')
            datanode2(ipaddr[4], ipaddr[3], ipaddr[2], v2, v4, 5)
            writeyml('  - dn6:')
            datanode2(ipaddr[5], ipaddr[4], ipaddr[3], v2, v4, 6)
            writeyml('  - dn7:')
            datanode2(ipaddr[6], ipaddr[5], ipaddr[4], v2, v4, 7)
            writeyml('  - dn8:')
            datanode2(ipaddr[7], ipaddr[6], ipaddr[5], v2, v4, 8)
            writeyml('  - dn9:')
            datanode2(ipaddr[8], ipaddr[7], ipaddr[6], v2, v4, 9)
            writeyml('  - dn10:')
            datanode2(ipaddr[-1], ipaddr[8], ipaddr[7], v2, v4, 10)
        res = env(v3, v1)
        fg = 'green'
        if res:
            result = "生成成功！"
        else:
            result = '部署形态与版本不符合。'
            fg = 'red'
    except Exception as e:
        result = '参数输入错误，请核实：' + str(e)
        fg = 'red'
    lb0.config(text=str(result), fg=fg)
    # inp1.delete(0, END)  # 清空输入


def createyml():
    root = Tk()
    root.geometry('460x240')
    root.title('GBASE yml生成器')

    lb1 = Label(root, text='请输入ip地址（使用英文逗号进分开）：', )
    lb1.place(relx=0.05, rely=0.1, relwidth=0.8, relheight=0.1, )
    inp1 = Entry(root, textvariable=1)
    inp1.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
    lb2 = Label(root, text='请选择您的部署形态：')
    lb2.place(relx=0.05, rely=0.3, relwidth=0.3, relheight=0.1)
    comb = Combobox(root, textvariable=StringVar(), values=['单机', '主备', '分布式', ])
    comb.place(relx=0.1, rely=0.4, relwidth=0.2)

    lb3 = Label(root, text='请选择您的备机数量：')
    lb3.place(relx=0.32, rely=0.3, relwidth=0.3, relheight=0.1)
    comb1 = Combobox(root, textvariable=StringVar(), values=['0备机', '1备机', '2备机', ])
    comb1.place(relx=0.4, rely=0.4, relwidth=0.2)

    lb6 = Label(root, text='DN组的数量：')
    lb6.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.1)
    comb2 = Combobox(root, textvariable=StringVar(), values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    comb2.place(relx=0.7, rely=0.4, relwidth=0.1, relheight=0.1)

    lb4 = Label(root, text='版本号（如:B01）：')
    lb4.place(relx=0.05, rely=0.5, relwidth=0.3, relheight=0.1)
    inp4 = Entry(root, )
    inp4.place(relx=0.1, rely=0.6, relwidth=0.1, relheight=0.1)

    lb5 = Label(root, text='请输入您的安装路径：（例：/home/gbase）')
    lb5.place(relx=0.3, rely=0.5, relwidth=0.7, relheight=0.1)
    inp5 = Entry(root)
    inp5.place(relx=0.3, rely=0.6, relwidth=0.6, relheight=0.1)

    # 方法-直接调用 run1()
    print(lb1, inp1, lb2, comb, lb3, comb1, lb6, comb2, lb4, inp4, lb5, inp5)
    btn1 = Button(root, text='生成', command=run1)
    btn1.place(relx=0.1, rely=0.8, relwidth=0.3, relheight=0.1)

    # 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
    lb0 = Label(root, text='结果')
    lb0.place(relx=0.4, rely=0.8, relwidth=0.6, relheight=0.1)

    root.mainloop()


if '__name__=' == '__main__':
    createyml()
    print()
