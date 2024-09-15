class fti18n:
    def fetch_translation_selected_language(selected_language, key):
        try:
            url = f'http://localhost:8006/translations/{selected_language}/{key}/'
            response = ftrequests.get(url)

            response.raise_for_status()

            data = response.json()

            return data.get(key, None)
        
        except ftrequests.exceptions.RequestException as error:
            return None
