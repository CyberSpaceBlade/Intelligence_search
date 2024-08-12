import ipaddress
import os
import re
import time
from datetime import datetime
from DrissionPage import WebPage, ChromiumOptions
import pandas as pd


def ip_loc(ip):
    url = 'https://ip138.com/iplookup.php?ip=' + str(ip) + '&action=2'
    options = ChromiumOptions().headless(True)
    options.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/127.0.0.0 Safari/537.36')  #headless必带user_agent,反之可带可不带。
    page = WebPage(chromium_options=options, timeout=1)
    page.get(url)
    div1 = page.ele(".table-box")
    information_list = div1.text.split("\n")
    information_list.pop(0)
    res = []
    for item in information_list:
        res.extend(item.split('\t'))
    return res


def Is_private_ip(ip):
    private_networks = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    ip_address_obj = ipaddress.ip_address(ip)
    for network in private_networks:
        if ip_address_obj in ipaddress.ip_network(network):
            return False
    return True  # False即为内网IP,反之均为外网IP


def IPv4_check(address):
    pattern = (r"^(?:25[0-5]|2[0-4]\d|[1]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.("
               r"?:25[0-5]|2[0-4]\d|[01]?\d\d?)$")
    res1 = bool(re.match(pattern, str(address)))  # res1确定是一个正确的IPV4,但仍可能是内网地址
    if res1:
        list_address = str(address).split(".")
        res2 = True
        if int(list_address[0]) == 0 or int(list_address[3]) == 0:  #筛选出头尾两个数字为0的情形
            res2 = False
        else:
            for ip in list_address:  #筛选类似018的情形
                if int(ip[0]) == 0 and len(ip) > 1:
                    res2 = False
                    break
        if res2 is True:
            res2 = Is_private_ip(address)
        return res1 and res2  # 只有两个条件都满足的才是满足要求的外网IP
    else:
        return res1  # 格式匹配都没通过的都不是标准IP,直接return False
    pass


def ip_bind_sort(ip_list1, ip_list2):
    # 定义一个IP地址列表
    total_list = list(set(ip_list1) | set(ip_list2))  #IP地址整合
    ip_addresses = [ipaddress.ip_address(ip) for ip in total_list if IPv4_check(ip)]
    sorted_ips = sorted(ip_addresses)
    # 只有列表才能排序
    # 只有转成ipv4格式才会按照第一位数字的大小排序,反之会出现99.X.X.X在175.X.X.X后面的情况

    # 将ipaddress.IPv4Address对象转换回字符串形式的IP地址
    sorted_ip_list = [str(ip) for ip in sorted_ips]  # IP地址排序
    return sorted_ip_list


def ip_import(excel_name):
    # 读取Excel文件
    df = pd.read_excel(excel_name, engine='calamine')
    ips = df.iloc[:, 0]
    # :前后是开始取数据的行始末，没有即为全取;0表示为第一列，多列可写为[0,1]
    # 此处即为取第一列。在操作过程中，只需要保障第一列为IP项目即可，其余条目内容不影响
    ip_list = [str(ip).strip().replace(" ", "") for ip in ips]
    column_length = len(df.columns)
    try:
        time_list = df.iloc[:, 1].tolist()
    except:
        time_list = []
    return ip_list, column_length, time_list

    # title=df.columns.tolist() #将表头行转为列表
    # print(df.iloc[0])    #读取第一行
    # print(df['IP'].tolist()) #将IP列转为列表


def return_time(ip, ip_list1, ip_list2, dict1, dict2, set1, set3, set4):
    if ip in set1:  # 在第一个表里
        if len(set3) == 0:  # 第一个表非规范化
            res = ip_list1[-1]
        else:  # 规范化,直接查字典
            res = dict1[ip]
    else:
        if len(set4) == 0:
            res = ip_list2[-1]
        else:
            res = dict2[ip]

    return res


def generate_or_update(excel_name1, excel_name2, target_excel):  #主要功能之一,情报表的构建、更新
    dict1 = dict2 = {}
    start = time.time()
    ip_list1, column_length1, time_list1 = ip_import(excel_name1)  #返回的是一个列表,数据类型str
    ip_list2, column_length2, time_list2 = ip_import(excel_name2)
    merge_ip = ip_bind_sort(ip_list1, ip_list2)  #返回的是一个列表,数据类型str，与Ip_list们的情况是一样的

    # 上述完成IP合并,下开始处置时间列
    if (column_length1 == 0) or (len(re.findall(r'\d{4}-\d{2}-\d{2}', str(time_list1))) == 0):
        # 说明表1非规范化,则需要获取时间戳并作废原list
        ip_list1.append(str(datetime.fromtimestamp(os.path.getmtime(excel_name1))).split(" ")[0])  #把最后一个元素作为生成时间
        time_list1 = []

    if (column_length2 == 0) or (len(re.findall(r'\d{4}-\d{2}-\d{2}', str(time_list2))) == 0):
        # 说明表2非规范化,则需要获取时间戳并作废原list
        ip_list2.append(str(datetime.fromtimestamp(os.path.getmtime(excel_name2))).split(" ")[0])
        time_list2 = []

    if len(time_list1) > 0:
        dict1 = dict(zip(ip_list1, time_list1))
    if len(time_list2) > 0:
        dict2 = dict(zip(ip_list2, time_list2))
    set1 = set(ip_list1)
    set3 = set(dict1.keys())
    set4 = set(dict2.keys())

    time_list = [return_time(ip, ip_list1, ip_list2, dict1, dict2, set1, set3, set4) for ip in merge_ip]

    data = {
        'IP': merge_ip,
        '情报生成时间': time_list
    }
    df = pd.DataFrame(data)
    df.to_excel(target_excel, index=False)

    end = time.time()
    return int(end - start)


def ip_search(ip, table_xlsx):
    ip_list = set(ip_import(table_xlsx)[0])
    if ip in ip_list:
        res = "命中情报!"
    else:
        res = "未命中情报!"
    return res


def ips_search(ips, table_xlsx):
    ip_list = set(ip_import(table_xlsx)[0])
    new_ip_list = []
    for ip in ips:
        if ip in ip_list:
            pass
        else:
            new_ip_list.append(ip)
    return new_ip_list


'''

def main():
    generate_or_update('Inte-All.xlsx', "Inte-GASS.xlsx", 'Inte-All.xlsx')
    pass


if __name__ == "__main__":
    main()
'''
