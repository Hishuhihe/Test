from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__)

@app.route('/api/showSerialpaso/', methods=['POST'])
def show_serial_paso():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.json
    file = data.get('file')
    app_env = data.get('app_env')
    contract_server = data.get('contract_server')

    if not all([file, app_env is not None, contract_server is not None]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Convert app_env and contract_server to strings for directory construction
    env_map = {0: "AWS", 1: "K5", 2: "T2"}
    server_map = {0: "app1", 1: "app2"}

    env = env_map.get(app_env, "")
    server = server_map.get(contract_server, "")

    # Construct the file path
    file_path = os.path.join("C:", "imprints_html_file", env, server, f"{file}.html")

    if not os.path.exists(file_path):
        return jsonify({
            "success": False,
            "filename": "",
            "message": "Seal Info response false"
        }), 200

    try:
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "filename": f"{file}.html",
            "content": content,
            "message": "Seal Info response successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "filename": "",
            "message": f"Error reading file: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(debug=True)