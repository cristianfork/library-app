from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    user='sa',
    password='Password123!',
    host='dbbooks',
    database='books')

cursor = conn.cursor()


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

    cursor.execute(f'''INSERT INTO books (id, title, author, copies) VALUES ('{id}','{title}' , '{author}', '{copies}')''' )

    conn.commit()
    return jsonify(data)


@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    
    id = data.get('id')
    title = data.get('title')
    author = data.get('author')
    copies = data.get('copies')

    cursor.execute(f'''UPDATE books SET title = '{title}', author = '{author}', copies = '{copies}' WHERE id = '{id}' ''')

    conn.commit()
    return jsonify(data)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    cursor.execute(f"DELETE FROM books WHERE id = '{id}'")
    conn.commit()
    return jsonify({'id': id})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
