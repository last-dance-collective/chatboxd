![image](https://github.com/user-attachments/assets/e2f778f5-8ae4-465f-9362-250b8914c7ba)

---

Chatboxd is a web application that allows you to easily interact with information logged into your Letterboxd account thanks to the power of LLMs.

It is multi-language, allows the use of several LLM models and contains many other features.

## Contents

1. [Execution](#execution)
    - [Environment Variables](#environment-variables)
    - [Load Your Data](#load-data)
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

Since Chatboxd is an application that leverages a LLM, it is necessary to configure some environment variables with the model credentials.

Currently, the repository supports Azure hosted LLMs, but we are working on supporting more models regardless of whether they are hosted in Azure or not.

In the `template_secrets.env` file you can find the following variables:

-   `OPENAI_API_ENDPOINT`: The API endpoint of the Azure OpenAI service.
-   `OPENAI_API_VERSION`: The API version of the Azure OpenAI service.
-   `OPENAI_API_KEY`: The API key of the Azure OpenAI service.

You can find the API endpoint, API version, and API key in the Azure portal under the "Keys and Endpoint" section of your Azure OpenAI service.

Once you have entered the values in the `template_secrets.env` file, you have to rename it to `secrets.env`.

If you prefer, you can declare the environment variables in your terminal before running the application.

```bash
export AZURE_OPENAI_ENDPOINT=<Your Azure OpenAI endpoint>
export OPENAI_API_VERSION=<Your OpenAI API version>
export OPENAI_API_KEY=<Your OpenAI API key>
```

### Load Your Data

**All files related to the data ingestion are located in the folder *data_ingestion* located in the root directory**
To load your data into a new SQLite database, follow these steps:

1. **Prepare Your Data Files**:
    - Go to the [export data section](https://letterboxd.com/settings/data/) on Letterboxd and download your data.
    - Extract the data and find the two CSV files named `reviews.csv` and `diary.csv`.
    - Place these files in the `data_ingestion/user_data` directory.

2. **CSV File Structure**:
    - `reviews.csv` should have the following columns:
        - `Date`: The date of the review.
        - `Name`: The name of the movie.
        - `Review`: The review text.
    - `diary.csv` should have the following columns:
        - `Date`: The date the movie was watched.
        - `Name`: The name of the movie.
        - `Year`: The year the movie was released.
        - `Letterboxd URI`: The URI of the movie on Letterboxd.
        - `Rating`: The rating given to the movie.
        - `Rewatch`: Indicates if the movie was rewatched.
        - `Tags`: Any tags associated with the movie.
        - `Watched Date`: The date the movie was watched.
        - `Username`: The username of the person who watched the movie.

3. **Run the Data Ingestion Script**:
    - **Important**: There is a variable called USER_NAME where you can specify the username of the person who watched the movies. This is intended to be used when multiple people are using the same database.
    - Make sure you have the necessary dependencies installed by running the following command:
      ```sh
      uv sync
      ```
    - Run the following commands to execute the script:
      ```sh
      cd data_ingestion
      python main.py
      ```

4. **What the Script Does**:
    - The script will create the necessary tables (`reviews` and `diary`) in the SQLite database if they do not already exist.
    - It will then read the data from `reviews.csv` and `diary.csv` and insert the entries into the respective tables.
    - The script will also link diary entries to their corresponding reviews based on the movie name and date.

5. **Database Location**:
    - The SQLite database file (`letterboxd.db`) will be created in the parent directory of the script.

By following these steps, you will be able to load your data into the SQLite database and interact with the data.

### Run App

To run the app you just need to enter the following command in a terminal:

```bash
uv run -m streamlit run src/main.py
```

Note that the first time you run this command, it creates the virtual environment and installs all the dependencies. This first run may take a little longer, but the following runs will be much faster.

## How It Works

This section documents the engineering process carried out for the operation of the project. It is a section in which technical concepts will be deepened in detail for those people who want the necessary knowledge to carry out a similar project.


### Agent

We have developed a ReAct agent architecture based on the following concepts:

* `act` - Let the model call specific tools.
* `observe` - Pass the tool output back to the model.
* `reason` - Let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly).

Here is a simple diagram of our architecture used:

![Architecture Diagram](https://github.com/user-attachments/assets/d4f39b93-896d-4496-84d3-f03677933458)


The operation and details of the tools are explained below.

### Tools

### BBDD
