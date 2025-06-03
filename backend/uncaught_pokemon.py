import json

# File paths - adjust as needed
MASTERED_FILE = "mastered_pokedex.json"
CAUGHT_FILE = "pokedex_status.json"
OUTPUT_FILE = "uncaught_pokedex.json"

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def main():
    mastered = load_json(MASTERED_FILE)  # list of dicts with number, name, location
    caught = load_json(CAUGHT_FILE)      # list of dicts with number, name, status (or just caught names)

    # Extract caught Pokémon names or numbers for quick lookup
    caught_names = set()
    caught_numbers = set()

    # Support both formats: list of dicts with number/name or just list of names
    if isinstance(caught, dict) and "caught" in caught:
        caught_list = caught["caught"]
        # Handle list of dicts or names
        if len(caught_list) > 0 and isinstance(caught_list[0], dict):
            for p in caught_list:
                caught_names.add(p.get("name", "").lower())
                caught_numbers.add(p.get("number", "").lower())
        else:
            for name in caught_list:
                caught_names.add(name.lower())
    elif isinstance(caught, list):
        for p in caught:
            if isinstance(p, dict):
                caught_names.add(p.get("name", "").lower())
                caught_numbers.add(p.get("number", "").lower())
            else:
                caught_names.add(str(p).lower())

    # Find uncaught Pokémon by filtering mastered list
    uncaught = []
    for p in mastered:
        name = p.get("name", "").lower()
        number = p.get("number", "").lower()
        if (name not in caught_names) and (number not in caught_numbers):
            uncaught.append(p)

    # Save uncaught list to JSON
    save_json(uncaught, OUTPUT_FILE)
    print(f"Saved {len(uncaught)} uncaught Pokémon to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
