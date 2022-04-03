#FROM http://192.168.50.242:8347/repository/pypi-all/

LABEL maintainer="j7breuer@gmail.com"

# Set port
#ARG APP_PORT=5050
#ENV APP_PORT=${APP_PORT}

# Set pip.conf
RUN export PIP_CONFIG_FILE=/.config/pip/pip.conf

# Set the local directory
ARG APP_HOME=/tweet-sentiment-api
ENV APP_HOME=${APP_HOME}
WORKDIR ${APP_HOME}

#  Get python libraries from nexus server
RUN pip install -r requirements.txt

# Run flask API
ENTRYPOINT ["python", "./app/app.py"]
EXPOSE 5000