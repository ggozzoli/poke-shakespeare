FROM python:alpine3.8
COPY application /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/src"
ENTRYPOINT [ "python" ]
CMD [ "/app/src/api/app.py" ]
