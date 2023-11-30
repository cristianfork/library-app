from flask import Flask, request, jsonify
import mysql.connector
import pika
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s   ")


conn = mysql.connector.connect(
    user='sa',
    password='Password123!',
    host='dbcustomers',
    database='customers')

cursor = conn.cursor()
logging.info("Connessione al DB")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
channel = connection.channel()

channel.queue_declare(queue='global_queue')

@app.route('/get')
def get_records():

    cursor.execute('SELECT * FROM customers')
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/get/<int:id>')
def get_data_by_id(id):
    cursor.execute(f"SELECT * FROM customers WHERE id = '{id}'")
    result = cursor.fetchone()

    return jsonify(result)


@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json()

    id = data.get('ID')
    name = data.get('Name')
    surname = data.get('Surname')
    mail = data.get('Mail')

    cursor.execute(f'''INSERT INTO customers (ID, Name, Surname, Mail) VALUES ('{id}','{name}' , '{surname}', '{mail}')''' )

    conn.commit()
    
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)
    
    return 'success'


@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    
    id = data.get('ID')
    name = data.get('Name')
    surname = data.get('Surname')
    mail = data.get('Mail')

    cursor.execute(f'''UPDATE customers SET Name = '{name}', Surname = '{surname}', Mail = '{mail}' WHERE ID = '{id}' ''')

    conn.commit()

    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)
    
    return 'success'


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    
    cursor.execute(f"DELETE FROM customers WHERE id = '{id}'")
    conn.commit()

    deleted_data = {'id': id}
    message = json.dumps(deleted_data)
    channel.basic_publish(exchange='', routing_key='global_queue', body=message)

    return jsonify({'id': id})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
