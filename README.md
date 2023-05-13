# Photo service backend

API for managing users photoes and albums.

## Quick start
Build docker image from inside the `Photo-service-backend` directory:
```commandline
docker build -t backend .
```
Run docker container :
   ```commandline
   docker run -p 8000:8000 backend
   ```
Run docker container for S3-Backend:
   ```commandline
   docker run --add-host host.docker.internal:host-gateway -p 8000:8000 backend 
   ```

**Swagger for full API documentation:** http://127.0.0.1:8000/docs.
