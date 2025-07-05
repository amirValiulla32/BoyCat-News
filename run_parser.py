# run_parser.py
from db import get_feed_configs
from app.rss.collector import fetch_latest
from app.rss.filter import keyword_filter
from save_articles_to_supabase import save_articles_to_supabase
from app.rss.utils import get_best_logo_url


##can be changed to any campaign, eventually the campaigns will be determined by the user for the main web app, for boycat Times, it will be the blog post, ex: openai-defense-campaign
# Campaign keywords are the keywords that will be used to filter the articles, they are the keywords
CAMPAIGN_KEYWORDS = ["Gaza","Palestine","West Bank","Hamas","Israeli","West Bank","IDF","Israeli Defense Forces","Israeli Air Force","Israeli Army","Israeli Navy","Israeli Settlements","Israeli Settler","Israeli Settlers",
                     "Israeli Occupation","Israeli Occupied Territories","Israeli Government","Israeli Politics","Israeli Elections","Israeli Prime Minister","Benjamin Netanyahu",
                     "Naftali Bennett","Yair Lapid","Gantz","Genocide","War Crimes","Human Rights Violations","Apartheid","Ethnic Cleansing","Displacement","Forced Evictions",
                     "Blockade","Siege","Military Operations","Airstrikes","Rocket Attacks","Ceasefire","Peace Talks","Two-State Solution","One-State Solution","International Law","UN Resolutions",
                     "BDS Movement","Boycott","Divestment","Sanctions","Palestinian Authority","Fatah","Hamas","Islamic Jihad","PLO","Palestinian Liberation Organization","Palestinian Territories","zara-big-fashion-glilot-boycott"]
BRAND_KEYWORDS = [
  "OLEHENRIKSEN",
  "Arla Yoggi",
  "Tic Tac",
  "Haagen-Dazs",
  "Arla Köket",
  "Keso",
  "Cinnabon",
  "Donut Shop",
  "Popeyes Louisiana Kitchen",
  "Trix",
  "Oreo",
  "SkinnyPop",
  "5 Gum",
  "Bartar",
  "Clorets",
  "Sabra",
  "Quaker",
  "Bagel Bites",
  "Baken-Ets",
  "Karolines Køkken",
  "York",
  "Balisto",
  "Carnation",
  "Pasta Roni",
  "Funyuns",
  "Maggi",
  "Annie's",
  "Betty Crocker",
  "Special K",
  "SunChips",
  "Rold Gold",
  "Heinz",
  "Febreze",
  "DryNites",
  "Maelys",
  "Kinder",
  "Hilo Life",
  "Mobileye",
  "Trader Joe's Made in Israel",
  "Marks & Spencer",
  "Vita Coco",
  "Milo",
  "SodaStream",
  "Arla Cheasy",
  "Lunchables",
  "Jack Link's",
  "Arla Cheese",
  "Lily's",
  "Mr. Goodbar",
  "Monster Cereals",
  "Hot Pockets",
  "PopCorners",
  "Zagnut",
  "KIND Bar",
  "Total",
  "Mounds",
  "Oui",
  "Chicken in a Biskit",
  "Toasteds",
  "La Grande Epicerie de Paris",
  "One Brands",
  "Maui Style",
  "Magnum",
  "Raisin Bran",
  "Starbursts",
  "Ritz",
  "Wheat Thins",
  "Philadelphia",
  "3 Musketeers",
  "Make Up For Ever",
  "Nature Valley",
  "Tru Fru",
  "Power Action",
  "Ben's Originals",
  "Prologic ITS",
  "Lemonade",
  "Barclays Bank",
  "Intel",
  "TKH Security",
  "Little Swimmers",
  "Minute Maid",
  "Arla Protein",
  "Fritos",
  "Stride",
  "Agrifood Marketing",
  "Ethel M Chocolates",
  "Galaxy",
  "Cornetto Ice Creams",
  "Kotex Anydays",
  "Breyers",
  "Jolly Rancher",
  "Good Measure",
  "Delta Galil Industries",
  "Carrefour",
  "Milka",
  "Tiger",
  "7DAYS",
  "Kent",
  "Alpen Gold",
  "Khazana"
];  
MAX_RESULTS = 5

def run_parser_job():
    feed_configs = get_feed_configs()
    print("Loaded Feeds:", [f["url"] for f in feed_configs])

    for feed in feed_configs:
        url = feed["url"]

        raw_articles = fetch_latest(limit=1000, feed_urls=[url])
        keywords = CAMPAIGN_KEYWORDS + BRAND_KEYWORDS
        filtered = keyword_filter(raw_articles, keywords, max_results=MAX_RESULTS)

        for article in filtered:
            logo_url = get_best_logo_url(feed["url"], article["url"])
            print(f"{'title:':12} {article['title']}")
            print(f"{'url:':12} {article['url']}")
            print(f"{'published at:':12} {article['published_at']}")
            print(f"{'source:':12} {article['source']}")
            print(f"{'summary:':12} {article['summary']}")
            print(f"{'logo_url:':12} {logo_url}")
            print("-" * 50)
        if filtered:
            save_articles_to_supabase(filtered, feed)

def main():
    """CLI entry‑point – simply runs the parser job."""
    run_parser_job()

if __name__ == "__main__":
    run_parser_job()
