from unittest import TestCase

import requests


class IntegrationTestCase(TestCase):
    base_url = 'http://localhost:5000/pokemon/{pokemonName}'

    def test_retrieve_charizard_description(self):
        url = self.base_url.format(pokemonName='charizard')
        r = requests.get(url=url)
        self.assertEqual(200, r.status_code)
        self.assertEqual('charizard', r.json().get('name'))

    def test_not_found(self):
        r = requests.get(url=self.base_url)
        self.assertEqual(404, r.status_code)

    def test_method_not_allowed(self):
        url = self.base_url.format(pokemonName='charizard')
        r = requests.post(url=url)
        self.assertEqual(405, r.status_code)
