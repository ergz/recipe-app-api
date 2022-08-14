FROM python:3.9-alpine3.13

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv .venv && \
	.venv/bin/pip install --upgrade pip && \
	.venv/bin/pip install -r /tmp/requirements.txt && \
	rm -rf /tmp && \
	adduser \
		--disabled-password \
		--no-create-home \
		django-user

# adds .venv path as the place to look first
ENV PATH=".venv/bin:$PATH" 

USER django-user
