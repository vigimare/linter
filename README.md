# Linter

This repo contains code for validating XML files in the [VIGIMARE](https://vigimare.eu/) project.
Multiple XSD files from the [CISE data model](https://emsa.europa.eu/cise-documentation/cise-data-model-1.5.3/) as well as the [VIGIMARE data model](https://github.com/vigimare/xsd/tree/main/vigimare) are used to verify the XML files.

The repo contains both a CLI and a webapp for this.


## How to install
This project use [uv](https://github.com/astral-sh/uv) for package managing, rather than `pip` or `conda`.

1. **Install uv**

    If you don’t have `uv` installed, you can install it via the command
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2. **Install dependencies**

    Run the following command in the project root:
      ```bash
      uv sync
      ```
      This will install the dependencies listed in pyproject.toml in a virtual environment called `.venv`

3. **Create the submodule**

    Fetch the contents from the [xsd repository](https://github.com/vigimare/xsd)
      ```bash
      git submodule update --init
      ```

## How to run
  Now everything should be set up correctly. The `examples` folder contains some XML files. Try to run
  ```bash
  uv run main.py --xml-files examples/vigimare_vessel.xml
  ```
This should return a success.

Run multiple files
  ```bash
  uv run main.py --xml-files examples/*.xml
  ```

## How to run webapp
In addition to the CLI this repo also contains a webapp that can be used to validate XML files. The webapp is based on `streamlit` which is a very lightweight and simple tool to create apps quickly.

To run the webapp, simply run
```bash
uv run streamlit run app.py
```
This should open the app in a browser on `http://localhost:8501`

## How to update `xsd` submodule
The XSD files in the project is contained in a separate [repo](https://github.com/vigimare/xsd). This repo is added as a `git submodule` to this repo. In order to pull the latest changes from this submodule, simply do:
```bash
git submodule update --remote --merge
```

## How to use API
XML file validation can also be done via an API. Start the API using
```bash
uv run uvicorn api:app --reload
```

Sending an XML file is done by using `curl` like this:
```bash
curl -X POST "http://localhost:8000/api/v1/validate-file" \
  -F "file=@examples/vigimare_vessel_with_mmsi.xml"
```
