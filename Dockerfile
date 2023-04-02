FROM python:3.10

WORKDIR /backend

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ARG COMMIT_ID="No commit ID specified"
ENV COMMIT_ID=$COMMIT_ID

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
