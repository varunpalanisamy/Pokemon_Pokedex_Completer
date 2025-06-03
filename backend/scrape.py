import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import time
import json
import os
import re

print("Script started")

RIGHT_PANEL_REGION = (1190, 250, 140, 550)
BRIGHTNESS_CHECK_POSITIONS = [40, 100, 160, 220, 280]
BRIGHTNESS_THRESHOLD = 120
OUTPUT_FILE = "pokedex_status.json"
NUM_BATCHES = 50
DELAY_BETWEEN_ACTIONS = 1.0

def capture_pokedex_batch(batch_num):
    screenshot = pyautogui.screenshot(region=RIGHT_PANEL_REGION)
    filename = f"screenshots/pokedex_batch_{batch_num:02d}.png"
    os.makedirs("screenshots", exist_ok=True)
    screenshot.save(filename)
    print(f"[DEBUG] Saved screenshot: {filename}")
    return filename

def save_annotated_image(image_path, ocr_text, batch_num):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    y_text = 10
    for line in ocr_text.split("\n"):
        draw.text((10, y_text), line, fill="red", font=font)
        y_text += 18

    annotated_path = f"screenshots/pokedex_batch_{batch_num:02d}_annotated.png"
    img.save(annotated_path)
    print(f"[DEBUG] Saved annotated OCR image: {annotated_path}")

def clean_ocr_lines(lines):
    """
    Remove common OCR artifacts (like 'et', 'le', 'll') that aren't Pokémon numbers or names.
    We'll keep lines that match 'No.' pattern or look like Pokémon names.
    """
    cleaned = []
    for line in lines:
        line_lower = line.lower()
        # Keep lines that look like a Pokemon number line (e.g. "no. 072", "no, 074")
        if re.match(r"no[.,]?\s*\d+", line_lower):
            cleaned.append(line)
        # Keep lines that look like a Pokemon name (only letters, spaces, hyphens)
        elif re.match(r"^[a-z\s\-]+$", line_lower):
            cleaned.append(line)
        else:
            # skip likely OCR noise like 'et', 'le', 'll', or other garbage
            pass
    return cleaned

def extract_pokemon_names_and_numbers(image_path, batch_num):
    img_pil = Image.open(image_path)

    ocr_text = pytesseract.image_to_string(img_pil)
    print(f"[DEBUG] OCR raw text for batch {batch_num}:\n{ocr_text}")

    save_annotated_image(image_path, ocr_text, batch_num)

    raw_lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]
    lines = clean_ocr_lines(raw_lines)
    print(f"[DEBUG] Cleaned OCR lines: {lines}")

    # The OCR lines should come in pairs: number line then name line
    pokemon_batch = []
    i = 0
    while i < len(lines) - 1:
        number_line = lines[i].lower()
        name_line = lines[i+1].lower()

        # Fix number_line format to standard "No. XXX"
        number_match = re.search(r"(no[.,]?\s*\d+)", number_line)
        number = number_match.group(1).replace(",", ".").replace(" ", "") if number_match else None
        name = name_line.strip()

        if number and re.match(r"^[a-z\s\-]+$", name):
            pokemon_batch.append({"number": number, "name": name})
            print(f"[DEBUG] Detected Pokémon: {number} {name}")
            i += 2
        else:
            # If parsing fails, try to skip a line to resync pairs
            i += 1

    return pokemon_batch

def main():
    all_pokemon = []

    print("Starting Pokédex batch screenshot and OCR scan...")
    time.sleep(3)  # switch to emulator

    for batch_num in range(NUM_BATCHES):
        print(f"Capturing batch {batch_num + 1}/{NUM_BATCHES}...")
        filename = capture_pokedex_batch(batch_num)
        batch_pokemon = extract_pokemon_names_and_numbers(filename, batch_num)
        all_pokemon.extend(batch_pokemon)

        pyautogui.press('d')
        print("[DEBUG] Pressed 'd' to scroll down by 5")
        time.sleep(DELAY_BETWEEN_ACTIONS)

    # Remove duplicates by 'number' (keep first occurrence)
    unique_pokemon = []
    seen_numbers = set()
    for p in all_pokemon:
        if p["number"] not in seen_numbers:
            unique_pokemon.append(p)
            seen_numbers.add(p["number"])

    # Save JSON with just number and name, no status
    with open(OUTPUT_FILE, "w") as f:
        json.dump(unique_pokemon, f, indent=2)

    print(f"Pokédex scan complete! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
