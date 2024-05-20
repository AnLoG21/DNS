FROM python:3.10
WORKDIR /MVVM/Model
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD ["python", "Compare.py"]


