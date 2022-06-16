import calendar
import time

now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
year = time.strftime('%Y', time.localtime())
moth = time.strftime('%m', time.localtime())
day = time.strftime('%d', time.localtime())
h = time.strftime('%H',time.localtime())
yesterday = f'{year}-{moth}-{int(day) - 1}'
print(f'{yesterday} {h}')
print(now_time[0:12])