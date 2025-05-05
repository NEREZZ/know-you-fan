import requests
import time
import json
import os
from datetime import datetime


def dadosUsuario(usuario):
    # Verifica se o nome de usuário é válido
    if not usuario or usuario.strip() == "":
        print("Nome de usuário vazio ou inválido")
        return None

    # Boa prática: Obter token de variáveis de ambiente
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN",
                             "")
    headers = {"Authorization": f"Bearer {bearer_token}"}

    try:
        # Primeiro, verifica a existência do usuário e obtém informações do perfil com lógica de repetição
        user_url = f"https://api.twitter.com/2/users/by/username/{usuario}?user.fields=description,public_metrics,profile_image_url,created_at"

        user_data = None
        max_retries = 3  # Número máximo de tentativas
        retry_delay = 2  # Começa com 2 segundos de espera

        # Loop de tentativas para obter dados do usuário
        for attempt in range(max_retries):
            user_response = requests.get(user_url, headers=headers)

            if user_response.status_code == 200:
                user_data = user_response.json()
                break
            elif user_response.status_code == 429:  # Rate limit excedido
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)  # Aumento exponencial do tempo de espera
                    print(f"Rate limit atingido. Aguardando {wait_time} segundos antes da tentativa {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {"error": "Limite de taxa da API do Twitter excedido após várias tentativas"}
            else:
                error_message = f"Erro ao buscar usuário: {user_response.status_code} {user_response.text}"
                print(error_message)
                return {"error": error_message}

        # Verifica se os dados do usuário foram obtidos com sucesso
        if not user_data or 'data' not in user_data:
            return {"error": "Usuário não encontrado ou dados indisponíveis"}

        # Agora busca por tweets com "fúria" com lógica de repetição similar
        tweets_data = []
        search_url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{usuario} fúria&max_results=10&tweet.fields=created_at,public_metrics"

        # Loop de tentativas para buscar tweets
        for attempt in range(max_retries):
            tweets_response = requests.get(search_url, headers=headers)

            if tweets_response.status_code == 200:
                tweets_data = tweets_response.json().get('data', [])
                break
            elif tweets_response.status_code == 429:  # Rate limit excedido
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"Rate limit atingido na busca de tweets. Aguardando {wait_time} segundos...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Limite de taxa excedido para busca de tweets após várias tentativas")
                    break  # Continua sem os tweets ao invés de falhar completamente
            else:
                print(f"Erro ao buscar tweets: {tweets_response.status_code}")
                break

        # Prepara os resultados das menções à "fúria"
        furia_mentions = []
        for tweet in tweets_data:
            furia_mentions.append({
                "tweet_id": tweet.get("id"),
                "text": tweet.get("text"),
                "created_at": tweet.get("created_at"),
                "likes": tweet.get("public_metrics", {}).get("like_count", 0)
            })

        # Estrutura o resultado final
        result = {
            "user_info": user_data.get("data", {}),
            "tweets": tweets_data,
            "furia_mentions": furia_mentions,
            "furia_sentiment_score": len(furia_mentions),  # Score baseado no número de menções
            "status": "success"
        }

        return result

    except Exception as e:
        error_message = f"Erro no processamento de dados do Twitter: {str(e)}"
        print(error_message)
        return {"error": error_message, "status": "error"}
