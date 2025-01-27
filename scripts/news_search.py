import os
import requests
import csv
import argparse
from datetime import datetime, timedelta, timezone

def search_news(output_path):
    companies = ["Kata.ai Indonesia", "SCAI Therapeutics", "Vexere Vietnam", "Spoon Korea", "Awair air quality", 
                 "Volantis Indonesia", "Ecotruck Vietnam", "Zuzu Hospitality", "Koobits", "Common Computer Korea",
                 "Perx Technologies", "Andalin Indonesia", "Abivin Vietnam", "PFC Technologies", "Akseleran Indonesia",
                 "Seoul Robotics", "Viec.co Vietnam", "Palexy Vietnam", "Revival TV Indonesia", "Credolab",
                 "Staffinc Indonesia", "Pion VCAT", "Aitomatic Semiconductor", "Volopay", "Coolmate Vietnam",
                 "Quotabook Korea", "Locad Logistics", "Plugo Indonesia", "M Village Vietnam", "Ulift Coding Valley",
                 "Phlox Korea", "Helicap Singapore"]
    api_url = "https://newsapi.org/v2/everything"
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        raise ValueError("NEWS_API_KEY environment variable is not set.")
    
    headers = {"X-Api-Key": api_key}
    today = datetime.now(timezone.utc)
    month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    
    results = []
    for company in companies:
        try:
            params = {
                "q": company,
                "from": month_ago,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 30
            }
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()  
            
            articles = response.json().get("articles", [])
            for article in articles:
                results.append({
                    "Company": company,
                    "Title": article.get("title", ""),
                    "Description": article.get("description", ""),
                    "URL": article.get("url", ""),
                    "PublishedAt": article.get("publishedAt", "")
                })
        except requests.RequestException as e:
            print(f"Error fetching news for {company}: {e}")
            results.append({
                "Company": company,
                "Title": "Error",
                "Description": str(e),
                "URL": "",
                "PublishedAt": ""
            })
    
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Company", "Title", "Description", "URL", "PublishedAt"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"News results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search news and save to a CSV file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output CSV file.")
    args = parser.parse_args()
    
    search_news(args.output)
