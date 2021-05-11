'''
e-Commerce Website. Users may; 
- Login, Logout
- View, Edit, Delete Medications and Categories 
- View Patients, Edit Their Credits

'''

from flask import Flask, request, flash, render_template, json, jsonify, session, abort
import requests
import os

app = Flask(__name__ )

proxy_address = os.environ["SERVICE_REGISTRY"] 

def login_request(user_name, password):
  response = requests.post("{}/medication/login-user/".format(proxy_address), json={"UserName":user_name, "Password": password} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def get_categories_request():    
  response = requests.get("{}/medication/get-categories/".format(proxy_address))  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def get_category_details_request(category_id):    
  response = requests.get("{}/medication/get-category-details/".format(proxy_address), json={"CategoryId":category_id})
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code    

def add_category_request(category_name):
  response = requests.post("{}/medication/add-new-category/".format(proxy_address), json={"Name":category_name} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code    

def edit_category_request(category_id, category_name):
  response = requests.post("{}/medication/update-category/".format(proxy_address), json={"CategoryId":category_id, "Name":category_name} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code    

def delete_category_request(category_id):
  response = requests.post("{}/medication/delete-category/".format(proxy_address), json={"CategoryId":category_id} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code   

def add_medication_request(name, description, supplier, category_id, price, unitsinstock):
  response = requests.post("{}/medication/add-new-medication/".format(proxy_address), 
      json={"Name":name, "Description":description, "Supplier":supplier, "CategoryId":category_id, "Price":price, "UnitsInStock":unitsinstock} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code    

def edit_medication_request(id, name, description, supplier, category_id, price, unitsinstock):
  response = requests.post("{}/medication/update-medication/".format(proxy_address), 
      json={"MedicationId":id, "Name":name, "Description":description, "Supplier":supplier, "CategoryId":category_id, "Price":price, "UnitsInStock":unitsinstock} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code    

def delete_medication_request(medication_id):
  response = requests.post("{}/medication/delete-medication/".format(proxy_address), json={"MedicationId":medication_id} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code   

def get_all_medications_request():    
  response = requests.get("{}/medication/get-all-medications/".format(proxy_address))  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def get_medication_details_request(medication_id):    
  response = requests.get("{}/medication/get-medication-details/".format(proxy_address), json={"MedicationId":medication_id})
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def get_medications_of_category_request(category_id):
  response = requests.get("{}/medication/get-medications/".format(proxy_address), json={"CategoryId":category_id} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code   

def get_patients_request():    
  response = requests.get("{}/patient/get-all-users/".format(proxy_address))  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def get_user_info(user_name):    
  response = requests.get("{}/patient/get-user/{}".format(proxy_address, user_name))  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def edit_user_credit_request(user_name, credit):
  response = requests.post("{}/patient/set-credit/".format(proxy_address), json={"UserName":user_name, "Credit":credit} )  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

def update_user(user_name, password, fullname, email):
  updated_user = {
    "UserName": user_name, 
    "Password": password, 
    "FullName": fullname,
    "Email": email, 
    "Credit": "100" 
  }
  response = requests.post("{}/manager/update-user/".format(proxy_address), json=updated_user)  
  if response.status_code == 200:
    return json.loads(response.content.decode('utf-8')), 200
  return "service call fail", response.status_code  

@app.route('/')
def home():  
  return render_template('index.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
  if (check_login() == True):
    flash("User already logged in") 
    return home()
  if request.method == 'POST':
    result, code = login_request(request.form['username'], request.form['password'])
    if (request.form['username'] == "admin" and request.form['password'] == "pass"):
      session['username'] = request.form['username']
      session['logged_in'] = True    
    return home()
  else:
    return render_template('login.html')

@app.route("/logout")
def logout():
  session['logged_in'] = False
  session['username'] = ""
  return home()

@app.route("/categories", methods=['GET']) 
def categories():   
  if (check_login() == False):
    flash("User not logged in") 
    return home()
  result, code = get_categories_request()  
  print(result)
  category_list = {}
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      category_list = result['result']['Categories']      
  return render_template('categories.html', categories=category_list)

@app.route("/edit-category", methods=['GET', 'POST']) 
def edit_category():    
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    edit_category_request(request.form['categoryid'], request.form['categoryname'])    
    return home()
  result, code = get_category_details_request(request.args.get('id'))
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      category_name = result['result']['Category'][2]
      return render_template('editcategory.html', category_id=request.args.get('id'), category_name=category_name)
  return home()

@app.route("/delete-category", methods=['GET', 'POST']) 
def delete_category():      
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    delete_category_request(request.form['categoryid'])    
    return home()
  result, code = get_category_details_request(request.args.get('id'))
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      category_name = result['result']['Category'][2]
      return render_template('deletecategory.html', category_id=request.args.get('id'), category_name=category_name)
  return home()

@app.route("/add-category", methods=['GET', 'POST']) 
def add_category():      
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    add_category_request(request.form['categoryname'])
  return render_template('addcategory.html')

@app.route("/view-medications/<id>", methods=['GET']) 
def view_medications(id):      
  if (check_login() == False):
    flash("User not logged in") 
    return home()
  result, code = get_medications_of_category_request(id)    
  medication_list = {}
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      medication_list = result['result']['Medications']      
  return render_template('medications.html', medications=medication_list)

@app.route("/medications", methods=['GET']) 
def medications():    
  if (check_login() == False):
    flash("User not logged in") 
    return home()
  result, code = get_all_medications_request()    
  medication_list = {}
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      medication_list = result['result']['Medications']      
  return render_template('medications.html', medications=medication_list)

@app.route("/add-medication", methods=['GET', 'POST']) 
def add_medication():    
  if (check_login() == False):
    flash("User not logged in") 
    return home()     
  category_list = {}
  result, code = get_categories_request()      
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      category_list = result['result']['Categories']        
  if request.method == 'POST':
    add_medication_request(
      request.form['medicationname'], request.form['description'], request.form['supplier'],
      request.form['select_category'], request.form['price'], request.form['unitsinstock'])        
  return render_template('addmedication.html', categories=category_list)  

@app.route("/edit-medication", methods=['GET', 'POST']) 
def edit_medication():    
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    edit_medication_request(
      request.form['medicationid'], request.form['medicationname'], request.form['description'], request.form['supplier'],
      request.form['select_category'], request.form['price'], request.form['unitsinstock']) 
    return home()  
  result, code = get_medication_details_request(request.args.get('id'))
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):        
      result_cat, code_cat = get_categories_request()      
      category_list = {}
      if (code_cat == 200):
        if (str(result_cat['result']['Status']) == "Success"):  
          category_list = result_cat['result']['Categories']        
      return render_template('editmedication.html', medication=result['result']['Medication'], categories=category_list)
  return home()

@app.route("/delete-medication", methods=['GET', 'POST']) 
def delete_medication():    
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    delete_medication_request(request.form['medicationid'])    
    return home()
  result, code = get_medication_details_request(request.args.get('id'))
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      medication_name = result['result']['Medication'][2]
      return render_template('deletemedication.html', medication_id=request.args.get('id'), medication_name=medication_name)
  return home()

@app.route("/patients", methods=['GET']) 
def patients():    
  if (check_login() == False):
    return home()
  result, code = get_patients_request()
  patient_list = {}
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):  
      patient_list = result['result']['Users']  
  print(patient_list)    
  return render_template('patients.html', patients=patient_list)  

@app.route("/edit-patient-credit", methods=['GET', 'POST']) 
def edit_patient_credit():    
  if (check_login() == False):
    return home()
  if request.method == 'POST':
    edit_user_credit_request(request.form['username'], request.form['credit'])
    return home()  
  result, code = get_user_info(request.args.get('id'))
  if (code == 200):
    if (str(result['result']['Status']) == "Success"):        
      result_cat, code_cat = get_user_info(request.args.get('id'))      
      if (code_cat == 200):
        if (str(result_cat['result']['Status']) == "Success"):            
          user_info = {}
          user_info['UserName'] = result['result']['User Info']['UserName']
          user_info['FullName'] = result['result']['User Info']['FullName']
          user_info['Credit'] = result['result']['User Info']['Credit']
          return render_template('editpatientcredit.html', patient=user_info)
  return home()

def check_login():
  if session.get('logged_in') is None:    
    return False
  if session['logged_in'] == False:      
    return False
  return True

if __name__ == "__main__":  
  app.secret_key = os.urandom(12)
  app.run(host="0.0.0.0", port=80, debug=True)
