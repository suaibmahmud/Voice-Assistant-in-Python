import datetime

date = datetime.datetime.now()

def current_date():
    year, month, day = date.year, date.month, date.day
    
    month_name = ""
    final_date = ""

    if month == 1:
        month_name = "January"
    elif month == 2:
        month_name = "February"
    elif month == 3:
        month_name = "March"
    elif month == 4:
        month_name = "April"
    elif month == 5:
        month_name = "May"
    elif month == 6:
        month_name = "June"
    elif month == 7:
        month_name = "July"
    elif month == 8:
        month_name = "August"
    elif month == 9:
        month_name = "September"
    elif month == 10:
        month_name = "October"
    elif month == 11:
        month_name = "November"
    elif month == 12:
        month_name = "December"

    final_date = f"{month_name} {day}, {year}"

    return final_date

def current_day():
    weekday = date.strftime("%A")
    return weekday

def current_time():
    time = date.strftime("%X")
    hr = int(time.split(":")[0])
    min = int(time.split(":")[1])

    suffix = ""
    final_time = ""

    if hr > 12:
        hr = hr - 12
        suffix = "PM"
    else:
        suffix = "AM"
    
    if hr == 0:
        hr = 12
        suffix = "AM"

    final_time = f"{hr}:{min} {suffix}"

    return final_time