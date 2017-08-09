# usr/bin/python
# encoding:utf-8



import json
import pika


def insert(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            '172.29.153.195'))
    channel = connection.channel()
    channel.queue_declare(queue='domain_queue', durable=True)  # 申明消息队列, 设置持久化存储
    channel.basic_publish(exchange='', routing_key='domain_queue', body=json.dumps(message))
    # print " [x] Sent 'Hello World!'"
    connection.close()


def recv():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            '172.29.153.195'))
    channel = connection.channel()
    channel.queue_declare(queue='domain_queue')

    channel.basic_consume(callback, queue='domain_queue', no_ack=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)


if __name__ == '__main__':
    domain_info = {'domain': 'baidu.cn', 'whois_server': 'whois.cnnic.cn'}
    insert(domain_info)
    recv()
