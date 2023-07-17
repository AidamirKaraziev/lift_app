FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app/
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
     cd /usr/local/bin && \
     ln -s /opt/poetry/bin/poetry && \
     poetry config virtualenvs.create false
# Install Poetry
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false

#RUN source $HOME/ad/.local/bin.poetry
#26.09.22 заработало с этим обнаружился поетри
#RUN source $HOME/ad/.local/bin.poetry && poetry update && poetry install

RUN pip3 install --upgrade pip
# RUN pip install poetry==1.2.0a1
RUN pip install greensms
RUN pip install --force-reinstall httpcore==0.15

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /app
ENV PYTHONPATH=/app
