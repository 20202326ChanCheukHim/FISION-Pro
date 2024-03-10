from flask import Flask, jsonify, request
import common
from flask_cors import CORS

app =  Flask(__name__, static_folder='statics')


#Cross Origin Resource Sharing (one domain call api from another domain [3000 call 5500])
# CORS(app)
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response


@app.route('/pingFlask')
def ping_flask():
    return jsonify({'message': 'Ping from Flask!'})

@app.route('/pingMongo', methods=['GET'])
def pingMongo():
    try:
        print("ping PingMongo called")
        db = common.mongodb_connect()
        collection_names = db.list_collection_names()
        return jsonify({"Collections": collection_names}), 200
    except Exception as e:
        return jsonify({"error": "Failed to connect to MongoDB"}), 500



@app.route('/login' , methods=['POST'])
def login(): 
    db = common.mongodb_connect()
    data = request.get_json(force=True)
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        print("Username:" +str(username))
        print("Password:" +str(password))


        hashed_password = str(common.simple_hash(password, 7))
        # print("hashed_password for login: " + str(hashed_password))

        # print("In DB: "+ str(db["User_Inventory"].find_one({"username": username})["password"]))
        # print(hashed_password == db["User_Inventory"].find_one({"username": username})["password"])

        # Empty Input
        if username == "" or hashed_password == "":
            return jsonify({"message": "Empty Input"}), 400
        
        # User not exist
        if (username == '') or (db["User_Inventory"].find_one({"username": username}) is None):
            return jsonify({"message": "User doesn't not exist"}), 400
        
        # Password Wrong
        if (hashed_password != "") and (hashed_password != str(db["User_Inventory"].find_one({"username": username})["password"])):
            return jsonify({"message":"Wrong Password for " + username}), 400
        
       # Successful Case
        if (hashed_password != "") and (hashed_password == db["User_Inventory"].find_one({"username": username})["password"]):
            return jsonify({"message": username + " has successfully logged in"}), 200
    else: 
        return jsonify({"message": exceptions["invalid_request_body"]}), 400
    return jsonify({"message": "Login is somehow not successful, Try again"}), 400


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = data['username']
    password = data['password']
    password = str(common.simple_hash(password,7))


    db = common.mongodb_connect()

    if not db["User_Inventory"].find_one({"username": username}) is None:
        return jsonify(exceptions["duplicated_username"]), 500

    db["User_Inventory"].insert_one({"username": username, "password": password})
    # private_key, token = otp_encrypt.otp_init("token", 7)
    # db["tokens"].insert_one(
    #     {"username": username, "private_key": private_key, "token": ""})

    return jsonify({'message': 'Successfully registered with pw: ' + password}), 200



exceptions = {
    "incorrect_password": {"message": "Please check your username and password"},
    "incorrect_token": {"message": "Please login"},
    "invalid_input": {"message": "Please check your input"},
    "invalid_ip": {"message": "Please check your requested ip"},
    "duplicated_request": {"message": "Requested core switch has been added"},
    "object_id_not_found": {"message": "Please check object id"},
    "duplicated_username": {'message': 'Your username has been used'},
    "duplicated_rack_number": {'message': "rack_number_i duplicated!"},
    "incorrect_rack_number": {"message": "Invalid rack string format"},
    "incorrect_rack_prefix": {"message": "Rack prefixes do not match"},
    "invalid_request_body": {"message": "Invalid request body"}
}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5500)