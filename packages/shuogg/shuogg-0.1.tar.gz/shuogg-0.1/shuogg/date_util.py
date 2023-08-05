import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DAY_FORMAT = "%Y-%m-%d"


def get_each_day(start_time, end_time):
    """
    list<datetime> where (start_time <= datetime <= end_time)
    :param start_time:
    :param end_time:
    :return: list<datetime>
    """
    day_list = []
    while end_time >= start_time:
        day_list.append(start_time)
        start_time = start_time + datetime.timedelta(days=1)
    return day_list


def get_now():
    """
    当前时间
    :return: datetime
    """
    return datetime.datetime.now()


def get_time_by_offset(time, h_offset=0, m_offset=0, s_offset=0):
    """
    获取time的前后n小时/分钟/秒
    :param time: datetime
    :param h_offset: hour offset
    :param m_offset: minute offset
    :param s_offset: second offset
    :return: datetime
    """
    new_time = time + datetime.timedelta(hours=h_offset)
    new_time = new_time + datetime.timedelta(minutes=m_offset)
    new_time = new_time + datetime.timedelta(seconds=s_offset)
    return new_time


def get_date_by_offset(date, D_offset=0, M_offset=0, Y_offset=0):
    """
    获取date的前后n日/月/年
    :param date:
    :param D_offset: Day offset
    :param M_offset: Month offset
    :param Y_offset: Year offset
    :return: datetime
    """
    old_year = date.year
    old_month = date.month
    old_day = date.day
    new_year = old_year + Y_offset
    new_month = old_month + M_offset
    if new_month > 12:
        new_year += 1
        new_month -= 12
    new_day = old_day + D_offset
    new_date = date.replace(new_year, new_month, new_day)
    return new_date


def timestamp2str(timestamp):
    """
    :param timestamp:
    :return: str
    """
    try:
        d = datetime.datetime.fromtimestamp(timestamp)
        return d.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    thelist = get_each_day(datetime.datetime.strptime(
        '2017-12-01 01:00:00', DATETIME_FORMAT), datetime.datetime.now())
    for i in thelist:
        print(i.strftime(DATETIME_FORMAT))
    print((get_date_by_offset(datetime.datetime.now(), 1, 1, 1) - get_now()).days)
    print(timestamp2str(1524878239))
