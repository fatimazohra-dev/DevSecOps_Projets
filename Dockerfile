# [Container / IaC] Image ancienne, tag non figé, exécution en root, secrets dans ENV
FROM python:3.6

ENV DB_PASSWORD=admin123 \
    API_TOKEN=ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE1234

WORKDIR /app
ADD app/ /app
RUN pip install -r requirements.txt

EXPOSE 5000
# Pas de USER non-root, pas de HEALTHCHECK
CMD ["python", "app.py"]
