# start from an official Python image
FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client

RUN mkdir -p /var/ounass
RUN mkdir -p /var/ounass/backend
WORKDIR /var/ounass/backend

# install our dependencies
COPY requirements.txt /var/ounass/backend

RUN pip install -r requirements.txt

# copy our project code
COPY . /var/ounass/backend

# run Django management commands at start
RUN cd /var/ounass/backend && python manage.py collectstatic --no-input

#COPY entrypoint.sh /var/ounass/backend
#RUN chmod +x "/var/ounass/backend/entrypoint.sh"
#ENTRYPOINT ["/var/ounass/backend/entrypoint.sh"]
#RUN cd /var/ounass/backend && python manage.py migrate --no-input
CMD ["gunicorn", "--chdir", "/var/ounass/backend", "--bind", ":8000", "ounass.wsgi:application", "--reload"]