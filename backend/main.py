from flask import Flask, request, send_file
from flask_restful import Api, Resource
import os
import random
import string
import time
from methods import actionDB

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

time_delay = dict()

def generate_random_filename():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))

def check_delay(token):
    if time_delay.get(token) is None: time_delay[token] = time.time() - 1

    if (time.time() - time_delay[token]) > 0:
        time_delay[token] = time.time() + 3
        return True
    else:
        return False

class uploadFiles(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part"}

        token_user = request.args.get('token')
        user_data = actionDB.get_account(token=token_user)

        if request.args.get('token') is None or len(user_data) == 0:
            return {"message": "No token passed"}

        file = request.files['file']

        if file.filename == '':
            return {"message": "No selected file"}

        check = check_delay(token_user)
        print(check)
        if not check: return {"code": 41, "message": "Please wait before downloading the file again."}, 418

        if file:
            file.filename = file.filename.split('/')[-1]
            private = request.args.get('private', 0)
            folder_id = request.args.get('folder_id', 0)
            filename = generate_random_filename() + '-' + file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_id = actionDB.get_unique_id("files") + 1
            file.save(file_path)

            file.seek(0, 2)
            file_size = file.tell()
            file.seek(0)
            actionDB.save_file(filename, file_size, user_data[0], folder_id, private)

            return {"folder_id": folder_id, "file_id": file_id, "file_name": filename, "url": f"http://sab.purpleglass.ru/uploads/{filename}", "size": file_size, "private": private}, 200

class downloadFile(Resource):
    def get(self, filename):
        token_user = request.args.get('token')
        user_data = actionDB.get_account(token=token_user)
        file_data = actionDB.get_file(file_name = filename)
        print(user_data)
        print(file_data)

        if not file_data:
            return {"message": "Info of file not found"}, 404

        if file_data[5]:
            if request.args.get('token') is None or len(user_data) == 0:
                return {"message": "No token passed"}, 401
            if file_data[4] != user_data[0]:
                return {"message": "permission denied"}, 401

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path, as_attachment=True)


class Accounts(Resource):
    def post(self):
        login = request.args.get("login")
        password = request.args.get("password")

        if len(login) < 8 or len(password) < 8: return {"code": 1, "message": "слишком мало букавк"}, 400
        if not login or not password:
            return {"code": 5, "message": "some parametr missed"}, 402
        user_data = actionDB.get_account(login)
        if user_data:
            return {"code": 6,"message": "login was already used"}, 401
        token = actionDB.create_user(login, password)

        return {"token": token}

    def get(self):
        login = request.args.get("login")
        password = request.args.get("password")

        if not login or not password:
            return {"code": 5, "message": "some parametr missed"}

        user_data = actionDB.get_account(login=login, password=password, get_user=True)

        if not user_data:
            return {"code": 4, "message": "user not found"}, 404

        return {"id": user_data[0],
                "token": user_data[3]}


class Files(Resource):
    def get(self):
        token_user = request.args.get('token')
        user_data = actionDB.get_account(token=token_user)
        print(user_data)

        if request.args.get('token') is None or user_data is None:
            return {"message": "No token passed"}, 401
        print(user_data)

        files_data = actionDB.get_files_user(user_data[0])
        items = []
        for file in files_data:
            items.append(
                {
                    "folder_id": file[1],
                    "file_id": file[0],
                    "file_name": file[2],
                    "url": "http://sab.purpleglass.ru/uploads/" + file[2],
                    "size": file[3],
                    "private": file[5]
                }
            )

        return {"items": items}

    def delete(self):
        token_user = request.args.get('token')
        file_id = request.args.get('file_id')

        user_data = actionDB.get_account(token=token_user)
        file_data = actionDB.get_file(file_id = file_id)

        if request.args.get('token') is None or user_data is None:
            return {"message": "No token passed"}, 401

        if not file_data: return {"message": "The file id parameter was not passed"}, 404
        if file_data[4] != user_data[0]:
            return {"message": "permission denied"}, 401

        actionDB.delete_file(file_id)
        return {"message": "я chmo"}, 200


api.add_resource(uploadFiles, '/upload')
api.add_resource(downloadFile, '/uploads/<filename>')
api.add_resource(Accounts, "/accounts")
api.add_resource(Files, "/uploads/files")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port='3555', debug=False)
