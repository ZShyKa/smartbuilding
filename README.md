# Smart Building

- api — Flask REST API, chạy trong Docker / k3s
- flutter — Flutter app, chạy trực tiếp trên máy

## Yêu cầu

- Docker Desktop 
- Rancher Desktop 
- Flutter SDK 

## Chạy API

bash
docker-compose up --build


API chạy tại http://localhost:5000

## Chạy Flutter app

bash
cd mobile
flutter pub get
flutter run


App kết nối đến http://localhost:5000

## API

### GET /devices

bash
curl http://localhost:5000/devices
curl http://localhost:5000/devices?type=light
curl http://localhost:5000/devices?floor=2
curl http://localhost:5000/devices?status=on


### POST /devices

bash
curl -X POST http://localhost:5000/devices \
  -H "Content-Type: application/json" \
  -d '{"name": "Den bep", "type": "light", "floor": 1, "unit": "A101"}

### PATCH /devices/:id

bash
curl -X PATCH http://localhost:5000/devices/dev-001 \
  -H "Content-Type: application/json" \
  -d '{"status": "off"}'


### DELETE /devices/:id

bash
curl -X DELETE http://localhost:5000/devices/dev-001


## Deploy lên k3s

bash
nerdctl build -t smart-apartment-api:latest ./api
kubectl apply -f k3s/


Truy cập tại http://localhost:30080

## Scale

bash
kubectl scale deployment smart-apartment --replicas=4
kubectl get pods -w

