# poke-shakespeare
Shakespeare's style Pokémon descriptions!

### Technologies:
- Python 3.8
- Flask 1.1.2
- Redis 6.0.5

### API Requirements:

- Retrieve Shakespearean description of a Pokémon given its name.

### **GET** endpoint: 

- **`/pokemon/<pokemonName>`**

**Output format:**
```
{
    "name": "charizard",
    "description": "Spits fire yond is hot enow to melt boulders. Known to cause forest fires unintentionally."
}
```

### Installation instructions:
1. Clone the repository on your system:
    * ```git clone https://github.com/ggozzoli/poke-shakespeare.git```
    
2. Navigate the the cloned repository;
    * ```cd poke-shakespeare```

3. Install Docker (if you have Docker installed you can skip this):
    * https://docs.docker.com/engine/install/
    
4. Builds, create and start the container for the service:
    * ```$ docker-compose up --build -d poke-shakespeare```
    
5. Attach to the container to see logs:
    * ```$ docker-compose logs -f poke-shakespeare```
    
6. Stop the container with:
    * ```$ docker-compose down```

### Usage example:
##### Curl 
```curl http://localhost:5000/pokemon/charizard```
##### httpie 
```http http://localhost:5000/pokemon/charizard```



### Third party APIs:

  - **PokeAPI**: https://pokeapi.co/docs/v2
  - **Shakespeare translator**: https://funtranslations.com/api/shakespeare

### Notes:
poke-shakespeare has a limit of 5 requests per hour per user, due to the shakespeare translator API usage limit. 
Pokémon descriptions are cached, only requests for new Pokémon will be considered for the limit count. 
Exceeding the limit will result in a HTTP 429 response.
