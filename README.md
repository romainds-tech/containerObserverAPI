# Container status API
This repo is an micro flask API with only one GET endpoint who let you see the status of yours docker containers

### Installation

- Clone the repo on the server then
  - Create your TOKEN and replace it in the command below

```bash
pip install -r requirements.txt && sudo ufw allow 5000 && API_TOKEN=YOUR_API_TOKEN gunicorn -w 4 -b 0.0.0.0:5000 "main:create_app()" &
```

### Usage

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" http://YOUR_SERVER_IP:5000/api/containers
```


