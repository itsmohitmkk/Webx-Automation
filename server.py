import datetime
from flask import Flask
from flask import request
from flask.json import jsonify
from automation import WebexAutomation

app = Flask(__name__)

running_automations = {}


def auth(token):
    return token == "jhf85yb#fl43d"


@app.route('/join', methods=['POST'])
def join_meeting():
    try:
        args = request.get_json()
        name = args["name"]
        email = args["email"]
        url = args["url"]
        header = request.headers
        auth_token = header["authentication"]
        if(auth(auth_token)):

            automation = WebexAutomation(url)
            length = len(running_automations)
            id = str(length + 1) + str(datetime.datetime.now())
            running_automations[id] = automation
            automation = running_automations[id]
            result, error = automation.joinMeeting(name, email)
            print(result, error)
            if result:
                return jsonify({"success": True, "message": "connected successfully", "id": id})
            return jsonify({"success": result, "error": error})

    except Exception as e:
        print(str(e))
        return jsonify({"success": False, "error": str(e)})


@app.route("/exit", methods=["POST"])
def exit_meeting():
    try:
        args = request.get_json()
        auth_token = request.headers["authentication"]
        id = str(args["id"])
        print("existing from meeting")
        print(running_automations)
        if(auth(auth_token) and running_automations.get(id) != None):
            print("founded")
            automation = running_automations[id]
            automation.close_meeting()
            return jsonify({"success": True, "message": "exited from meeting"})
        else:
            return jsonify({"success": False, "message": "Not a valid id or token"})
    except Exception as e:
        print(str(e))
        return jsonify({"success": False, "error": str(e)})


@app.route("/message", methods=["POST"])
def message():
    args = request.get_json()
    auth_token = request.headers["authentication"]
    id = str(args["id"])
    if(auth(auth_token) and running_automations.get(id) != None):

        automation = running_automations[id]
        result, error = automation.message(str(args["chat_message"]))
        if result:
            return jsonify({"success": True, "message": "messaeg sent successfully"})
        return jsonify({"success": result, "error": error})
    return jsonify({"success": False, "error": "Not valid"})


if __name__ == "__main__":
    app.run(debug=True, port=5003)
