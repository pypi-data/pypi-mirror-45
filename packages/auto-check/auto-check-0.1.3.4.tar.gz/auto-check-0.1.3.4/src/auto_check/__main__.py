# -*- coding: UTF-8 -*-
import hashlib
import json
import threading
import time

import requests

from .auto_checker import AutoChecker
from .property import Property
from .parse_params import parse


def is_holiday():
    try:
        url = 'http://api.goseek.cn/Tools/holiday?date=' + time.strftime('%Y%m%d', time.localtime())
        resp = requests.get(url).json()
        print(resp)
    except Exception:
        # 请求接口失败，调用本地日历，进行基本判断
        print('查询API失败，调用本地日历，判断是否为周末')
        return 5 <= time.localtime()[6] <= 6
    else:
        return resp['data'] == 1 or resp['data'] == 3


def get_check_conf(url):
    try:
        conf = requests.get(url).json()
    except Exception:
        print('获取配置信息失败')
        return json
    else:
        return conf


def main(**kwargs):
    # 解析参数
    params = parse()
    if params.url == '' and params.config_dir == '':
        print('No conf info defined, please check again or use -h')
        return
    # 工作日判定
    if is_holiday():
        print('holiday')
        return
    print('workday')
    # 优先从网络获取配置参数
    timestr = time.strftime('%Y.%m.%d', time.localtime(time.time())) + 'yysasurai'
    m = hashlib.md5()
    m.update(timestr.encode('utf-8'))
    header = {
        'auth': m.hexdigest()
    }
    if params.url != '':
        resp = str(requests.get(params.url, headers=header).content).replace('b\'', '').replace(']\'', ']')
        print(resp)
        configs = json.loads(resp)
        print(configs)
        for conf in configs:
            # print(conf['username'])
            # 若已设置过滤，
            if params.suffix != '':
                # print(params.suffix)
                if not conf['username'].__contains__(params.suffix):
                    pass
                else:
                    t = threading.Thread(target=AutoChecker(Property(conf), params.test, not params.immediately, params.force).check,
                                         name=conf['username'])
                    t.start()
                    print('matched for %s' % params.suffix)
                    break
            else:
                t = threading.Thread(target=AutoChecker(Property(conf), params.test, not params.immediately, params.force).check,
                                     name=conf['username'])
                t.start()
    # 再从本地获取
    elif params.config_dir != '':
        print('local config not supported any more')
        return
        # configs = os.listdir(params.config_dir)
        # os.chdir(params.config_dir)
        #
        # cnt = 0
        # for config_name in configs:
        #     if config_name.__contains__('config_' + params.suffix):
        #         print(config_name)
        #         t = threading.Thread(
        #             target=AutoChecker(Property(config_name), params.test, not (params.immediately)).check,
        #             name=config_name)
        #         t.start()
        #         cnt += 1
        # print('There are ' + str(cnt) + ' configuration file(s) satisfied. ')
    else:
        print('No conf info defined, please check again or use -h')
        return


if __name__ == '__main__':
    main()
