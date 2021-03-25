import fire
import requests


class ApiTester:
    """CLI for testing Things API"""

    def __init__(self, host="http://localhost:8000"):
        self.host = host

    def fetch_tokens(self):
        """Fetches access and refresh JWT tokens from api

        Returns:
            tuple: access,refresh
        """

        token_url = f"{self.host}/api/token/"

        response = requests.post(
            token_url, json={"username": "admin", "password": "admin"}
        )

        data = response.json()

        tokens = data["access"], data["refresh"]

        return tokens

    def get_things(self):
        """get list of all things from api
        Usage: python api_tester.py get_things

        Returns: JSON
        """
        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/things/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def get_thing(self, id):
        """get 1 thing by id from api

        Usage:
        python api_tester.py get_thing 1

        Returns: JSON
        """
        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/things/{id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json()

    def create_thing(self, name, description=None, owner=None):
        """creates a thing in api

        Usage:
        python api_tester.py create_thing /
            --name=required --description=optional --owner=optional

        Returns: JSON
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/things/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        data = {
            "name": name,
            "description": description,
            "owner": owner,
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def update_thing(self, id, name=None, description=None, owner=None):
        """updates a thing in api

        Usage:
        python api_tester.py update_thing 1 /
            --name=optional --description=optional --owner=optional

        Returns: JSON
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/things/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        original_thing = self.get_thing(id)

        data = {
            "name": name or original_thing["name"],
            "description": description or original_thing["description"],
            "owner": owner or original_thing["owner"],
        }

        response = requests.put(url, json=data, headers=headers)

        return response.text

    def delete_thing(self, id):
        """deletes a thing in api

        Usage:
        python api_tester.py delete_thing 1

        Returns: Empty string if no error
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/things/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.delete(url, headers=headers)

        return response.text


if __name__ == "__main__":
    fire.Fire(ApiTester)
