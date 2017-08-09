import time
from get_data import update_redis
while 1:
    print"start update redis"
    update_redis()
    print"complete update redis"
    time.sleep(10800)
