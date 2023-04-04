# Install common packages
FROM python:3.9 AS install-common

WORKDIR /src
ENV DELPHAI_ENVIRONMENT=local

RUN python -m venv /app
ENV PATH /app/bin:$PATH
ENV VIRTUAL_ENV=/app

RUN python -m venv /root/.poetry && /root/.poetry/bin/pip install --no-cache-dir poetry==1.2.2
ENV PATH $PATH:/root/.poetry/bin

COPY *.toml *.lock ./
RUN poetry install --no-cache --only main --no-root && pip cache purge && rm -rf ~/.cache/pypoetry/artifacts ~/.cache/pypoetry/cache

# Install develop packages, run codegen and tests
FROM install-common AS codegen

ARG CI
ARG RUN_TESTS

COPY . /src
RUN if [ -n "$CI" ] || [ -n "$RUN_TESTS" ]; then poetry install --no-cache --no-root && poetry run flake8 && poetry run black --check --diff . ; fi

# Install
FROM install-common AS install
COPY --from=codegen /src /src
RUN pip install --no-deps .


# Make runtime image
FROM python:3.9-slim AS runtime
EXPOSE 8000
WORKDIR /app
ENV DELPHAI_ENVIRONMENT=local

ENV PATH /app/bin:$PATH
ENV VIRTUAL_ENV /app

COPY --from=install /app /app

CMD ["uvicorn", "--host", "0.0.0.0", "delphai_api:app"]
