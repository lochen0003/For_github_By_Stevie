#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Created on :  2020/8/9
# @Created by :  Stevie
#安装f5-sdk

from f5.bigip import ManagementRoot
from openpyxl import Workbook

pool_node_link_list_0 = []
pool_node_link_list = []
vs_pool_link_list_0 = []
vs_pool_link_list = []
vs_pool_node_link_list_0 = []
vs_pool_node_link_list = []

wb = Workbook()
dest_file = 'f5.xlsx'  # xls 文件名

# 连接
mgmt = ManagementRoot("1.1.1.1", "web_admin", "web_passwd")

pools = mgmt.tm.ltm.pools.get_collection()
for pool in pools:
    # print(pool.name)
    for node_in_pool in pool.members_s.get_collection():
        # print(node_in_pool.name)
        pool_node_link_list_0 = [pool.name, node_in_pool.name]
        pool_node_link_list.append(pool_node_link_list_0)
pool_node_link_list_0 = []
# print(pool_node_link_list)

virtual_servers = mgmt.tm.ltm.virtuals.get_collection()
for virtual_server in virtual_servers:
    # print(virtual_server.raw)
    # print(virtual_server.destination)
    try:
        vs_pool_link_list_0 = [virtual_server.name, virtual_server.destination.split('/')[-1],
                               virtual_server.pool.split('/')[-1]]
        vs_pool_link_list.append(vs_pool_link_list_0)
        # print(virtual_server.pool)
    except AttributeError as error_1:
        try:
            pass
            # print(virtual_server.rules)
        except AttributeError as error_2:
            print(error_2)
            print(error_1)

for x in vs_pool_link_list:
    for y in pool_node_link_list:
        if x[2] == y[0]:
            vs_pool_node_link_list_0 = (x[0], x[1], y[0], y[1])
            vs_pool_node_link_list.append(vs_pool_node_link_list_0)
        else:
            pass

list_len = len(vs_pool_node_link_list)
ws1 = wb.active
ws1.title = 'F5_VS_Link_Info'
xls_head = ['VS名称', 'VS_IP地址', '关联Pool名称', '后端IP地址']
ws_row = 2

for col in range(1, 5):
    ws1.cell(column=col, row=1, value=xls_head[col-1])

for info in vs_pool_node_link_list:
    ws1.cell(column=1, row=ws_row, value=info[0])
    ws1.cell(column=2, row=ws_row, value=info[1])
    ws1.cell(column=3, row=ws_row, value=info[2])
    ws1.cell(column=4, row=ws_row, value=info[3])
    ws_row = ws_row + 1
    print(info)

ws1.column_dimensions['A'].width = 30.0
ws1.column_dimensions['B'].width = 25.0
ws1.column_dimensions['C'].width = 35.0
ws1.column_dimensions['D'].width = 25.0

wb.save(filename=dest_file)

print(':) Py by Stevie_Chen...')

# 待更新vs类型、'i_rules' 关联关系