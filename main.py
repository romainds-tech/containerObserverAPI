from flask import Flask, request, jsonify
import os
import docker

def create_app():
    app = Flask(__name__)

    API_TOKEN = os.getenv("API_TOKEN")

    # use Docker client with Unix socket
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    @app.route('/api/containers', methods=['GET'])
    def get_containers():
        token = request.headers.get('Authorization')

        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401

        try:
            containers = client.containers.list(all=True)
            container_list = []
            for container in containers:
                container_list.append({
                    'id': container.id,
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags
                })
            return jsonify(container_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)