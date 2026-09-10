LANGUAGE_NAMES = {
    "ES": "🇪🇸 Español",
    "EN": "🇬🇧 English",
}

NO_DB_TEXT = """# Welcome to Chatboxd!
Looks like you don't have a database with the letterboxd data.
Go to the [export data section](https://letterboxd.com/settings/data/) on Letterboxd and download your data. Extract the data and find the two CSV files named `reviews.csv` and `diary.csv`. These two files are the ones required for building the database."""

TRANSLATIONS = {
    "ES": {
        "select_language": "Selecciona tu idioma",
        "select_model": "Selecciona un LLM",
        "available_provider": "✅ Proveedor {provider} disponible",
        "not_available_provider": "⚠️ Proveedor {provider} no disponible",
        "not_openai_api_key": "⚠️ OpenAI API Key no encontrada",
        "reset_chat": "Reiniciar Conversación",
        "configure_app": "Ajustes",
        "chat_placeholder": "Escribe tu mensaje aquí...",
        "header_caption": "¡Chatboxd te permite chatear con tus estadisticas de LetterBoxd!",
        "chat_loading": "Generando respuesta...",
        "continue": "Continuar",
        "reviews_filter_loading": "Buscando reseñas con los siguientes filtros:\n",
        "reviews_loading": "Buscando reseñas...\n",
        "film_filter_loading": "Buscando películas con los siguientes filtros:\n",
        "film_loading": "Buscando películas...\n",
        "title_filter": "* Título: {name}",
        "date_range_filter": "* Vistas desde **{from_date}** hasta **{to_date}**\n",
        "date_to_filter": "* Vistas antes de **{to_date}**\n",
        "rating_range_filter": "* Puntuadas entre **{from_rating}** y **{to_rating} estrellas**\n",
        "rating_filter": "* Puntuadas con **{from_rating} estrellas**\n",
        "year_filter": "* Lanzadas en el año **{year}**\n",
        "rewatch": "* 🔁 Vista de nuevo\n",
        "one_movie_daily_msg": "Tal día como hoy en {year} viste [{m_name} ({m_year})]({m_uri}). Le pusiste un {m_rating}.",
        "daly_msg_start": "Tal día como hoy viste varias películas de peso: \n",
        "many_movies_daily_msg": "* En {year} viste {name} ({m_year}).",
        "start_page_markdown": "# ¡Bienvenido/a a Chatboxd!\n\nPara empezar, configura el idioma en el que te gustaría utilizar la aplicación.",
        "keys_not_set": "🔴 Error al iniciar el agente, por favor asegúrate de configurar correctamente sus claves en secrets.env",
        "suggestions_label": "¿No sabes qué preguntar? Puedes elegir alguna de estas sugerencias:",
        "suggestions_list": [
            "¿Mi Top 10 pelliculas favoritas?",
            "¿A qué peliculas les he puesto 1 estrella?",
            "¿Qué peliculas he visto los ultimos 3 meses?",
            "¿Última review que he escrito?",
            "¿Pelis de este año que he visto?",
            "Gráfico de las peliculas del año pasado",
        ],
    },
    "EN": {
        "select_language": "Select your language",
        "select_model": "Choose a Large Language Model",
        "available_provider": "✅ Provider {provider} available",
        "not_available_provider": "⚠️ Provider {provider} not available",
        "not_openai_api_key": "⚠️ OpenAI API Key not found",
        "reset_chat": "Reset Conversation",
        "configure_app": "Settings",
        "chat_placeholder": "Type your message here...",
        "header_caption": "Chatboxd lets you chat with your LetterBoxd stats!",
        "chat_loading": "Generating response...",
        "continue": "Continue",
        "reviews_filter_loading": "Searching reviews with the following filters:\n",
        "reviews_loading": "Searching reviews...\n",
        "film_filter_loading": "Searching films with the following filters:\n",
        "film_loading": "Searching films...\n",
        "title_filter": "* Title: {name}",
        "date_range_filter": "* Watched from **{from_date}** to **{to_date}**\n",
        "date_to_filter": "* Watched before **{to_date}**\n",
        "rating_range_filter": "* Rated between **{from_rating}** and **{to_rating} stars**\n",
        "rating_filter": "* Rated with **{from_rating} stars**\n",
        "year_filter": "* Released in the year **{year}**\n",
        "rewatch": "* 🔁 Rewatched\n",
        "one_movie_daily_msg": "On this day in {year}, you watched [{m_name} ({m_year})]({m_uri}). You rated it {m_rating}.",
        "daly_msg_start": "On this day, you watched several notable films: \n",
        "many_movies_daily_msg": "* In {year}, you watched {name} ({m_year}).",
        "start_page_markdown": "# Welcome to Chatboxd!\n\nTo get started, set the language you'd like to use the app in.",
        "keys_not_set": "🔴 Failed to initialize agent, please make sure you have set up your keys correctly at secrets.env",
        "suggestions_label": "Don't know what to ask? You can choose one of these suggestions:",
        "suggestions_list": [
            "What are my top 10 favorite movies?",
            "What movies have I rated 1 star?",
            "What movies did I watch last 3 months?",
            "What was my last review?",
            "What movies did I watch in this year?",
            "Make a graph of the movies from last year",
        ],
    },
}

TOOL_RESPONSES = {
    "ES": {
        "get_reviews_response": "El usuario ha hecho las siguientes reviews de las películas que ha visto:\n",
        "get_movies_response": "De acuerdo a los filtros proporcionados, el usuario ha visto las siguientes películas:\n",
        "movie_details_not_found": "No se encontraron detalles de la película",
        "get_movie_details_response": "🎬 Los detalles de la película son (Añade emojis para que visualmente se vea mejor):\n{movie_detail}\n\nEn ningún caso debes mostrar una imagen ni la sinopsis, ni los Ratings. El diccionario que viene a continuación es irrelevante para ti, no le hagas caso.",
        "get_graph_response": "No devuelvas ningún dato, la gráfica será mostrada al usuario.",
    },
    "EN": {
        "get_reviews_response": "The user has made the following reviews of the movies they've watched:\n",
        "get_movies_response": "According to the provided filters, the user has watched the following movies:\n",
        "movie_details_not_found": "No movie details were found",
        "get_movie_details_response": "🎬 The details of the movie are (Add emojis to make it visually better):\n{movie_detail}\n\nUnder no circumstances should you show an image, synopsis, or Ratings. The dictionary below is irrelevant to you, do not pay attention to it.",
        "get_graph_response": "Do not return any data, the graph will be displayed to the user.",
    },
}

MODEL_PROVIDERS = {
    "ES": {
        "Ollama": """**Ollama** te permite ejecutar un modelo de lenguaje en tu propio dispositivo.

Para ello, deberás instalar Ollama en tu sistema y descargar el modelo a utilizar mediante `ollama pull <model_name>` (asegúrate de que el mismo modelo esté en la lista de permitidos de `llm_service.py`).

Para disponibilizar el modelo, ejecuta `ollama serve`.

Una vez hecho esto, puedes comenzar a chatear con **Chatboxd**.
""",
        "OpenAI": """**OpenAI** permite el acceso a modelos de lenguaje a través de su API.

Para comenzar, necesitarás registrarte en la plataforma y obtener tus credenciales de API. Una vez que tengas tus credenciales, deberás almacenarlas en variables de entorno o en el fichero `secrets.env`:

```
OPENAI_API_KEY=...
```

Una vez configuradas las credenciales, puedes comenzar a chatear con **Chatboxd**. Ten en cuenta que el uso de la API de OpenAI puede acarrear costes.""",
        "Google": """**Google** permite el acceso a modelos de lenguaje a través de su API.

Para comenzar, necesitarás registrarte en la plataforma y obtener tus credenciales de API. Una vez que tengas tus credenciales, deberás almacenarlas en variables de entorno o en el fichero `secrets.env`:

```
GOOGLE_API_KEY=...
```

Una vez configuradas las credenciales, puedes comenzar a chatear con **Chatboxd**. Ten en cuenta que el uso de la API de Gemini puede acarrear costes.""",
        "Groq": """**Groq** permite el acceso a modelos de lenguaje a través de su API.

Para comenzar, necesitarás registrarte en https://console.groq.com y obtener tus credenciales de API. Una vez que tengas tus credenciales, deberás almacenarlas en variables de entorno o en el fichero `secrets.env`:

```
GROQ_API_KEY=...
```

Una vez configuradas las credenciales, puedes comenzar a chatear con **Chatboxd**. Ten en cuenta que el uso de la API de Groq puede acarrear costes.""",
        "OpenRouter": """**OpenRouter** permite el acceso a modelos de lenguaje a través de su API, incluidos modelos gratuitos.

Para comenzar, necesitarás registrarte en https://openrouter.ai/keys y obtener tus credenciales de API. Una vez que tengas tus credenciales, deberás almacenarlas en variables de entorno o en el fichero `secrets.env`:

```
OPENROUTER_API_KEY=...
```

El catálogo empieza por `openrouter/free` y otros modelos `:free` con soporte de herramientas. Una vez configuradas las credenciales, puedes comenzar a chatear con **Chatboxd**. OpenRouter también ofrece modelos de pago que no están en esta lista, y usarlos puede acarrear costes.""",
    },
    "EN": {
        "Ollama": """**Ollama** allows you to run a Large Language Model in your own device.

To use Ollama, first you must install it in your machine and download the model you want to use, by running `ollama pull <model_name>` (make sure the same model is on the allow-list in `llm_service.py`).

To make the model available, run `ollama serve`.

Once you're done, you can start chatting with **Chatboxd**.
""",
        "OpenAI": """**OpenAI** allows you to access Large Language Models through their API.

To get started, you must sign up on the platform and get your API credentials. Once you have your credentials, you must store them in environment variables or in the `secrets.env` file:

```
OPENAI_API_KEY=...
```

Once you have your credentials, you can start chatting with **Chatboxd**. Note that using the OpenAI API may incur costs.""",
        "Google": """**Google** allows you to access Large Language Models through their API.

To get started, you must sign up on the platform and get your API credentials. Once you have your credentials, you must store them in environment variables or in the `secrets.env` file:

```
GOOGLE_API_KEY=...
```

Once you have your credentials, you can start chatting with **Chatboxd**. Note that using the Gemini API may incur costs.""",
        "Groq": """**Groq** allows you to access Large Language Models through their API.

To get started, you must sign up at https://console.groq.com and get your API credentials. Once you have your credentials, you must store them in environment variables or in the `secrets.env` file:

```
GROQ_API_KEY=...
```

Once you have your credentials, you can start chatting with **Chatboxd**. Note that using the Groq API may incur costs.""",
        "OpenRouter": """**OpenRouter** allows you to access Large Language Models through their API, including free models.

To get started, you must sign up at https://openrouter.ai/keys and get your API credentials. Once you have your credentials, you must store them in environment variables or in the `secrets.env` file:

```
OPENROUTER_API_KEY=...
```

The catalog starts with `openrouter/free` and other `:free` models that support tools. Once you have your credentials, you can start chatting with **Chatboxd**. Paid models exist on OpenRouter but are not in this list, and using them may incur costs.""",
    },
}
