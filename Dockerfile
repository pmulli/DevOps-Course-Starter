FROM python:3.9.2-slim-buster as base
RUN pip install --upgrade pip
RUN pip install poetry
COPY poetry.lock pyproject.toml ./

FROM base as production
RUN poetry config virtualenvs.create false --local && poetry install
RUN poetry add gunicorn
RUN poetry add pymongo
RUN poetry add pymongo[srv]
COPY ./todo_app ./todo_app
COPY ./entrypoint.sh /entrypoint.sh
ENV WEBAPP_PORT=80
EXPOSE ${WEBAPP_PORT}
ENV PORT=80
EXPOSE ${PORT}
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

FROM base as development
RUN poetry install
COPY ./todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as test
RUN pip install mongomock
RUN poetry install
RUN poetry add mongomock
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update -qqy \
 && apt-get -qqy install google-chrome-stable \
 && rm /etc/apt/sources.list.d/google-chrome.list \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Install Chrome WebDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
 && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
 && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
 && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod 755 /usr/bin/chromedriver
COPY ./todo_app ./todo_app
WORKDIR /todo_app
ENTRYPOINT ["poetry", "run", "pytest"]