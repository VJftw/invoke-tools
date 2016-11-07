FROM alpine:3.4

#RUN sed -i -e 's/v3\.4/edge/g' /etc/apk/repositories
RUN apk add --update gcc python python-dev musl-dev linux-headers git curl

RUN curl -O -L https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py

RUN pip install --upgrade pip

# Install app deps
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install dev deps
COPY tests/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Clean up
RUN apk del gcc musl-dev linux-headers curl && rm -rf /var/cache/apk
