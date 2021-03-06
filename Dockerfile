FROM bamos/openface

RUN	pip install pathlib django djangorestframework jsonfield
RUN	pip install channels 
RUN pip install asgi_redis django-cors-headers imagehash openface pygments
COPY . /root/openfaceapi
RUN cd ~/openfaceapi && \
    pip install -r requirements.txt 

ENTRYPOINT ["python", "/root/openfaceapi/manage.py", "runserver","0:8000"]