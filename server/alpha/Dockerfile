FROM python:3.5
MAINTAINER Leonid Logvinov <logvinov.leon@gmail.com>
RUN mkdir /dpcs
WORKDIR /dpcs
ENV DJANGO_SETTINGS_MODULE 'server_django.prod_settings'
ADD ./requirements/ /dpcs/requirements/
RUN pip install -r requirements/requirements.common
RUN pip install -r requirements/requirements.prod
RUN apt-get update && apt-get install -y \
						ca-certificates \
						nginx \
						gettext-base \
	&& rm -rf /var/lib/apt/lists/*
ADD . /dpcs
RUN python manage.py check --deploy
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py makemigrations alpha
RUN python manage.py migrate alpha
RUN python manage.py collectstatic -v0 --no-input
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

RUN nginx

CMD ["gunicorn", "-c", "gunicorn_conf.py", "--chdir", "/dpcs", "server_django.wsgi", "--reload"]

