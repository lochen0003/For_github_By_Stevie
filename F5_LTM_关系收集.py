#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Created on :  2020/8/9
# @Created by :  Stevie

from f5.bigip import ManagementRoot

pool_node_link_list_0 = []
pool_node_link_list = []
vs_pool_link_list_0 = []
vs_pool_link_list = []
vs_pool_node_link_list_0 = []
vs_pool_node_link_list = []

# 连接
mgmt = ManagementRoot("168.10.80.172", "admin", "YBwonders2008")

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

f5_info_file = open('f5_info_file.txt', 'w', encoding='utf-8-sig')
for info in vs_pool_node_link_list:
    f5_info_file.write('VS名称: ' + info[0] + ' VS_IP地址: ' + info[1] +
                       ' 关联Pool名称: ' + info[2] + ' 后端IP地址: ' + info[3] + '\n')
    print(info)
f5_info_file.close()
print(':) Py by Stevie_Chen...')

# print(vs_pool_node_link_list)

# # pool name
# for i in pool_node_link_list:
#     print(i[0])
# # node name
# for i in pool_node_link_list:
#     print(i[1])