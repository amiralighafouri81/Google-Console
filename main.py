from Console import Console

console = Console(api_key_file='API_KEY', search_engine_id_file='SEARCH_ENGINE_ID')
search_query = input('Enter search query: ')
console.autocomplete_and_search(search_query)