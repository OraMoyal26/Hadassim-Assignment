from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['store_db']
suppliers_collection = db['suppliers']
orders_collection = db['orders']






@app.route('/register_supplier', methods=['POST'])
def register_supplier():
    data= request.json
    supplier= {
        "company_name": data['company_name'],
        "representative_name": data['representative_name'],
        "phone_number": data['phone_number'],
        "products": data['products']
    }
    suppliers_collection.insert_one(supplier)
    return jsonify({"Message": "Supplier registered successfully"}), 201








@app.route('/login_supplier',methods=['POST'])
def login_supplier():
    data= request.json
    supplier= suppliers_collection.find_one({
        "representative_name": data['representative_name'],
        "company_name": data['company_name']
    })

    if supplier:
        return jsonify({
            "company_name": supplier['company_name'],
            "phone_number": supplier['phone_number'],
            "representative_name": supplier['representative_name'],
            "products": supplier['products']
        }), 200
    else:
        return jsonify({"Error": "Supplier not found"}), 404






@app.route('/view_orders_for_supplier/<supplier_id>', methods=['GET'])
def view_orders_for_supplier(supplier_id):
    orders= orders_collection.find({"supplier_id": supplier_id})
    orders_list= []
    for order in orders:
        orders_list.append({
            "order_id": str(order['_id']),
            "status": order['status'],
            "products": order['products']
        })
    return jsonify(orders_list), 200






@app.route('/approve_order/<order_id>', methods=['PUT'])
def approve_order(order_id):
    order= orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        return jsonify({"Error": "Order not found"}), 404

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "In Process"}}
    )
    return jsonify({"Message": "Order status updated to 'In process'"}), 200









@app.route('/order', methods=['POST'])
def order():
    data= request.json
    order= {
        "supplier_id": data['supplier_id'],
        "status": "Pending",
        "products": data['products']
    }
    order_id= orders_collection.insert_one(order).inserted_id
    return jsonify({"Message": "Order placed successfully", "order_id": str(order_id)}), 201








@app.route('/view_orders', methods=['GET'])
def view_orders():
    orders= orders_collection.find({"status": {"$ne": "Completed"}})
    orders_list= []

    for order in orders:
        orders_list.append({
            "order_id": str(order['_id']),
            "supplier_id": order['supplier_id'],
            "status": order['status'],
            "products": order['products']
        })

    return jsonify(orders_list), 200









@app.route('/complete_order/<order_id>', methods=['PUT'])
def complete_order(order_id):
    order= orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        return jsonify({"Message": "Order not found!"}), 404

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "Completed"}}
    )

    return jsonify({"Message": "Order status updated to 'Completed'"}), 200













if __name__ == '__main__':
    app.run(debug=True)

