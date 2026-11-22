import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

load_dotenv()
base_url = "https://go.apis.huit.harvard.edu/ats/dining/v3"
headers = {"X-Api-Key": os.getenv("DINING_API_KEY")}
berg_name = "Annenberg Hall"

today = datetime.now(ZoneInfo("America/New_York")).date()
wanted_dates = {today + timedelta(days=offset) for offset in range(4)}

# Get location ID of Annenberg
locations = requests.get(base_url+"/locations", headers=headers).json()
berg_id = None
for location in locations:
    if location["location_name"] == berg_name:
        berg_id = location["location_number"]
        break
# If unavailable, report error
if not berg_id:
    raise KeyError("The location ID of Annenberg is unavailable from the API.")


def parse_recipe(recipe):
    excluded_fields = {
        "Recipe_Name",
        "Recipe_Print_As_Character",
        "Recipe_Print_As_Color",
        "Recipe_Product_Information",
        "portion_cost",
        "selling_price",
    }
    parsed = {key: value for key, value in recipe.items() if key not in excluded_fields}
    codes = recipe.get("Recipe_Web_Codes", "")
    parsed["Recipe_Web_Codes"] = codes.split() if isinstance(codes, str) else codes
    return parsed


def fetch_meals():
    meals = []
    for date in wanted_dates:
        response = requests.get(
            "https://go.apis.huit.harvard.edu/ats/dining/v3/recipes",
            headers=headers,
            params={"date": date.strftime("%m/%d/%Y"), "locationId": berg_id},
            timeout=15,
        )
        response.raise_for_status()
        meals.extend(parse_recipe(recipe) for recipe in response.json())

    parsed_meals = [parse_recipe(recipe) for recipe in meals]
    return parsed_meals


def main():
    meals = fetch_meals()
    for meal in meals: print(meal)


if __name__ == "__main__":
    main()
