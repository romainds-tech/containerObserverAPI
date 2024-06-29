from flask import Flask, request, jsonify
import os
import docker
import json


# Vérifier si l'objet peut être sérialisé en JSON
def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False


# Transformer un conteneur en dictionnaire avec des attributs JSON-serializables
def container_to_dict(container):
    return {
        k: v
        for k, v in container.attrs.items()
        if is_json_serializable(v)
    }


def create_app():
    app = Flask(__name__)
    API_TOKEN = os.getenv("API_TOKEN")
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    @app.route('/api/containers', methods=['GET'])
    def get_containers():
        token = request.headers.get('Authorization')

        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401

        try:
            containers = client.containers.list(all=True)
            container_list = [container_to_dict(container) for container in containers]
            return jsonify(container_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)