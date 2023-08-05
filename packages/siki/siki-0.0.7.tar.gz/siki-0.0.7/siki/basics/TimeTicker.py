# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: May 09, 2018
# Modifi: May 09, 2018

MS_PER_SECOND = 1000
MS_PER_MINUTE = 60000
MS_PER_HOUR = 3600000
MS_PER_DAY = 86400000

def tick_count():
    import time
    return time.time()

def current_timestamp(strMessage = None):
    import datetime
    if strMessage is None:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return "{0} {1}".format(timestamp, strMessage)


def current_year():
    from datetime import datetime
    return int(datetime.now().strftime("%Y"))


def current_month():
    from datetime import datetime
    return int(datetime.now().strftime("%m"))


def current_day():
    from datetime import datetime
    return int(datetime.now().strftime("%d"))


def current_hours():
    from datetime import datetime
    return int(datetime.now().strftime("%H"))


def current_minutes():
    from datetime import datetime
    return int(datetime.now().strftime("%M"))


def current_seconds():
    from datetime import datetime
    return int(datetime.now().strftime("%S"))


def current_milliseconds():
    from datetime import datetime
    return int(datetime.now().strftime("%f")[0:3])


if __name__ == "__main__":
    print(current_year())
    print(current_month())
    print(current_day())
    print(current_hours())
    print(current_minutes())
    print(current_seconds())
    print(current_milliseconds())