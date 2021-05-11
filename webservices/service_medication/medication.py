'''
Medication Service. Provides Category & Medication API as described on def index()


'''
from flask import Flask
from flask import request
from flask import jsonify
from flask import json
import os
import sqlite3
import uuid
import pika
import sys
import json
import datetime
import threading

app = Flask(__name__)
postgres_address = "msdemo-db-medication"

@app.route('/', methods=['GET'])
def index():
  services = {  
    "get-medications": {
      "CategoryId": "string"
    },
    "get-all-medications": {
      
    },
    "get-medication-details": {
      "MedicationId": "string"
    },
    "add-new-medication": {
      "Name": "string",
      "Description": "string",
      "Supplier": "string",
      "CategoryId": "string",
      "Price": "double",
      "UnitsInStock": "int"
    },
    "update-medication": {
      "MedicationId": "string",
      "Name": "string",
      "Description": "string",
      "Supplier": "string",
      "Category": "string",
      "Price": "double",
      "UnitsInStock": "int"
    },
    "delete-medication": {
      "MedicationId": "string"
    },    
    "get-categories": {
      
    },
    "add-new-category": {      
      "Name": "string",     
    },
    "update-category": {
      "CategoryId": "string",
      "Name": "string",     
    },
    "delete-category": {
      "CategoryId": "string"
    }    
  }
  
  return jsonify(services=services), 200

@app.route('/get-medications/', methods=['GET'])
def get_medications():              
  db_connection = create_connection()
  cursor = db_connection.cursor()
  category_id = request.json['CategoryId']  
  print(category_id)
  cursor.execute("SELECT Medications.*, Categories.Name \
      FROM Medications INNER JOIN Categories on Medications.CategoryId=Categories.CategoryId WHERE Categories.CategoryId==?", (category_id,)) 
  rows = cursor.fetchall()
  result = {}
  if len(rows) == 0:
    result['Status'] = 'Not Found'
  else:
    result['Status'] = 'Success'
    result['Medications'] = rows
  return jsonify(result=result), 200

@app.route('/get-all-medications/', methods=['GET'])
def get_all_medications():              
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("SELECT Medications.*, Categories.Name \
      FROM Medications INNER JOIN Categories on Medications.CategoryId=Categories.CategoryId") 
  rows = cursor.fetchall()
  result = {}
  if len(rows) == 0:
    result['Status'] = 'Not Found'
  else:
    result['Status'] = 'Success'
    result['Medications'] = rows
  return jsonify(result=result), 200

@app.route('/get-medication-details/', methods=['GET'])
def get_medication_details():            
  db_connection = create_connection()
  cursor = db_connection.cursor()
  medication_id = request.json['MedicationId']  
  cursor.execute("SELECT Medications.*, Categories.Name \
      FROM Medication INNER JOIN Categories on Medication.CategoryId=Categories.CategoryId WHERE MedicationId==?", (medication_id,))   
  medication = cursor.fetchone()
  result = {}
  if medication is None:
    result['Status'] = 'Not Found'
  else:
    result['Status'] = 'Success'    
    result['Medication'] = medication
  return jsonify(result=result), 200

@app.route('/add-new-medication/', methods=['POST'])
def add_new_medication():
  store_data = {}
  store_data['Action'] = "Add New Medication"
  store_data['MedicationId'] = str(uuid.uuid4())
  store_data['Name'] = request.json['Name']
  store_data['Description'] = request.json['Description']
  store_data['Supplier'] = request.json['Supplier']
  store_data['CategoryId'] = request.json['CategoryId']
  store_data['Price'] = request.json['Price']
  store_data['UnitsInStock'] = request.json['UnitsInStock']
  send_event_store_data("add_medication", store_data)    
  return jsonify(result='Success'), 200

@app.route('/update-medication/', methods=['POST'])
def update_medication():
  store_data = {}
  store_data['Action'] = "Update Medication"
  store_data['MedicationId'] = request.json['MedicationId']
  store_data['Name'] = request.json['Name']
  store_data['Description'] = request.json['Description']
  store_data['Supplier'] = request.json['Supplier']
  store_data['CategoryId'] = request.json['CategoryId']
  store_data['Price'] = request.json['Price']
  store_data['UnitsInStock'] = request.json['UnitsInStock']
  send_event_store_data("update_medication", store_data)    
  return jsonify(result='Success'), 200

@app.route('/delete-medication/', methods=['POST'])
def delete_medication():
  store_data = {}
  store_data['Action'] = "Delete Medication"
  store_data['MedicationId'] = request.json['MedicationId']
  send_event_store_data("delete_medication", store_data)  
  return jsonify(result='Success'), 200

@app.route('/get-categories/', methods=['GET'])
def get_categories():          
  db_connection = create_connection()
  cursor = db_connection.cursor()
  cursor.execute("SELECT * FROM Categories") 
  rows = cursor.fetchall()
  result = {}
  if len(rows) == 0:
    result['Status'] = 'Not Found'
  else:
    result['Status'] = 'Success'
    result['Categories'] = rows
  return jsonify(result=result), 200

@app.route('/get-category-details/', methods=['GET'])
def get_category_details():          
  db_connection = create_connection()
  cursor = db_connection.cursor()
  cursor.execute("SELECT * FROM Categories WHERE CategoryId=?", (request.json['CategoryId'],))   
  rows = cursor.fetchall()
  result = {}
  if len(rows) == 0:
    result['Status'] = 'Not Found'
  else:
    result['Status'] = 'Success'
    result['Category'] = rows[0]
  return jsonify(result=result), 200

@app.route('/add-new-category/', methods=['POST'])
def add_new_category():
  store_data = {} 
  store_data['Action'] = "Add New Category"
  store_data['CategoryId'] = str(uuid.uuid4())
  store_data['Name'] = request.json['Name']  
  send_event_store_data("add_category", store_data)    
  return jsonify(result='Success'), 200

@app.route('/update-category/', methods=['POST'])
def update_category():
  store_data = {} 
  store_data['Action'] = "Update Category"
  store_data['CategoryId'] = request.json['CategoryId']
  store_data['Name'] = request.json['Name']  
  send_event_store_data("update_category", store_data)    
  return jsonify(result='Success'), 200
  
@app.route('/delete-category/', methods=['POST'])
def delete_category():
  store_data = {} 
  store_data['Action'] = "Delete Category"
  store_data['CategoryId'] = request.json['CategoryId']  
  send_event_store_data("delete_category", store_data)    
  return jsonify(result='Success'), 200

def create_tables():
  db_connection = create_connection()  
  create_orders_table_sql = 'CREATE TABLE IF NOT EXISTS Medications' \
        '(id INTEGER PRIMARY KEY AUTOINCREMENT       NOT NULL,' \
        'MedicationId       TEXT       NOT NULL,' \
        'Name            TEXT       NOT NULL,'  \
        'Description     TEXT       NOT NULL,' \
        'Supplier        TEXT       NOT NULL,' \
        'CategoryId      TEXT       NOT NULL,' \
        'PRICE           FLOAT      NOT NULL,' \
        'UnitsInStock    INT        NOT NULL)'

  create_categories_table_sql = 'CREATE TABLE IF NOT EXISTS Categories' \
        '(id INTEGER PRIMARY KEY AUTOINCREMENT       NOT NULL,' \
        'CategoryId      TEXT       NOT NULL,' \
        'Name            TEXT       NOT NULL)'

  cursor = db_connection.cursor()
  cursor.execute(create_orders_table_sql)
  cursor.execute(create_categories_table_sql)

def test_tables():
  db_connection = create_connection()  
  print("test")
  category_id = 'cat1'
  cursor = db_connection.cursor()
  cursor.execute("SELECT * from Medications WHERE CategoryId==?", (category_id,)) 
  rows = cursor.fetchall()  
  print(len(rows))
  for row in rows:
    print(row[0])
    print(row[1])
    print(row[2])

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
      return sqlite3.connect(database=os.environ["DATABASE_NAME"])
    except Exception as e:
      print(e)
    return None

#Database functions
def event_add_new_medication(medication_info):
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("INSERT INTO Medications(MedicationId, Name, Description, Supplier, CategoryId, Price, UnitsInStock) Values (?,?,?,?,?,?,?)", 
             (medication_info['MedicationId'], 
             medication_info['Name'], medication_info['Description'], 
             medication_info['Supplier'], medication_info['CategoryId'], 
             medication_info['Price'], medication_info['UnitsInStock'],)) 
  db_connection.commit()
  db_connection.close()    
  print("event_add_new_medication Fail" if cursor.rowcount <= 0 else "event_add_new_medication Success")  

def event_update_medication(medication_info):
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("UPDATE Medications SET Name=?, Description=?, Supplier=?, CategoryId=?, Price=?, UnitsInStock=? WHERE MedicationId=?", 
             (medication_info['Name'], medication_info['Description'], 
             medication_info['Supplier'], medication_info['CategoryId'], 
             medication_info['Price'], medication_info['UnitsInStock'],
             medication_info['MedicationId'],)) 
  db_connection.commit()
  db_connection.close()    
  print("event_update_medication Fail" if cursor.rowcount <= 0 else "event_update_medication Success")  

def event_delete_medication(medication_info):
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("DELETE FROM Medications WHERE MedicationId=?", (medication_info['MedicationId'],))   
  db_connection.commit()  
  db_connection.close()      
  print("event_delete_medication Fail" if cursor.rowcount <= 0 else "event_delete_medication Success")  

def event_add_new_category(category_info):
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("INSERT INTO Categories(CategoryId, Name) Values (?,?)", (category_info['CategoryId'], category_info['Name'])) 
  db_connection.commit()
  db_connection.close()  
  print("event_add_new_category Fail" if cursor.rowcount <= 0 else "event_add_new_category Success")  

def event_update_category(category_info):
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("UPDATE Categories Set Name=? WHERE CategoryId=?", (category_info['Name'], category_info['CategoryId'],))
  db_connection.commit()
  db_connection.close() 
  print("event_update_category Fail" if cursor.rowcount <= 0 else "event_update_category Success")  
  
def event_delete_category(category_info):  
  db_connection = create_connection()
  cursor = db_connection.cursor()  
  cursor.execute("DELETE FROM Categories WHERE CategoryId=?", (category_info['CategoryId'],)) 
  db_connection.commit()
  db_connection.close()    
  print("event_delete_category Fail" if cursor.rowcount <= 0 else "event_delete_category Success")  

bus_user_name = os.environ["EVENT_BUS_USERNAME"]
bus_password = os.environ["EVENT_BUS_PASSWORD"]
bus_hostname = os.environ["EVENT_BUS_IP"]

credentials = pika.PlainCredentials(username=bus_user_name, password=bus_password)
parameters = pika.ConnectionParameters(bus_hostname, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

#Event Bus Addressing
send_queue_name = "msdemo_queue_event_store"
send_exchange_name = "msdemo_exchange_event_store"
send_routing_key = "msdemo_routingkey_event_store"

receive_queue_name = "msdemo_queue_medication"
receive_exchange_name = "msdemo_exchange_medication"
receive_routing_key = "msdemo_routingkey_medication"

exchange_name_order = "msdemo_exchange_order"

saga_exchange_name_order = "msdemo_exchange_saga_order"
saga_routing_key_order = "msdemo_routingkey_saga_order"
saga_routing_key_orderresponse = "msdemo_routingkey_saga_orderresponse"


def listener_callback(ch, method, properties, body):    
  response_json = json.loads(body)
  print("Listener Callback Key:{0} Json:{1}".format(method.routing_key, response_json))
  print(response_json)
  if (method.routing_key == receive_routing_key):
    if (response_json['Data']['Action'] == "Add New Medication"):
      event_add_new_medication(response_json['Data'])
    elif (response_json['Data']['Action'] == "Update Medication"):
      event_update_medication(response_json['Data'])
    elif (response_json['Data']['Action'] == "Delete Medication"):
      event_delete_medication(response_json['Data'])
    elif (response_json['Data']['Action'] == "Add New Category"):
      event_add_new_category(response_json['Data'])
    elif (response_json['Data']['Action'] == "Update Category"):
      event_update_category(response_json['Data'])
    elif (response_json['Data']['Action'] == "Delete Category"):
      event_delete_category(response_json['Data'])
  elif (method.routing_key == saga_routing_key_order):
    print("Processing Order Placed. Event:{0}".format(response_json['Event']))
    if (response_json['Event'] == "OrderPlaced"):
      event_new_order_placed(response_json['Data'])
    elif (response_json['Event'] == "OrderFinalized"):
      event_order_finalized(response_json['Data'])

def event_new_order_placed(message):  
  print("event_new_order_placed:" + message) 
  message_json = json.loads(message)
  data_json = json.loads(message_json['Data'])  
  db_connection = create_connection()      
  cursor = db_connection.cursor()
  cursor.execute("SELECT * from Medications WHERE MedicationId==?", (data_json['MedicationId'],)) 
  rows = cursor.fetchall()    
  for row in rows:    
    app.logger.info('event_new_order_placed found row: %s', row)  
    result = { "OrderID": data_json['OrderID'], "Stock":row[7], "Price":row[6] }
    send_order_saga_data("PriceAndStock", json.dumps(result))
    break

def event_order_finalized(message):
  print("event_order_finalized:" + message) 
  message_json = json.loads(message)
  data_json = json.loads(message_json['Data']) 
  db_connection = create_connection()       
  cursor = db_connection.cursor()
  print("A: {0} PID: {1}".format(data_json['Amount'], data_json['MedicationId']))
  cursor.execute("UPDATE Medications SET UnitsInStock = UnitsInStock - ? WHERE MedicationId==?", (data_json['Amount'], data_json['MedicationId'],)) 
  db_connection.commit()
  db_connection.close()    
  
def init_event_bus():
  threading.Thread(target=start_listener).start() 
  start_sender()

def start_listener():
  #Receive from Event Store  
  receive_channel = connection.channel()
  receive_channel.exchange_declare(exchange=receive_exchange_name, exchange_type='direct')
  receive_channel.exchange_declare(exchange=saga_exchange_name_order, exchange_type='direct')

  receive_channel.queue_declare(
                queue=receive_queue_name, 
                durable=True,
                exclusive=False,
                auto_delete=False,
                arguments=None)

  receive_channel.queue_bind(exchange=receive_exchange_name,
                    queue=receive_queue_name,
                    routing_key=receive_routing_key)

  receive_channel.queue_bind(exchange=saga_exchange_name_order,
                    queue=receive_queue_name,
                    routing_key=saga_routing_key_order)

  receive_channel.basic_qos(prefetch_size=0, prefetch_count=1)
  receive_channel.basic_consume(listener_callback, queue=receive_queue_name, no_ack=True)
  receive_channel.start_consuming()              
 
send_channel = connection.channel()

def start_sender():
  #Send to Event Store  
  send_channel.exchange_declare(exchange=send_exchange_name, exchange_type='direct')
  send_channel.queue_declare(queue=send_queue_name, durable=True, exclusive=False, auto_delete=False, arguments=None)
  send_channel.queue_bind(queue=send_queue_name, exchange=send_exchange_name, routing_key=send_routing_key)

def send_event_store_data(event_type, data):
  item = {}
  item_data = {}
  item["Aggregate"] = "Medication"
  item["Topic"] = "msdemo_topic.medication.{0}".format(event_type)
  item["Timestamp"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")  
  item["Version"] = "1.0"
  item["BUS_ExchangeName"] = receive_exchange_name
  item["BUS_Queue"] = receive_queue_name
  item["BUS_RoutingKey"] = receive_routing_key
  item["Data"] = data
  message = json.dumps(item)
  print(message)
  try:
    send_channel.basic_publish(exchange=send_exchange_name,
                        routing_key=send_routing_key,
                        body=message,
                        properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                        ))
  except pika.exceptions.ConnectionClosed:
    print("send_event_store_data Exception. Connection closed")
  except:
    print("send_event_store_data Exception")

def send_order_saga_data(event_type, data): 
  print("send_order_saga_data type:{0} data:{1}".format(event_type, data))
  item = {}
  item_data = {}
  item["Event"] = event_type
  item["Data"] = data
  message = json.dumps(item)
  print(message)
  try:
    send_channel.basic_publish(exchange=exchange_name_order,
                        routing_key=saga_routing_key_orderresponse,
                        body=message,
                        properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                        ))
  except pika.exceptions.ConnectionClosed:
    print("send_order_saga_data Exception. Connection closed")
  except:
    print("send_order_saga_data Exception")

if __name__ == "__main__": 
  create_tables()    
  init_event_bus()
  app.run(host="0.0.0.0", port=80, debug=True)  