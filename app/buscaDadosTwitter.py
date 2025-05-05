import requests
import time
import json
import os
from datetime import datetime


def dadosUsuario(usuario):
    if not usuario or usuario.strip() == "":
        print("Nome de usuário vazio ou inválido")
        return None

    # Better practice: Get token from environment variables
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN",
                             "AAAAAAAAAAAAAAAAAAAAAPMI1AEAAAAAkoXiBrhPF884MdIrqJn4Uma%2FTWA%3DJy7WAgC6cIUgQQM2fqjNAfiXyZyYYYtPla8OFDSga5sXmYtmum")
    headers = {"Authorization": f"Bearer {bearer_token}"}

    try:
        # First, check user existence and get profile info with retry logic
        user_url = f"https://api.twitter.com/2/users/by/username/{usuario}?user.fields=description,public_metrics,profile_image_url,created_at"

        user_data = None
        max_retries = 3
        retry_delay = 2  # Start with 2 seconds

        for attempt in range(max_retries):
            user_response = requests.get(user_url, headers=headers)

            if user_response.status_code == 200:
                user_data = user_response.json()
                break
            elif user_response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)  # Exponential backoff
                    print(f"Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {"error": "Twitter API rate limit exceeded after multiple retries"}
            else:
                error_message = f"Error fetching user: {user_response.status_code} {user_response.text}"
                print(error_message)
                return {"error": error_message}

        if not user_data or 'data' not in user_data:
            return {"error": "User not found or data unavailable"}

        # Now search for tweets with "fúria" with similar retry logic
        tweets_data = []
        search_url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{usuario} fúria&max_results=10&tweet.fields=created_at,public_metrics"

        for attempt in range(max_retries):
            tweets_response = requests.get(search_url, headers=headers)

            if tweets_response.status_code == 200:
                tweets_data = tweets_response.json().get('data', [])
                break
            elif tweets_response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"Rate limit hit on tweets search. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Rate limit exceeded for tweets search after retries")
                    break  # Continue without tweets rather than failing completely
            else:
                print(f"Error fetching tweets: {tweets_response.status_code}")
                break

        # Prepare results
        furia_mentions = []
        for tweet in tweets_data:
            furia_mentions.append({
                "tweet_id": tweet.get("id"),
                "text": tweet.get("text"),
                "created_at": tweet.get("created_at"),
                "likes": tweet.get("public_metrics", {}).get("like_count", 0)
            })

        result = {
            "user_info": user_data.get("data", {}),
            "tweets": tweets_data,
            "furia_mentions": furia_mentions,
            "furia_sentiment_score": len(furia_mentions),
            "status": "success"
        }

        return result

    except Exception as e:
        error_message = f"Twitter data processing error: {str(e)}"
        print(error_message)
        return {"error": error_message, "status": "error"}