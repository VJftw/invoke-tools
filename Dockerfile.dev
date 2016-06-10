FROM alpine:3.4

RUN apk add --update gcc python3 python3-dev musl-dev linux-headers git

RUN pip3 install --upgrade pip

# Install app deps
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Install dev deps
COPY tests/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Clean up
RUN apk del gcc python3-dev musl-dev linux-headers && rm -rf /var/cache/apk
