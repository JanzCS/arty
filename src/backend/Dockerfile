FROM python:3.10
WORKDIR /backend
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install fastapi uvicorn
COPY ./ /backend/
ENV PYTHONPATH /
# WORKDIR /
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]