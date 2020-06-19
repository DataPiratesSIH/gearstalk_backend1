import pika
import json

''' todo: fix file sending through rabbit'''

def rabbitmq_bridge(file,url):
    credentials = pika.PlainCredentials('test', 'test')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.1.1', credentials=credentials))                       #load_balancer url/ip in (host)
    channel = connection.channel()

    channel.queue_declare(queue='video_frame')

    # data = {
    #     "img" : file,
    # }
    message = json.dumps(data, ensure_ascii=False, indent=4)
    
    channel.basic_publish(exchange='', routing_key='video_frame', body=message)
    print(" [x] Sent The JSON Data")
    connection.close()


def rabbitmq_live(cam_id, lat, lng, url):
    credentials = pika.PlainCredentials('test', 'test')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.1.1', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='live_data')

    data = {
        "cam_id" : str(cam_id),
        "lat" : lat,
        "lng" : lng,
        "url" : url
    }
    message = json.dumps(data, ensure_ascii=False, indent=4)
    print(message)

    channel.basic_publish(exchange='', routing_key='live_data', body=message)
    print(" [x] Sent The JSON Data")
    connection.close()