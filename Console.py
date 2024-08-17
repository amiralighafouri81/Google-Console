import requests


class Console:
    def __init__(self, api_key_file, search_engine_id_file):
        # Load API key and Search Engine ID from files
        self.api_key = self._load_file(api_key_file)
        self.search_engine_id = self._load_file(search_engine_id_file)
        self.autocomplete_url = 'https://suggestqueries.google.com/complete/search'
        self.search_url = 'https://www.googleapis.com/customsearch/v1'

    def _load_file(self, file_path):
        """Load content from a file and strip any extra whitespace."""
        with open(file_path, 'r') as file:
            return file.read().strip()

    def search_results(self, query, max_results=10):
        """Fetch and print URL, snippet, and image from search results."""
        start_index = 1
        results_fetched = 0

        while results_fetched < max_results:
            params = {
                'q': query,
                'key': self.api_key,
                'cx': self.search_engine_id,
                'start': start_index
            }
            response = requests.get(self.search_url, params=params)
            results = response.json()

            # Debug: Print the entire response to inspect its structure
            print("Response JSON:", results)

            if 'items' in results:
                for item in results['items']:
                    if results_fetched >= max_results:
                        return
                    title = item.get('title')
                    snippet = item.get('snippet')
                    image = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
                    link = item.get('link')

                    # Debug: Print extracted values to ensure they are being fetched
                    print(f"Extracted image URL: {image}")

                    print(f"Title: {title}")
                    print(f"Snippet: {snippet}")
                    print(f"Image: {image}")
                    print(f"Link: {link}")
                    print()
                    results_fetched += 1
            else:
                break
            start_index += 10

    def pdf_urls(self, query, max_results=10, start_index=1):
        """Fetch and print URLs of PDF results."""
        pdf_urls = []
        results_fetched = 0

        while results_fetched < max_results:
            params = {
                'q': query + ' filetype:pdf',
                'key': self.api_key,
                'cx': self.search_engine_id,
                'start': start_index
            }
            response = requests.get(self.search_url, params=params)
            results = response.json()

            # Debug: Print the entire response to inspect its structure
            print("Response JSON for PDFs:", results)

            if 'items' in results:
                for item in results['items']:
                    if results_fetched >= max_results:
                        return pdf_urls
                    pdf_url = item.get('link')
                    print(pdf_url)
                    pdf_urls.append(pdf_url)
                    results_fetched += 1
            else:
                break
            start_index += 10
        return pdf_urls

    def autocomplete_suggestions(self, query):
        """Fetch and print autocomplete suggestions."""
        params = {
            'client': 'chrome',
            'q': query
        }
        response = requests.get(self.autocomplete_url, params=params)
        suggestions = response.json()[1]
        print("Autocomplete suggestions:")
        for suggestion in suggestions:
            print(suggestion)
