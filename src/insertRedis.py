import cont as cont
import content as content
import redis
import json
a = redis.Redis("127.0.0.1", "6379")
content.lpush('aiqicha_xinwenyuqing:start_urls', 'https://baidu.com/')  # 存入内容

a = redis.Redis("127.0.0.1", "6379")
content = {"url": 'https://www.baidu.com', "callback": "parse", }
content = json.dumps(cont)  # 将字典转化为json
a.sadd('task:百度:start_urls', content)  # 存入内容