from flask import Flask, request

app = Flask(__name__)

@app.route('/flame-data', methods=['GET'])
def receive_flame_data():
    if request.method == 'GET':
        flame_status = request.form.get('flameStatus')
        print(flame_status)
        print("Received flame sensor status:", flame_status)
        # Process the received data here
        return 'Data received successfully', 200
    else:
        return 'Invalid request method', 405

if __name__ == '__main__':
    app.run(debug=True, port=9989)
