import os
from pathlib import Path
import fire
import requests
from dotenv import load_dotenv

dotenv_path = Path("project/.env")
load_dotenv(dotenv_path=dotenv_path)

# NOTE: Adjust these settings as needed in project/.env
API_HOST = os.getenv("TEST_API_HOST") or "http://localhost:8000"
RESOURCE_URI = os.getenv("TEST_RESOURCE_URI") or "things"
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")


class ApiTester:
    """CLI for testing API
    Server must be running.
    WARNING: Database queries are performed on supplied database.
        So be extra careful and/or use a test database.
    """

    def __init__(self, host=API_HOST):
        self.host = host

    def fetch_tokens(self):
        """Fetches access and refresh JWT tokens from api

        Returns:
            tuple: access,refresh
        """

        token_url = f"{self.host}/api/token/"

        response = requests.post(
            token_url, json={"username": USERNAME, "password": PASSWORD}
        )

        data = response.json()

        tokens = data["access"], data["refresh"]

        return tokens

    def get_all(self):
        """get list of all resources from api
        Usage: python api_tester.py get_all

        Returns: JSON
        """
        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json() or 'No resources'

    def get_one(self, id):
        """get 1 resource by id from api

        Usage:
        python api_tester.py get_one 1

        Returns: JSON
        """
        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)

        return response.json()

    # TODO adjust parameter names to match API
    def create(self, name, description, owner):
        """creates a resource in api

        Usage:
        python api_tester.py create /
            --name=required --description=required --owner=required

        Returns: JSON
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        data = {
            "name": name,
            "description": description,
            "owner": int(owner),
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def update(self, id, name=None, description=None, owner=None):
        """updates a resource in api

        Usage:
        python api_tester.py update 1 /
            --name=optional --description=optional --owner=optional

        Returns: JSON
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        original = self.get_one(id)

        data = {
            "name": name or original["name"],
            "description": description or original["description"],
            "owner": owner or original["owner"],
        }

        response = requests.put(url, json=data, headers=headers)

        return response.text

    def delete(self, id):
        """deletes a resource in api

        Usage:
        python api_tester.py delete 1

        Returns: Empty string if no error
        """

        access_token = self.fetch_tokens()[0]

        url = f"{self.host}/api/v1/{RESOURCE_URI}/{id}/"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.delete(url, headers=headers)

        return response.text


if __name__ == "__main__":
    fire.Fire(ApiTester)
