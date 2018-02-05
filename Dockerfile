FROM bamos/openface

RUN apt-get install -y libffi-dev libssl-dev
ENV PYTHONWARNINGS="ignore:a true SSLContext object"
RUN pip install pyopenssl ndg-httpsclient pyasn1
RUN	pip install pathlib django djangorestframework jsonfield channels asgi_redis django-cors-headers imagehash openface pygments
COPY . /root/openfaceapi
RUN cd ~/openfaceapi && \
    pip install -r requirements.txt 

ENTRYPOINT ["python", "/root/openfaceapi/manage.py", "runserver","0:8000"]