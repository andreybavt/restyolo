# restyolo
### A rest api for a @eriklindernoren PyTorch-YOLOv3 object detector

## Installation
From the project directory run
```shell script
make install
```

## Running
From the project directory run:
```shell script
./run.sh
```
The default port is 5000

## Endpoints

- `/detect`
    
    method: `POST`
    
    required headers: `'content-type': 'application/json'`
    
    request body: 
    ```{"image_id":"base64_encoded_image"}``` 
  
     