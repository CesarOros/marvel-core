URL = "http://gateway.marvel.com/v1/public"
API_KEY = "1e0644ead7d2bff40f063b6c43c974ba"
API_HASH = "66477e78833cccd5c7412e84ea917628"
TS = "1"
AUTHENTICATION_HEADER = f"?ts={TS}&apikey={API_KEY}&hash={API_HASH}"

CHARACTERS = "characters"
COMICS = "comics"

SEARCH_TYPE_KEY = {"personajes": CHARACTERS, "comics": COMICS}
