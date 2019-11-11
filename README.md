# restyolo
### A rest api for a @eriklindernoren PyTorch-YOLOv3 object detector

## Installation
1. Clone this repository
2. Run `git submodule update --init --recursive`
3. From the root of this repo run
```shell script
make install
```

## Running
From the root of this repo run:
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
  
     
