# wallbox-challenge

WallBox coding challenge /2022/

## Repository structure

- Answers for Part 1 in `unit_testing` folder
- Answers for Part 2 in `system_testing` folder

```text
.
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── system_testing
│   ├── architecture.png
│   └── README.md
└── unit_testing
    ├── __init__.py
    ├── test_problem_1.py
    ├── test_problem_2.py
    └── test_problem_3.py
```

## Building the Docker image (for Part 1)

```
docker build -f ./Dockerfile -t wallbox_docker .
```

## Changing log level (for Part 1)

Can be achieved through changing `DEBUG` to `INFO` in 'pyproject.toml' file.

## Running unit tests (for Part 1)

Mount current directory to Docker container, in case we want to have access to
any files generated during execution.

```bash
export WORKSPACE="/tmp/wallbox-challenge/" && \
docker run --rm -it \
--name wallbox_challenge \
-v $(pwd):$WORKSPACE \
wallbox_docker \
pytest -v
```