from Console import Console

console = Console(api_key_file='API_KEY', search_engine_id_file='SEARCH_ENGINE_ID')
search_query = input('Enter search query: ')
max_results = int(input('Enter number of results to see: '))

# Print search results
console.search_results(search_query, max_results=max_results)

# Print PDF URLs
console.pdf_urls(search_query, max_results=max_results)

# Print autocomplete suggestions
console.autocomplete_suggestions(search_query)
