from core.wrappers import PokemonInfoWrapper


class PokemonInfoWrapperImpl(PokemonInfoWrapper):

    def __init__(self):
        url = 'https://pokeapi.co/api/v2/pokemon-species/{pokemonName}'

    def get_description(self, pokemon_name: str) -> str:
        pass
