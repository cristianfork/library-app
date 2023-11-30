import pika, sys, os
#import json

def main():


    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
    channel = connection.channel()

    channel.queue_declare(queue='global_queue')


    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='queue',
                        auto_ack=True,
                        on_message_callback=callback)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)