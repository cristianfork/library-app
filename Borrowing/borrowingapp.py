import couchdb
from flask import Flask, request, jsonify


app = Flask(__name__)

couch = couchdb.Server(url='http://admin:Password123!@couchserver:5984')
db = couch['borrowings']

@app.route('/borrowings')
def get_borrowings():
    data = list(db.view('_all_docs', include_docs=True))
    return jsonify(data)

@app.route('/borrowings/<id>')
def get_borrowing(id):
    doc = db.get(id)

    if doc is None:
        return jsonify({'error': 'not found'}), 404
    return jsonify(doc)

@app.route('/create', methods=['POST'])
def create_borrowing():
    data = request.get_json()

    doc_id, doc_rev = db.save(data)

    return jsonify({'id': doc_id, 'rev': doc_rev})


@app.route('/delete/<doc_id>', methods=['DELETE'])
def delete_data(doc_id):

    if doc_id in db:
        doc = db[doc_id]
        db.delete(doc)
        return jsonify({'message': 'eliminated'})
    return jsonify({'error': 'Document not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')