from flask import Flask, request, jsonify
import mysql.connector
import pika
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s   ")

conn = mysql.connector.connect(
    user='sa',
    password='Password123!',
    host='dbbooks',
    database='books')

cursor = conn.cursor()
logging.info("Connessione al DB")

# connect to RabbitMQ and declare the queue
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
channel = connection.channel()

channel.queue_declare(queue='global_queue')


@app.route('/get')
def get_records():
    cursor.execute('SELECT * FROM books')
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/get/<int:id>')
def get_data_by_id(id):
    cursor.execute(f"SELECT * FROM books WHERE id = '{id}'")
    result = cursor.fetchone()
    return jsonify(result)


@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json()

    id = data.get('id')
    title = data.get('title')
    author = data.get('author')
    copies = data.get('copies')

    cursor.execute(
        f'''INSERT INTO books (id, title, author, copies) VALUES ('{id}','{title}' , '{author}', '{copies}')''')

    conn.commit()

    # RabbitMQ
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)

    return jsonify(data)


@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()

    id = data.get('id')
    title = data.get('title')
    author = data.get('author')
    copies = data.get('copies')

    cursor.execute(
        f'''UPDATE books SET title = '{title}', author = '{author}', copies = '{copies}' WHERE id = '{id}' ''')

    conn.commit()

    # RabbitMQ
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)

    return jsonify(data)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    cursor.execute(f"DELETE FROM books WHERE id = '{id}'")
    conn.commit()

    # RabbitMQ
    deleted_data = {'id': id}
    message = json.dumps(deleted_data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)

    return jsonify({'id': id})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
