import backend.scrape as scrape
import backend.uncaught_pokemon as uncaught_pokemon

def main():
    print("Running scrape.py to detect caught Pokémon...")
    scrape.main()  # Run scrape script that outputs caught_pokemon.json

    print("\nRunning uncaught_pokemon.py to find uncaught Pokémon...")
    uncaught_pokemon.main()  # Run uncaught Pokémon comparison script

    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()
