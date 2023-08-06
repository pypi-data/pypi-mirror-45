# -*- coding=utf-8 -*-
" Output helper of rlj "
import colorama
import os
import sys
from .language import getLanguage

def addColor(color, text):
    return getattr(colorama.Fore, color) + text + colorama.Fore.RESET


def addBgColor(color, text):
    return getattr(colorama.Back, color) + getattr(colorama.Fore, 'BLACK')\
        + ' ' + text + ' ' + colorama.Fore.RESET + colorama.Back.RESET


def addStyle(style, text):
    return getattr(colorama.Style, style) + text + colorama.Style.RESET_ALL


def getFormat(config):
    datas = config.datas
    format_string = ''
    head_line = ''
    task_len = max(4, len(str(len(datas) + 1)))
    format_string += '{{:<{}}}'.format(task_len)
    head_line += '编号' + ' ' * (task_len - 4)
    indata_len = 8
    outdata_len = 8
    for (indata, outdata) in datas:
        indata_len = max(indata_len, len(indata))
        outdata_len = max(outdata_len, len(outdata))
    format_string += '  {{:<{}}}'.format(indata_len)
    format_string += '  {{:<{}}}'.format(outdata_len)
    head_line += '  输入文件' + ' ' * (indata_len - 8)
    head_line += '  输出文件' + ' ' * (outdata_len - 8)
    status_len = 4
    format_string += '  {{:<{}}}'.format(status_len)
    head_line += '  状态' + ' ' * (status_len - 4)
    time_len = max(4, len('{:.3f}s'.format(config.time_limit / 1000)))
    memory_len = max(4, len('{}MB'.format(int(config.memory_limit))))
    format_string += '  {{:<{}}}'.format(memory_len)
    format_string += '  {{:<{}}}'.format(time_len)
    head_line += '  内存' + ' ' * (memory_len - 4)
    head_line += '  时间' + ' ' * (time_len - 4)
    # print(format_string)
    return (head_line, format_string)


def printResult(config, result, status=[]):
    lang = getLanguage(config.source)
    silent = config.silent
    head, fmt = getFormat(config)
    sep_line = '=' * (len(head.encode('gb2312')) + 2)
    if not silent:
        print(sep_line)
        print(addStyle('BRIGHT', addColor('BLUE', 'Language: '))
              + addBgColor('BLUE', lang['name']))
        print('正在编译...')

    compileStatusColor = {'CTLE': 'YELLOW', 'ERROR': 'RED', 'DONE': 'GREEN'}

    compile_status = result.__next__()
    color = compileStatusColor[compile_status[0]]
    print(addBgColor(color, compile_status[0])
          + addColor(color, compile_status[1]), end='')
    if compile_status[0] == 'DONE':
        print(addColor(color, ', 用时：%.3fs' % compile_status[2]))
    else:
        if not silent:
            print('\n' + sep_line)
        if compile_status[0] == 'ERROR':
            os.system('cat temp/compile.log')
            print(sep_line)
        return False

    statusColor = {'AC': 'GREEN', 'WA': 'RED', 'TLE': 'YELLOW',
                   'MLE': 'BLUE', 'RE': 'CYAN'}
    status = []
    if silent:
        num = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'RE': 0}
        for task in result:
            st = task[2].status
            print(addBgColor(statusColor[st], st[0]), end='')
            num[st] += 1
            sys.stdout.flush()
            status.append(st)
        print()
        for st in statusColor:
            if not num[st]:
                continue
            print(addBgColor(statusColor[st], st[0] + ':%d' % num[st]),
                  end=' ')
        print()
    else:
        print(sep_line)
        print(head)
        print(sep_line)
        tot_time = 0
        max_memory = 0
        for task in result:
            st = task[2].status
            s = fmt.format(task[0], task[1][0], task[1][1],
                           addBgColor(statusColor[st], st),
                           str(int(task[2].memory_used)) + 'MB',
                           '%.3fs' % (task[2].time_used / 1000))
            if st == 'AC':
                tot_time += task[2].time_used
                max_memory = max(max_memory, task[2].memory_used)
            print(s)
            status.append(st)
        print(sep_line)
        print('总时:%.3fs\n最大空间:%dMB' % (tot_time / 1000, int(max_memory)))
    return True

