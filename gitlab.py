#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Ferras
# @Date:   2016-12-08 14:41:23
# @Last Modified time: 2016-12-08 16:17:48
import requests
import subprocess
import platform
from bs4 import BeautifulSoup


class GetHosts(object):
    def __init__(self, url):
        self.url = url

    def getHostsForLinux(self):
        # url = 'https://github.com/racaljk/hosts/blob/master/hosts'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep - alive',
            'Host': 'github.com',
            'Referer': 'https://github.com/racaljk/hosts',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/55.0.2883.9 Safari/537.36'
            }
        r = requests.get(url, headers)
        html = r.content
        hostList = BeautifulSoup(html, 'html.parser')
        hosts = hostList.find_all('td', attrs={'class': 'blob-code blob-code-inner js-file-line'})
        hl = []
        for h in hosts:
            host = h.string
            hl.append(host)
        # insert into hosts 127.0.0.1 ubuntu
        hl.insert(9, '127.0.0.1\tubuntu')
        print('Get hosts successfully!')

        sys_str = platform.system()
        if sys_str == 'Linux':
            fl = open('/home/ferras/Desktop/MyProject/hosts', 'w')
            for _ in hl:
                fl.write(_)
                fl.write('\n')
            fl.close()
            print('Write hosts OK!')

            p = subprocess.Popen('sudo mv /home/ferras/Desktop/MyProject/hosts /etc/',
                                 shell=True,
                                 close_fds=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            # bytes('sudo password' + '\n', 'encode')
            p.stdin.write(bytes('mxl' + '\n', 'ascii'))
            print('Hosts has been moved to \'/etc\'!')

        elif sys_str == 'Windows':
            fl = open('C:\Windows\System32\drivers\etc\hosts', 'w')
            for _ in hl:
                fl.write(_)
                fl.write('\n')
            fl.close()
            print('Write hosts OK!')


if __name__ == '__main__':
    url = 'https://github.com/racaljk/hosts/blob/master/hosts'
    new_hosts = GetHosts(url)
    new_hosts.getHostsForLinux()
