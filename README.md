There are two servers running here. There is a base nodejs server that runs on port 3000, and a python wrapper (implemented to have the swagger docs available) that calls that internally. 

1. Pull the repo

2. Run with Docker:

```sh
docker build -t kvstore . 
docker run --rm -p 3000:3000 -p 1234:1234 -it --name kvstore kvstore
```

Do debug and see files in docker

```sh
docker exec -it kvstore bas
```

Or run directly

3.  In the main folder:
```sh
cd backend
npm install
node main.js
```

4. In the main folder: 

```sh
pip install -r requirements.txt
uvicorn main:app --port=<port> #suggested 1234
```

5. Push the docker to artifect registry

```sh
bash docker_build_push.sh
```