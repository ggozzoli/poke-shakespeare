# poke-shakespeare
Shakespeare's style Pokémon descriptions

sudo apt install python3-pip
source venv/bin/activate
pip3 install -r requirements.txt

docker-compose up --build -d poke-shakespeare
docker-compose logs -f poke-shakespeare
