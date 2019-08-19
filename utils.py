import random
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    # 改进log把web写入文件
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


# 格式化时间戳
def formatted_time(t):
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(t))
    formatted = time.strftime(time_format, value)
    return formatted
