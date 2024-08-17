import requests


class Console:
    def __init__(self, api_key_file, search_engine_id_file):
        # Load API key and Search Engine ID from files
        self.api_key = self._load_file(api_key_file)
        self.search_engine_id = self._load_file(search_engine_id_file)
        self.autocomplete_url = 'https://suggestqueries.google.com/complete/search'
        self.search_url = 'https://www.googleapis.com/customsearch/v1'
        self.results_info = []

    def _load_file(self, file_path):
        """Load content from a file and strip any extra whitespace."""
        with open(file_path, 'r') as file:
            return file.read().strip()

    def fetch_autocomplete_suggestions(self, query):
        """Fetch autocomplete suggestions from Google."""
        params = {
            'client': 'chrome',
            'q': query
        }
        response = requests.get(self.autocomplete_url, params=params)
        suggestions = response.json()[1]
        return suggestions

    def fetch_search_results(self, query, start_index):
        """Fetch search results from Google Custom Search API."""
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'start': start_index
        }
        response = requests.get(self.search_url, params=params)
        return response.json()

    def process_results(self, results):
        """Process search results to extract title, snippet, and image."""
        if 'items' in results:
            for item in results['items']:
                if len(self.results_info) >= 10:
                    return False
                title = item.get('title')
                snippet = item.get('snippet')
                image = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
                link = item.get('link')
                self.results_info.append({'title': title, 'snippet': snippet, 'image': image, 'link': link})
        return True

    def search(self, query):
        """Perform a search and collect results."""
        start_index = 1
        while start_index <= 10:
            results = self.fetch_search_results(query, start_index)
            if not self.process_results(results):
                break
            if 'items' not in results:
                break
            start_index += 10

    def print_results(self):
        """Print the collected search results."""
        print("\nSearch Results:")
        for info in self.results_info:
            print(f"Title: {info['title']}")
            print(f"Snippet: {info['snippet']}")
            print(f"Image: {info['image']}")
            print(f"Link: {info['link']}")
            print()
