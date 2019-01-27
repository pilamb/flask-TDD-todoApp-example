from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/todolist_c/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucket_list = Bucketlist(name=name)
                bucket_list.save()
                response = jsonify({
                    'id': bucket_list.id,
                    'name': bucket_list.name,
                    'date_created': bucket_list.date_created,
                    'date_modified': bucket_list.date_modified
                })
                response.status_code = 201
                return response
        else:
            return jsonify(Bucketlist.get_all())

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                       "message": "bucketlist {} deleted successfully".format(bucketlist.id)
                   }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

    return app
