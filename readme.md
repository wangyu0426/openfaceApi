
# jenkins config
```
docker rm $(docker stop $(docker ps -a -q --filter="name=main_program"))|| true
docker build . -t wangyu1998/openfaceapi:v0.${BUILD_NUMBER}
docker push wangyu1998/openfaceapi:v0.${BUILD_NUMBER}

docker run -d --name main_program -p 80:8000 -p 8080:9000 wangyu1998/openfaceapi:v0.${BUILD_NUMBER}

```
