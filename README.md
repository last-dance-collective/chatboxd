![image](https://github.com/user-attachments/assets/e2f778f5-8ae4-465f-9362-250b8914c7ba)

---

Chatboxd is a web application that allows you to easily interact with your LeeterBoxd statistics thanks to the power of GenAI.

It is multi-language, allows the use of several LLM models and contains many other features.

## Contents

1. [Execution](#execution)
    - [Environment Variables](#environment-variables)
    - [Load Data](#load-data)
    - [Run App](#run-app)
2. [How It Works](#how-it-works)
    - [Agent](#agent)
    - [Tools](#tools)
    - [BBDD](#bbdd)

## Execution

In this section, we will explain how to execute the application once you have cloned the repository.

### Requirements

For the execution of the application, you need to have installed:

##### [UV](https://docs.astral.sh/uv/)

uv is an extremely fast Python package and project manager, written in Rust. For installation, you can use one of the following methods:

-   `curl`
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
-   `wget`
    ```bash
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```
-   `Homebrew`
    ```bash
    brew install uv
    ```

If you need another method, you can find it [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/).

### Environment Variables

Since it is a chatbot with generative ia, it is necessary to configure some environment variables with the model credentials.

Currently, the repository supports Azure hosted LLMs, but we are working on supporting more models regardless of whether they are hosted in Azure or not.

In the `template_secrets.env` file you can find the following variables:

-   `OPENAI_API_ENDPOINT`: The API endpoint of the Azure OpenAI service.
-   `OPENAI_API_VERSION`: The API version of the Azure OpenAI service.
-   `OPENAI_API_KEY`: The API key of the Azure OpenAI service.

You can find the API endpoint, API version, and API key in the Azure portal under the "Keys and Endpoint" section of your Azure OpenAI service.

Once you have enter the values in the `template_secrets.env` file, you have to rename it to `secrets.env`.

If you prefer, you can declare the environment variables in your terminal before running the application.

### Load Data

`Coming Soon`

### Run App

To run the app you just need to enter the following command in a terminal:

```bash
uv run -m streamlit run src/main.py
```

Note that the first time you run this command, it creates the virtual environment and installs all the dependencies. This first run may take a little longer, but the following runs will be much faster.

## How It Works

### Agent

### Tools

### BBDD
