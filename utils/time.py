from datetime import datetime, timedelta


def timedelta_to_hm(td):
    total_minutes = td.total_seconds() // 60
    hours, minutes = divmod(total_minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}"


def get_week_dates(base_date):
    start_date = base_date - timedelta(days=base_date.weekday() + 1)
    return [start_date + timedelta(days=i) for i in range(7)]

def split_time_range(time_range):
    split_time = time_range.split(' - ')

    start_time = split_time[0]
    end_time = split_time[1]

    return start_time, end_time
