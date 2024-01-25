FROM python:3.11-alpine



# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



COPY ./requirements.txt /tmp/requirements.txt

#COPY ./app /app
WORKDIR /app

# install dependencies  
RUN python -m venv /py && \
    apk add --no-cache  build-base && \
    /py/bin/pip install --upgrade pip  && \
    pip install -r /tmp/requirements.txt   && \
    addgroup -S appgroup && adduser --home "$(pwd)" --no-create-home \ 
    -S django-user -G appgroup
    
    

USER django-user

# port where the Django app runs  
EXPOSE 8000  


