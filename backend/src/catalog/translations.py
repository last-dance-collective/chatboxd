LANGUAGE_NAMES = {
    "ES": "🇪🇸 Español",
    "EN": "🇬🇧 English",
    "FR": "🇫🇷 Français",
    "DE": "🇩🇪 Deutsch",
    "IT": "🇮🇹 Italiano",
    "PT": "🇵🇹 Português",
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
    "FR": {
        "select_language": "Sélectionnez votre langue",
        "select_model": "Sélectionnez un LLM",
        "available_provider": "✅ Fournisseur {provider} disponible",
        "not_available_provider": "⚠️ Fournisseur {provider} non disponible",
        "not_openai_api_key": "⚠️ OpenAI API Key non trouvé",
        "reset_chat": "Réinitialiser la Conversation",
        "configure_app": "Paramètres",
        "chat_placeholder": "Tapez votre message ici...",
        "header_caption": "Chatboxd vous permet de discuter avec vos statistiques LetterBoxd !",
        "chat_loading": "Génération de réponse...",
        "continue": "Continuer",
        "reviews_filter_loading": "Recherche d'avis avec les filtres suivants :\n",
        "reviews_loading": "Recherche d'avis...\n",
        "film_filter_loading": "Recherche de films avec les filtres suivants :\n",
        "film_loading": "Recherche de films...\n",
        "title_filter": "* Titre : {name}",
        "date_range_filter": "* Regardé du **{from_date}** au **{to_date}**\n",
        "date_to_filter": "* Regardé avant le **{to_date}**\n",
        "rating_range_filter": "* Noté entre **{from_rating}** et **{to_rating} étoiles**\n",
        "rating_filter": "* Noté avec **{from_rating} étoiles**\n",
        "year_filter": "* Sorti en **{year}**\n",
        "rewatch": "* 🔁 Revu\n",
        "one_movie_daily_msg": "En ce jour de l'année {year}, vous avez regardé [{m_name} ({m_year})]({m_uri}). Vous lui avez donné une note de {m_rating}.",
        "daly_msg_start": "En ce jour, vous avez regardé plusieurs films remarquables : \n",
        "many_movies_daily_msg": "* En {year}, vous avez regardé {name} ({m_year}).",
        "start_page_markdown": "# Bienvenue sur Chatboxd !\n\nPour commencer, configurez la langue dans laquelle vous souhaitez utiliser l'application.",
        "keys_not_set": "🔴 Échec de l'initialisation de l'agent, veuillez vous assurer que vous avez correctement configuré vos clés dans secrets.env",
        "suggestions_label": "Ne sais pas quoi poser ? Vous pouvez choisir l'une de ces suggestions :",
        "suggestions_list": [
            "Quels sont mes 10 films préférés ?",
            "Quels films j'ai noté 1 étoile ?",
            "Quels films j'ai regardé les 3 derniers mois ?",
            "Quelle est ma dernière critique ?",
            "Quels films j'ai vus cette année ?",
            "Fais un graphe des films de l'année dernière",
        ],
    },
    "DE": {
        "select_language": "Wähle deine Sprache",
        "select_model": "Wähle ein LLM",
        "available_provider": "✅ Provider {provider} verfügbar",
        "not_available_provider": "⚠️ Provider {provider} nicht verfügbar",
        "not_openai_api_key": "⚠️ OpenAI API Key nicht gefunden",
        "reset_chat": "Konversation zurücksetzen",
        "configure_app": "Einstellungen",
        "chat_placeholder": "Geben Sie hier Ihre Nachricht ein...",
        "header_caption": "Chatboxd ermöglicht es Ihnen, mit Ihren LetterBoxd-Statistiken zu chatten!",
        "chat_loading": "Antwort wird generiert...",
        "continue": "Fortfahren",
        "reviews_filter_loading": "Suche nach Bewertungen mit den folgenden Filtern:\n",
        "reviews_loading": "Suche nach Bewertungen...\n",
        "film_filter_loading": "Suche nach Filmen mit den folgenden Filtern:\n",
        "film_loading": "Suche nach Filmen...\n",
        "title_filter": "* Titel: {name}",
        "date_range_filter": "* Angesehen von **{from_date}** bis **{to_date}**\n",
        "date_to_filter": "* Angesehen vor **{to_date}**\n",
        "rating_range_filter": "* Bewertet zwischen **{from_rating}** und **{to_rating} Sterne**\n",
        "rating_filter": "* Bewertet mit **{from_rating} Sterne**\n",
        "year_filter": "* Veröffentlicht im Jahr **{year}**\n",
        "rewatch": "* 🔁 Erneut angesehen\n",
        "one_movie_daily_msg": "An diesem Tag im Jahr {year} hast du [{m_name} ({m_year})]({m_uri}) gesehen. Du hast ihm {m_rating} gegeben.",
        "daly_msg_start": "An diesem Tag hast du mehrere bemerkenswerte Filme gesehen: \n",
        "many_movies_daily_msg": "* Im Jahr {year} hast du {name} ({m_year}) gesehen.",
        "start_page_markdown": "# Willkommen bei Chatboxd!\n\nUm loszulegen, stellen Sie die Sprache ein, in der Sie die App verwenden möchten.",
        "keys_not_set": "🔴 Agent konnte nicht initialisiert werden, bitte stellen Sie sicher, dass Sie Ihre Schlüssel richtig in secrets.env eingerichtet haben",
        "suggestions_label": "Weißt du nicht, was zu fragen ist? Du kannst eine dieser Vorschläge wählen:",
        "suggestions_list": [
            "Was sind meine Top 10 Lieblingsfilme?",
            "Welche Filme habe ich mit 1 Stern bewertet?",
            "Welche Filme habe ich letzten 3 Monate gesehen?",
            "Was war meine letzte Bewertung?",
            "Welche Filme habe ich dieses Jahr gesehen?",
            "Erstelle einen Graphen der Filme des letzten Jahres",
        ],
    },
    "IT": {
        "select_language": "Seleziona la tua lingua",
        "select_model": "Seleziona un LLM",
        "available_provider": "✅ Provider {provider} disponibile",
        "not_available_provider": "⚠️ Provider {provider} non disponibile",
        "not_openai_api_key": "⚠️ OpenAI API Key non trovato",
        "reset_chat": "Reimposta Conversazione",
        "configure_app": "Impostazioni",
        "chat_placeholder": "Scrivi qui il tuo messaggio...",
        "header_caption": "Chatboxd ti permette di chattare con le tue statistiche di LetterBoxd!",
        "chat_loading": "Generazione della risposta...",
        "continue": "Continua",
        "reviews_filter_loading": "Ricerca recensioni con i seguenti filtri:\n",
        "reviews_loading": "Ricerca recensioni...\n",
        "film_filter_loading": "Ricerca film con i seguenti filtri:\n",
        "film_loading": "Ricerca film...\n",
        "title_filter": "* Titolo: {name}",
        "date_range_filter": "* Visti dal **{from_date}** al **{to_date}**\n",
        "date_to_filter": "* Visti prima di **{to_date}**\n",
        "rating_range_filter": "* Valutati tra **{from_rating}** e **{to_rating} stelle**\n",
        "rating_filter": "* Valutati con **{from_rating} stelle**\n",
        "year_filter": "* Rilasciati nell'anno **{year}**\n",
        "rewatch": "* 🔁 Rivisto\n",
        "one_movie_daily_msg": "In questo giorno del {year}, hai visto [{m_name} ({m_year})]({m_uri}). Gli hai dato un voto di {m_rating}.",
        "daly_msg_start": "In questo giorno, hai visto diversi film notevoli: \n",
        "many_movies_daily_msg": "* Nel {year}, hai visto {name} ({m_year}).",
        "start_page_markdown": "# Benvenuto/a su Chatboxd!\n\nPer iniziare, imposta la lingua che desideri utilizzare nell'applicazione.",
        "keys_not_set": "🔴 Impossibile inizializzare l'agente, assicurati di aver impostato correttamente le tue chiavi in secrets.env",
        "suggestions_label": "Non sai cosa chiedere? Puoi scegliere una di queste suggerimenti:",
        "suggestions_list": [
            "Quali sono i miei film preferiti?",
            "Quali film ho votato 1 stella?",
            "Quali film ho visto negli ultimi 3 mesi?",
            "Qual è la mia ultima recensione?",
            "Quali film ho visto quest'anno?",
            "Fai un grafico dei film dell'anno scorso",
        ],
    },
    "PT": {
        "select_language": "Selecione seu idioma",
        "select_model": "Selecione um LLM",
        "available_provider": "✅ Provedor {provider} disponível",
        "not_available_provider": "⚠️ Provedor {provider} não disponível",
        "not_openai_api_key": "⚠️ OpenAI API Key não encontrado",
        "reset_chat": "Reiniciar conversa",
        "configure_app": "Configurações",
        "chat_placeholder": "Digite sua mensagem aqui...",
        "header_caption": "Chatboxd permite que você converse com suas estatísticas LetterBoxd!",
        "chat_loading": "Gerando resposta...",
        "continue": "Continuar",
        "reviews_filter_loading": "Buscando avaliações com os seguintes filtros:\n",
        "reviews_loading": "Buscando avaliações...\n",
        "movies_loading": "Buscando filmes...\n",
        "rating_filter": "* Avaliados com **{from_rating} estrelas**\n",
        "year_filter": "* Lançados no ano **{year}**\n",
        "rewatch": "* 🔁 Revisão\n",
        "one_movie_daily_msg": "Tal dia como hoje em {year} viu [{m_name} ({m_year})]({m_uri}). Você me deu um {m_rating}.",
        "daly_msg_start": "Tal dia como hoje viu vários filmes de peso: \n",
        "many_movies_daily_msg": "* Em {year} viu {name} ({m_year}).",
        "start_page_markdown": "# Bem-vindo/a ao Chatboxd!\n\nPara começar, configure o idioma que gostaria de usar no aplicativo.",
        "keys_not_set": "🔴 Falha ao inicializar agente, certifique-se de configurar corretamente suas chaves em secrets.env",
        "suggestions_label": "Não sei o que perguntar? Você pode escolher uma dessas sugestões:",
        "suggestions_list": [
            "Quais são meus filmes favoritos?",
            "Quais filmes eu devo avaliar com 1 estrela?",
            "Quais filmes eu vi last 3 meses?",
            "Qual foi minha última avaliação?",
            "Quais filmes eu vi esse ano?",
            "Faça um gráfico dos filmes desse ano passado",
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
    "FR": {
        "get_reviews_response": "L'utilisateur a écrit les critiques suivantes pour les films qu'il a regardés :\n",
        "get_movies_response": "Selon les filtres fournis, l'utilisateur a regardé les films suivants :\n",
        "movie_details_not_found": "Aucun détail du film n'a été trouvé",
        "get_movie_details_response": "🎬 Les détails du film sont (Ajoutez des émojis pour améliorer la présentation visuelle) :\n{movie_detail}\n\nEn aucun cas, vous ne devez afficher une image, un synopsis ou des notes. Le dictionnaire ci-dessous est sans importance pour vous, ne vous y attardez pas.",
        "get_graph_response": "Ne retournez aucune donnée, le graphique sera affiché à l'utilisateur.",
    },
    "DE": {
        "get_reviews_response": "Der Benutzer hat die folgenden Rezensionen zu den Filmen geschrieben, die er gesehen hat:\n",
        "get_movies_response": "Entsprechend den angegebenen Filtern hat der Benutzer die folgenden Filme gesehen:\n",
        "movie_details_not_found": "Keine Filmdetails gefunden",
        "get_movie_details_response": "🎬 Die Details des Films sind (Fügen Sie Emojis hinzu, um es visuell besser zu machen):\n{movie_detail}\n\nUnter keinen Umständen sollten Sie ein Bild, eine Zusammenfassung oder Bewertungen anzeigen. Das untenstehende Wörterbuch ist für Sie irrelevant, ignorieren Sie es.",
        "get_graph_response": "Geben Sie keine Daten zurück, das Diagramm wird dem Benutzer angezeigt.",
    },
    "IT": {
        "get_reviews_response": "L'utente ha scritto le seguenti recensioni dei film che ha visto:\n",
        "get_movies_response": "Secondo i filtri forniti, l'utente ha visto i seguenti film:\n",
        "movie_details_not_found": "Dettagli del film non trovati",
        "get_movie_details_response": "🎬 I dettagli del film sono (Aggiungi emoji per migliorare la visualizzazione):\n{movie_detail}\n\nIn nessun caso devi mostrare un'immagine, una sinossi o le valutazioni. Il dizionario sottostante è irrilevante per te, non farci caso.",
        "get_graph_response": "Non restituire alcun dato, il grafico sarà mostrato all'utente.",
    },
    "PT": {
        "get_reviews_response": "O usuário fez as seguintes análises dos filmes que assistiu:\n",
        "get_movies_response": "De acordo com os filtros fornecidos, o usuário assistiu aos seguintes filmes:\n",
        "movie_details_not_found": "Nenhum detalhe do filme foi encontrado",
        "get_movie_details_response": "🎬 Os detalhes do filme são (Adicione emojis para melhorar visualmente):\n{movie_detail}\n\nEm nenhuma circunstância você deve mostrar uma imagem, sinopse ou classificações. O dicionário abaixo é irrelevante para você, ignore-o.",
        "get_graph_response": "Não retorne nenhum dado, o gráfico será exibido ao usuário.",
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
    "FR": {
        "Ollama": """**Ollama** vous permet d'exécuter un modèle de langage à votre propre appareil.

Pour l'utiliser, vous devez d'abord l'installer sur votre machine et télécharger le modèle que vous souhaitez utiliser, en exécutant `ollama pull <model_name>` (assurez-vous que le même modèle figure dans la liste autorisée de `llm_service.py`).

Pour rendre le modèle disponible, exécutez `ollama serve`.

Une fois que vous avez terminé, vous pouvez commencer à discuter avec **Chatboxd**.
""",
        "OpenAI": """**OpenAI** vous permet d'accéder aux modèles de langage à travers leur API.

Pour commencer, vous devez vous inscrire sur la plateforme et obtenir vos identifiants d'API. Une fois que vous avez vos identifiants, vous devez les stocker dans des variables d'environnement ou dans le fichier `secrets.env`:

```
OPENAI_API_KEY=...
```

Après cela, vous pouvez commencer à utiliser **Chatboxd**. Notez que l'utilisation de l'API OpenAI peut entraîner des frais.
""",
        "Google": """**Google** vous permet d'accéder à des modèles de langage à travers leur API.

Pour commencer, vous devez vous inscrire sur la plateforme et obtenir vos identifiants d'API. Une fois que vous avez vos identifiants, vous devez les stocker dans des variables d'environnement ou dans le fichier `secrets.env`:

```
GOOGLE_API_KEY=...
```

Une fois que vous avez vos identifiants, vous pouvez commencer à discuter avec **Chatboxd**. Notez que l'utilisation de l'API de Gemini peut entraîner des frais.""",
        "Groq": """**Groq** vous permet d'accéder à des modèles de langage à travers leur API.

Pour commencer, vous devez vous inscrire sur https://console.groq.com et obtenir vos identifiants d'API. Une fois que vous avez vos identifiants, vous devez les stocker dans des variables d'environnement ou dans le fichier `secrets.env`:

```
GROQ_API_KEY=...
```

Une fois que vous avez vos identifiants, vous pouvez commencer à discuter avec **Chatboxd**. Notez que l'utilisation de l'API de Groq peut entraîner des frais.""",
        "OpenRouter": """**OpenRouter** vous permet d'accéder à des modèles de langage à travers leur API, y compris des modèles gratuits.

Pour commencer, vous devez vous inscrire sur https://openrouter.ai/keys et obtenir vos identifiants d'API. Une fois que vous avez vos identifiants, vous devez les stocker dans des variables d'environnement ou dans le fichier `secrets.env`:

```
OPENROUTER_API_KEY=...
```

Le catalogue commence par `openrouter/free` et d'autres modèles `:free` qui prennent en charge les outils. Une fois que vous avez vos identifiants, vous pouvez commencer à discuter avec **Chatboxd**. OpenRouter propose aussi des modèles payants absents de cette liste, et leur utilisation peut entraîner des frais.""",
    },
    "DE": {
        "Ollama": """**Ollama** ermöglicht es Ihnen, ein Sprachmodell auf Ihrem eigenen Gerät auszuführen.

Dazu müssen Sie Ollama auf Ihrem System installieren und das zu verwendende Modell mit `ollama pull <model_name>` herunterladen (stellen Sie sicher, dass dasselbe Modell auf der Zulassungsliste in `llm_service.py` steht).

Um das Modell bereitzustellen, führen Sie `ollama serve` aus.

Sobald dies erledigt ist, können Sie mit **Chatboxd** chatten.
""",
        "OpenAI": """**OpenAI** ermöglicht den Zugriff auf Sprachmodelle über seine API.

Um zu beginnen, müssen Sie sich auf der Plattform registrieren und Ihre API-Anmeldedaten erhalten. Sobald Sie Ihre Anmeldedaten haben, sollten Sie diese in Umgebungsvariablen oder in der Datei `secrets.env` speichern:

```
OPENAI_API_KEY=...
```

Nachdem die Anmeldedaten konfiguriert wurden, können Sie mit **Chatboxd** chatten. Beachten Sie, dass die Nutzung der OpenAI-API Kosten verursachen kann.
""",
        "Google": """**Google** ermöglicht den Zugriff auf Sprachmodelle über ihre API.

Um zu beginnen, müssen Sie sich auf der Plattform registrieren und Ihre API-Anmeldedaten erhalten. Sobald Sie Ihre Anmeldedaten haben, sollten Sie diese in Umgebungsvariablen oder in der Datei `secrets.env` speichern:

```
GOOGLE_API_KEY=...
```

Nachdem die Anmeldedaten konfiguriert wurden, können Sie mit **Chatboxd** chatten. Beachten Sie, dass die Nutzung der Gemini-API Kosten verursachen kann.""",
        "Groq": """**Groq** ermöglicht den Zugriff auf Sprachmodelle über ihre API.

Um zu beginnen, müssen Sie sich auf https://console.groq.com registrieren und Ihre API-Anmeldedaten erhalten. Sobald Sie Ihre Anmeldedaten haben, sollten Sie diese in Umgebungsvariablen oder in der Datei `secrets.env` speichern:

```
GROQ_API_KEY=...
```

Nachdem die Anmeldedaten konfiguriert wurden, können Sie mit **Chatboxd** chatten. Beachten Sie, dass die Nutzung der Groq-API Kosten verursachen kann.""",
        "OpenRouter": """**OpenRouter** ermöglicht den Zugriff auf Sprachmodelle über ihre API, einschließlich kostenloser Modelle.

Um zu beginnen, müssen Sie sich auf https://openrouter.ai/keys registrieren und Ihre API-Anmeldedaten erhalten. Sobald Sie Ihre Anmeldedaten haben, sollten Sie diese in Umgebungsvariablen oder in der Datei `secrets.env` speichern:

```
OPENROUTER_API_KEY=...
```

Der Katalog beginnt mit `openrouter/free` und weiteren `:free`-Modellen mit Tool-Unterstützung. Nachdem die Anmeldedaten konfiguriert wurden, können Sie mit **Chatboxd** chatten. OpenRouter bietet auch kostenpflichtige Modelle, die nicht in dieser Liste stehen, und deren Nutzung kann Kosten verursachen.""",
    },
    "PT": {
        "Ollama": """**Ollama** permite que você execute um modelo de linguagem em seu próprio dispositivo.

Para isso, você precisará instalar o Ollama em seu sistema e baixar o modelo a ser usado com `ollama pull <model_name>` (certifique-se de que o mesmo modelo esteja na lista de permitidos de `llm_service.py`).

Para disponibilizar o modelo, execute `ollama serve`.

Depois de fazer isso, você pode começar a conversar com **Chatboxd**.
""",
        "OpenAI": """**OpenAI** permite o acesso a modelos de linguagem através de sua API.

Para começar, você precisará se registrar na plataforma e obter suas credenciais de API. Depois de obter suas credenciais, armazene-as em variáveis de ambiente ou no arquivo `secrets.env`:

```
OPENAI_API_KEY=...
```

Após configurar as credenciais, você pode começar a conversar com **Chatboxd**. Observe que o uso da API do OpenAI pode acarretar custos.
""",
        "Google": """**Google** permite o acesso a modelos de linguagem através de sua API.

Para começar, você precisará se registrar na plataforma e obter suas credenciais de API. Depois de obter suas credenciais, armazene-as em variáveis de ambiente ou no arquivo `secrets.env`:

```
GOOGLE_API_KEY=...
```

Após configurar as credenciais, você pode começar a conversar com **Chatboxd**. Observe que o uso da API de Gemini pode acarretar custos.""",
        "Groq": """**Groq** permite o acesso a modelos de linguagem através de sua API.

Para começar, você precisará se registrar em https://console.groq.com e obter suas credenciais de API. Depois de obter suas credenciais, armazene-as em variáveis de ambiente ou no arquivo `secrets.env`:

```
GROQ_API_KEY=...
```

Após configurar as credenciais, você pode começar a conversar com **Chatboxd**. Observe que o uso da API de Groq pode acarretar custos.""",
        "OpenRouter": """**OpenRouter** permite o acesso a modelos de linguagem através de sua API, incluindo modelos gratuitos.

Para começar, você precisará se registrar em https://openrouter.ai/keys e obter suas credenciais de API. Depois de obter suas credenciais, armazene-as em variáveis de ambiente ou no arquivo `secrets.env`:

```
OPENROUTER_API_KEY=...
```

O catálogo começa com `openrouter/free` e outros modelos `:free` com suporte a ferramentas. Após configurar as credenciais, você pode começar a conversar com **Chatboxd**. A OpenRouter também oferece modelos pagos que não estão nesta lista, e usá-los pode acarretar custos.""",
    },
    "IT": {
        "Ollama": """**Ollama** permette di eseguire un modello di linguaggio sul tuo dispositivo.

Per utilizzare Ollama, prima devi installarlo sul tuo sistema e scaricare il modello che vuoi utilizzare, eseguendo `ollama pull <model_name>` (assicurati che lo stesso modello sia nella lista consentita di `llm_service.py`).

Per rendere il modello disponibile, esegui `ollama serve`.

Una volta fatto, puoi iniziare a chattare con **Chatboxd**.
""",
        "OpenAI": """**OpenAI** permette di accedere a modelli di linguaggio attraverso la loro API.

Per iniziare, devi registrarti sulla piattaforma e ottenere le tue credenziali API. Una volta ottenute le tue credenziali, devi memorizzarle in variabili di ambiente o nel file `secrets.env`:

```
OPENAI_API_KEY=...
```

Una volta configurate le credenziali, puoi iniziare a conversare con **Chatboxd**. Nota che l'utilizzo dell'API OpenAI può comportare costi.
""",
        "Google": """**Google** permette di accedere a modelli di linguaggio attraverso la loro API.

Per iniziare, devi registrarti sulla piattaforma e ottenere le tue credenziali API. Una volta ottenute le tue credenziali, devi memorizzarle in variabili di ambiente o nel file `secrets.env`:

```
GOOGLE_API_KEY=...
```

Una volta configurate le credenziali, puoi iniziare a conversare con **Chatboxd**. Nota che l'utilizzo dell'API Gemini può comportare costi.""",
        "Groq": """**Groq** permette di accedere a modelli di linguaggio attraverso la loro API.

Per iniziare, devi registrarti su https://console.groq.com e ottenere le tue credenziali API. Una volta ottenute le tue credenziali, devi memorizzarle in variabili di ambiente o nel file `secrets.env`:

```
GROQ_API_KEY=...
```

Una volta configurate le credenziali, puoi iniziare a conversare con **Chatboxd**. Nota che l'utilizzo dell'API Groq può comportare costi.""",
        "OpenRouter": """**OpenRouter** permette di accedere a modelli di linguaggio attraverso la loro API, inclusi modelli gratuiti.

Per iniziare, devi registrarti su https://openrouter.ai/keys e ottenere le tue credenziali API. Una volta ottenute le tue credenziali, devi memorizzarle in variabili di ambiente o nel file `secrets.env`:

```
OPENROUTER_API_KEY=...
```

Il catalogo inizia con `openrouter/free` e altri modelli `:free` con supporto per gli strumenti. Una volta configurate le credenziali, puoi iniziare a conversare con **Chatboxd**. OpenRouter offre anche modelli a pagamento assenti da questa lista, e usarli può comportare costi.""",
    },
}
