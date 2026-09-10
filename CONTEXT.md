# Chatboxd

Chat with a Letterboxd diary and reviews through an Agent that calls Tools.

## Letterboxd store

**Letterboxd store**:
The Diary and Review loaded from one Letterboxd export. Schema, ingest, and queries live here.
_Avoid_: database, sqlite service

**Letterboxd export**:
The `diary.csv` and `reviews.csv` files from Letterboxd. A load replaces the store.

**Diary**:
A watch: title, year, rating, watched date, rewatch, Letterboxd URL, optional link to a Review, and the username the caller passed on ingest.

**Review**:
The user's written text about a film, optionally linked from a Diary row when title and date match.

**Username**:
The Letterboxd person this store belongs to. Callers pass it on ingest; the store does not invent it.

**On this day**:
Diary watches whose watched date falls on today's month and day, used for the daily message.

## Chat

**Chat event**:
An item in the chat stream the UI understands: token, status, movie card, graph, error, or done.

**Tool artifact**:
Something a Tool call produces for the UI: a movie card, a graph, or a status line. Not a token, error, or done.
_Avoid_: payload, SSE event, UI event

**Movie card**:
A film's title, Letterboxd URL, image, and optional plot and ratings, shown in chat.

**Graph**:
A rating distribution shown as a chart in chat.

**Status**:
A short progress line shown in chat while a Tool runs, including any filters the Tool was called with.
_Avoid_: HTTP status, loading spinner

**Language**:
Spanish or English. Status and UI copy follow it. Tool observations are English today.

## Agent

**Tool**:
A capability the Agent calls to read the diary or reviews, or to fetch film details.

**Tool observation**:
The text a Tool returns for the Agent to read. Distinct from a Tool artifact.
_Avoid_: payload, tool output

**Agent**:
The ReAct loop that answers the user by calling Tools.
_Avoid_: chatbot, LLM chain

**Provider**:
An LLM host the Agent can call: Google, OpenAI, Ollama, Groq, or OpenRouter. One table is the catalog; table order is the picker preference.
_Avoid_: vendor, backend
