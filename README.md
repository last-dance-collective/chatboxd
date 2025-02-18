![image](https://github.com/user-attachments/assets/e2f778f5-8ae4-465f-9362-250b8914c7ba)

---

Chatboxd is a web application that allows you to easily interact with information logged into your Letterboxd account thanks to the power of LLMs.

It is multi-language, allows the use of several LLM models and contains many other features.

## Contents

1. [Execution](#execution)
    - [Environment Variables](#environment-variables)
    - [Load Your Data](#load-your-data)
    - [Run App](#run-app)
2. [How It Works](#how-it-works)
    - [Agent](#agent)
    - [Tools](#tools)
    - [BBDD](#bbdd)

## Execution

In this section, we will explain how to execute the application once you have cloned the repository.

### Requirements

> [!IMPORTANT]
> You need to have installed [UV](https://docs.astral.sh/uv/)

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

Currently, the repository supports OpenAI LLMs, but we are working on supporting more models.

> [!NOTE]
> In the `template_secrets.env` file you can find the following variable:
>
> -   `OPENAI_API_KEY`: The API key of the OpenAI service.

> [!TIP]
> You can find the API key in the OpenAI dashboard under the "API Keys" section.

> [!IMPORTANT]
> Once you have entered the values in the `template_secrets.env` file, you have to rename it to `secrets.env`.

If you prefer, you can declare the environment variables in your terminal before running the application.

```bash
export OPENAI_API_KEY=<Your OpenAI API key>
```

### Load Your Data

**All files related to the data ingestion are located in the folder _data_ingestion_ located in the root directory**
To load your data into a new SQLite database, follow these steps:

#### Prepare Your Data Files

1. Go to the [export data section](https://letterboxd.com/settings/data/) on Letterboxd and download your data.
2. Extract the data and find the two CSV files named `reviews.csv` and `diary.csv`.
3. Place these files in the `data_ingestion/user_data/` directory.

> [!NOTE] > `reviews.csv` should have the following columns:
>
> -   `Date`: The date of the review.
> -   `Name`: The name of the movie.
> -   `Review`: The review text.

> [!NOTE] > `diary.csv` should have the following columns:
>
> -   `Date`: The date the movie was watched.
> -   `Name`: The name of the movie.
> -   `Year`: The year the movie was released.
> -   `Letterboxd URI`: The URI of the movie on Letterboxd.
> -   `Rating`: The rating given to the movie.
> -   `Rewatch`: Indicates if the movie was rewatched.
> -   `Tags`: Any tags associated with the movie.
> -   `Watched Date`: The date the movie was watched.
> -   `Username`: The username of the person who watched the movie.

#### Run the Data Ingestion Script

> [!IMPORTANT]
> There is a variable called `USER_NAME` at `data_ingestion/main.py` where you can specify the username of the person who watched the movies. This is intended to be used when multiple people are using the same database.

```bash
uv run data_ingestion/main.py
```

#### What it Does?

The script initializes the SQLite database by creating the required tables (`reviews` and `diary`) if they do not already exist. It then processes data from `reviews.csv` and `diary.csv`, inserting the entries into their corresponding tables.

Additionally, the script associates diary entries with their respective reviews by matching the movie name and date. The SQLite database file, `letterboxd.db`, will be generated in the script's parent directory.

By following these steps, you will be able to load your data into the SQLite database and interact with the data.

### Run App

To run the app you just need to enter the following command in a terminal:

```bash
uv run -m streamlit run src/main.py
```

> [!NOTE]
> The first time you run this command, it creates the virtual environment and installs all the dependencies. This first run may take a little longer, but the following runs will be much faster.

## How It Works

This section documents the engineering process carried out for the operation of the project. It is a section in which technical concepts will be deepened in detail for those people who want the necessary knowledge to carry out a similar project.

### Agent

We have developed a ReAct agent architecture based on the following concepts:

-   `act` - Let the model call specific tools.
-   `observe` - Pass the tool output back to the model.
-   `reason` - Let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly).

Here is a simple diagram of our architecture used:

![Architecture Diagram](https://github.com/user-attachments/assets/e48dedcc-73a0-4e05-9b40-ad28871eacb7)

We have added a previous node called `Filter` which is in charge of filtering the message history so that it is not excessively long after several iterations.
The operation and details of the tools are explained below.

### Tools

The agent has at its disposal several tools that allow it to access the SQLite database that we have created with our data and also perform queries to external APIs. According to the user's request, the agent will decide to call one tool, several, or directly answer as mentioned above.

The list of tools is:

-   `get_movies`: Filters the user movie registry according to the search parameters identified in the user query, then retrieves the search result.
-   `get_reviews`: Retrieve reviews from movies watched by the user, searching by movie name or by review id.
-   `get_graph`: Generates and displays a graph based upon the provided list of movies.
-   `get_movie_details`: Retrieves the detail of a movie by its Letterboxd URL.
-   `get_movie_details_extended`: Retrieves the detail of a movie by its title (in English) using the OmdbAPI and its Letterboxd URL.

> [!NOTE]
> If the user has an `OMDb API KEY`, the agent will always use `get_movie_details_extended` for movie requests in detail. If not, the agent will use `get_movie_details`.

### BBDD

Although it has been previously commented on the structure of the csv, for a more adequate knowledge of the database used, the following E/R model is attached:

![E/R Model](https://github.com/user-attachments/assets/47c8e353-c457-4a1a-ac9d-25731a78afc9)
