import random
import uuid


def __num(n):
    """
    n个9的int
    :param n: 位数
    :return: int eg: num(2)-->99 num(3)-->999
    """
    return 10 ** (n) - 1


def numstr(n):
    """
    n位随机数的字符串
    :param n: 位数
    :return: str eg: numstr(2)-->'23' numstr(3)-->'551'
    """
    return str(random.randint(0, __num(n))).zfill(n)


def num(n):
    """
    n位随机整数
    :param n: 位数
    :return:
    """
    return int(numstr(n))


def numfloat(n, roundnum=2):
    """
    n位整数+roundnum位小数的浮点
    :param n:
    :param roundnum: 小数点后位数
    :return: float eg: floatnum(3)-->342.78
    """
    new_num = random.uniform(0, __num(n))
    return round(new_num, roundnum)


def mobile():
    """
    返回一个11位的手机号码-str
    return: str
    """
    mobile_rand = '1' + numstr(10)
    return mobile_rand


def email():
    email_types = ('@163.com', '@qq.com', '@sina.cn', '@sina.com')
    pre_rand = numstr(9)
    return pre_rand + random.choice(email_types)


def identification():
    """
    身份证
    :return:
    """
    id_rand = '44' + numstr(16)
    return id_rand


def list_gen(length, func, *arg):
    """
    list_gen(3, mobile)-->返回3个mobile结果
    :param length:
    :param func:
    :return: list
    """
    ret_list = []
    for x in range(length):
        ret_list.append(func(*arg))
    return ret_list


def uuid1():
    """
    16字节
    :return:
    """
    return str(uuid.uuid1()).replace('-', '')


if __name__ == '__main__':
    print(uuid1())
    print(list_gen(2, mobile))
    print(num(3))
