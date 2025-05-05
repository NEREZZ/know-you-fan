from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from werkzeug.utils import secure_filename
from database import save_user_data, get_db_connection
from ai_processing import analisaTweets, analisaSentimento
from buscaDadosTwitter import dadosUsuario

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Em produção, use uma chave segura e não a inclua no código

# Configurações
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

analiseIa = {'total_score': 0, 'tweet_analysis': [], 'recommendations': []}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def show_form():
    return render_template('form.html')

def generate_recommendations(user_data):
    recommendations = []

    try:

        total_score= analiseIa.get('total_score',0)
        # Recomendações baseadas em jogos
        games = user_data.get('interests', {}).get('games', [])
        if isinstance(games, list):
            if 'CSGO' in games:
                recommendations.append("Sugerir conteudos de CS:GO")
            if 'LOL' in games:
                recommendations.append("Sugerir conteúdo de League of Legends")
            if 'VALORANT' in games:
                recommendations.append("Sugerir conteudos de VALORANT")
            if 'Apex Legends' in games:
                recommendations.append("Sugerir conteudos de Apex Legends")
            if 'Rainbow Six: Siege' in games:
                recommendations.append("Sugerir conteudos de Rainbow Six: Siege")
            if 'Kings League' in games:
                recommendations.append("Sugerir conteudos de Kings League")
            if 'Rocket League' in games:
                recommendations.append("Sugerir conteudos de Rocket League")

        # Recomendações baseadas em sentimentos da análise global
        if analisaSentimento:  # Usa a variável global
            positivos = sum(1 for tweet in analisaSentimento if tweet['sentimento'] == 'POSITIVO')
            if positivos > 0:
                recommendations.append("Cliente satisfeito com compras - oferecer novidades")
            else:
                recommendations.append("Cliente menos satisfeito - oferecer desconto especial")
            if total_score > 70:
                recommendations.append("Fã altamente engajado - convidar para programa de embaixadores")
            elif total_score < 30:
                recommendations.append("Fã pouco engajado - oferecer conteúdo exclusivo para aumentar engajamento")
        return {'recommendations': recommendations}
    except Exception as e:
        print(f"Erro ao gerar recomendações: {e}")
        return {'recommendations': ["Erro ao gerar recomendações personalizadas"]}

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Dados do formulário
        user_data = {
            'personal_info': {
                'name': request.form.get('name', ''),
                'cpf': request.form.get('cpf', ''),
                'email': request.form.get('email', ''),
                'birthdate': request.form.get('birthdate', '')
            },
            'address': {
                'cep': request.form.get('cep', ''),
                'address': request.form.get('address', ''),
                'city': request.form.get('city', ''),
                'state': request.form.get('state', '')
            },
            'interests': {
                'games': request.form.getlist('games'),
                'favorite_team': request.form.get('favorite_team', ''),
                'nick_name': request.form.get('nick_name', ''),
                'events_attended': request.form.get('events_attended', ''),
                'merch_purchases': request.form.get('merch_purchases', '')
            },
            'social_media': {
                'twitter_profile': request.form.get('twitter_profile', ''),
                'instagram_profile': request.form.get('instagram_profile', ''),
                'esports_profiles': request.form.get('esports_profiles', '')
            },
            'documents': {}
        }

        # Processar upload de documentos
        if 'id_document' in request.files:
            file = request.files['id_document']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"id_{user_data['personal_info']['cpf']}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user_data['documents']['id_document'] = filename

        if 'proof_of_address' in request.files:
            file = request.files['proof_of_address']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"address_{user_data['personal_info']['cpf']}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user_data['documents']['proof_of_address'] = filename

        # Buscar dados do Twitter se o perfil for fornecido
        twitter_data = None
        perfil_twitter = user_data['social_media']['twitter_profile']
        if perfil_twitter and perfil_twitter.strip():
            # Remove @ do início se existir
            if perfil_twitter.startswith('@'):
                perfil_twitter = perfil_twitter[1:]

            #twitter_data = dadosUsuario(perfil_twitter)
            twitter_data={'user_info': {'description': 'founder @FURIA 🇧🇷', 'username': 'jaimepadua', 'id': '34398147',
                                                      'profile_image_url': 'https://pbs.twimg.com/profile_images/1747293705533288454/8RWY44Hs_normal.jpg', 'name': 'FURIA jaimepadua', 'created_at': '2009-04-22T21:06:20.000Z',
                                                      'public_metrics': {'followers_count': 47214, 'following_count': 1876, 'tweet_count': 20856, 'listed_count': 112, 'like_count': 54723, 'media_count': 727}}, 'tweets': [{'id': '1918101210390761757',
                                                                                    'text': 'RT @FURIA: VITÓRIA da #FURIAApex no game 6! 🔥\n\nVAMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n\n@FURIA_USA @pOkizGames https…',
                                                    'created_at': '2025-05-02T00:32:19.000Z', 'edit_history_tweet_ids': ['1918101210390761757'], 'public_metrics': {'retweet_count': 11, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 1}}, {'id': '1918073769727328265',
                                                'text': '@dudolagordola @FURIA seria legal, mas o calendário não colabora com a reduzida quantidade de jogos e as mudanças agora também, mas vamos melhorar nisso tb 👊🏼', 'created_at': '2025-05-01T22:43:17.000Z', 'edit_history_tweet_ids': ['1918073769727328265'], 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 18, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 758}}, {'id': '1918066788606132316', 'text': '✅ Finais do Mundial de PUBG - amanhã\n✅ começo excelente no Mundial de APEX - hoje\n\na @FURIA está competindo em todo lugar \ne onde não tá legal, vai ficar! \n\npodem confiar! 🇧🇷', 'created_at': '2025-05-01T22:15:33.000Z', 'edit_history_tweet_ids': ['1918066788606132316'], 'public_metrics': {'retweet_count': 9, 'reply_count': 41, 'like_count': 423, 'quote_count': 4, 'bookmark_count': 4, 'impression_count': 22939}}, {'id': '1918063386757132363', 'text': 'agora temos nosso @tvoy_molodoy sem ping 100 e com todas as condições de mostrar seu potencial... \n\né o Rock Lee sem os pesos! seguraaaaa!! https://t.co/MOf959znVH https://t.co/uZ7IAWR3Ge', 'created_at': '2025-05-01T22:02:01.000Z', 'edit_history_tweet_ids': ['1918063386757132363'], 'public_metrics': {'retweet_count': 0, 'reply_count': 7, 'like_count': 199, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 7023}}, {'id': '1918063119793893744', 'text': 'RT @FURIA: Ол келді! Ele chegou! 🇧🇷🇰🇿\n\n@tvoy_molodoy de visto aprovado e junto da #FURIACS! https://t.co/pavzQprpNv', 'created_at': '2025-05-01T22:00:58.000Z', 'edit_history_tweet_ids': ['1918063119793893744'], 'public_metrics': {'retweet_count': 81, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 0}}, {'id': '1918027235207901516', 'text': '@FURIA present ✅', 'created_at': '2025-05-01T19:38:22.000Z', 'edit_history_tweet_ids': ['1918027235207901516'], 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 16, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 1034}}, {'id': '1917668775878336523', 'text': '@andradebarbarCS @FURIA estamos num período de reavaliação, com planos de internacionalização neste sentido também - quando tiver mais concreto comunicaremos a respeito 👊', 'created_at': '2025-04-30T19:53:59.000Z', 'edit_history_tweet_ids': ['1917668775878336523'], 'public_metrics': {'retweet_count': 0, 'reply_count': 2, 'like_count': 39, 'quote_count': 1, 'bookmark_count': 0, 'impression_count': 2641}}, {'id': '1917645995866833015', 'text': '"aahhh jaime, se você comprar o fulano eu compro a skin da @FURIA!" \n\ntá achando que os times vão aceitar cartão de crédito, irmão? ajuda ai po 🤣 https://t.co/LUdO36Umyw', 'created_at': '2025-04-30T18:23:28.000Z', 'edit_history_tweet_ids': ['1917645995866833015'], 'public_metrics': {'retweet_count': 7, 'reply_count': 82, 'like_count': 786, 'quote_count': 7, 'bookmark_count': 10, 'impression_count': 59098}}, {'id': '1917617321041916039', 'text': "RT @FURIA: molodoy paved the way for KZ...\nNow it's @krizzencsgo's time to join #FURIACS! 🇰🇿🐾\n\nDamos as boas-vindas ao KrizzeN como novo As…", 'created_at': '2025-04-30T16:29:31.000Z', 'edit_history_tweet_ids': ['1917617321041916039'], 'public_metrics': {'retweet_count': 25, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 0}}, {'id': '1917616973044658190',
                                                                                                                                                                                                                                                                    'text': 'RT @FURIA: O carro bicho da #FURIAPUBG ta chegando pra Final do mundial! ESTAMOS CLASSIFICADOS! 🇧🇷\n\nNos vemos nas manhãs de sexta a domingo…', 'created_at': '2025-04-30T16:28:08.000Z', 'edit_history_tweet_ids': ['1917616973044658190'], 'public_metrics': {'retweet_count': 11, 'reply_count': 0, 'like_count': 0, 'quote_count': 0, 'bookmark_count': 0, 'impression_count': 0}}], 'furia_mentions': [{'tweet_id': '1918101210390761757', 'text': 'RT @FURIA: VITÓRIA da #FURIAApex no game 6! 🔥\n\nVAMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n\n@FURIA_USA @pOkizGames https…', 'created_at': '2025-05-02T00:32:19.000Z', 'likes': 0}, {'tweet_id': '1918073769727328265', 'text': '@dudolagordola @FURIA seria legal, mas o calendário não colabora com a reduzida quantidade de jogos e as mudanças agora também, mas vamos melhorar nisso tb 👊🏼', 'created_at': '2025-05-01T22:43:17.000Z', 'likes': 18}, {'tweet_id': '1918066788606132316', 'text': '✅ Finais do Mundial de PUBG - amanhã\n✅ começo excelente no Mundial de APEX - hoje\n\na @FURIA está competindo em todo lugar \ne onde não tá legal, vai ficar! \n\npodem confiar! 🇧🇷', 'created_at': '2025-05-01T22:15:33.000Z', 'likes': 423}, {'tweet_id': '1918063386757132363', 'text': 'agora temos nosso @tvoy_molodoy sem ping 100 e com todas as condições de mostrar seu potencial... \n\né o Rock Lee sem os pesos! seguraaaaa!! https://t.co/MOf959znVH https://t.co/uZ7IAWR3Ge', 'created_at': '2025-05-01T22:02:01.000Z', 'likes': 199}, {'tweet_id': '1918063119793893744', 'text': 'RT @FURIA: Ол келді! Ele chegou! 🇧🇷🇰🇿\n\n@tvoy_molodoy de visto aprovado e junto da #FURIACS! https://t.co/pavzQprpNv', 'created_at': '2025-05-01T22:00:58.000Z', 'likes': 0}, {'tweet_id': '1918027235207901516', 'text': '@FURIA present ✅', 'created_at': '2025-05-01T19:38:22.000Z', 'likes': 16}, {'tweet_id': '1917668775878336523', 'text': '@andradebarbarCS @FURIA estamos num período de reavaliação, com planos de internacionalização neste sentido também - quando tiver mais concreto comunicaremos a respeito 👊', 'created_at': '2025-04-30T19:53:59.000Z', 'likes': 39}, {'tweet_id': '1917645995866833015', 'text': '"aahhh jaime, se você comprar o fulano eu compro a skin da @FURIA!" \n\ntá achando que os times vão aceitar cartão de crédito, irmão? ajuda ai po 🤣 https://t.co/LUdO36Umyw', 'created_at': '2025-04-30T18:23:28.000Z', 'likes': 786}, {'tweet_id': '1917617321041916039', 'text': "RT @FURIA: molodoy paved the way for KZ...\nNow it's @krizzencsgo's time to join #FURIACS! 🇰🇿🐾\n\nDamos as boas-vindas ao KrizzeN como novo As…", 'created_at': '2025-04-30T16:29:31.000Z', 'likes': 0}, {'tweet_id': '1917616973044658190', 'text': 'RT @FURIA: O carro bicho da #FURIAPUBG ta chegando pra Final do mundial! ESTAMOS CLASSIFICADOS! 🇧🇷\n\nNos vemos nas manhãs de sexta a domingo…', 'created_at': '2025-04-30T16:28:08.000Z', 'likes': 0}], 'furia_sentiment_score': 10}

        else:
            print("Nenhum perfil de Twitter fornecido")


        # Salvar no banco de dados
        user_id = save_user_data(user_data)


        # Processar com IA
        global analiseIa
        resultado = generate_recommendations(user_data)
        analiseIa = {'total_score': 0, 'tweet_analysis':twitter_data, 'recommendations': resultado.get('recommendations')}

        # Armazenar ID do usuário na sessão para uso posterior
        session['last_user_id'] = user_id

        flash('Formulário enviado com sucesso!', 'success')
        return redirect(url_for('thank_you'))

    except Exception as e:
        app.logger.error(f'Erro ao processar o formulário: {str(e)}')
        flash(f'Erro ao processar o formulário: {str(e)}', 'error')
        return redirect(url_for('show_form'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/dashboard-view')
def dashboard_view():
    return render_template('dashboard.html')


@app.route('/dashboard')
def dashboard_data():
    try:
        user_id = session.get('last_user_id')
        conn = get_db_connection()

        if user_id:
            query = 'SELECT * FROM users WHERE id = ?'
            user = conn.execute(query, (user_id,)).fetchone()
        else:
            user = conn.execute('SELECT * FROM users ORDER BY registration_date DESC LIMIT 1').fetchone()

        conn.close()

        if user:
            # Buscar dados do Twitter
            twitter_profile = user['twitter_profile']
            if twitter_profile:
                # Remove @ se existir
                twitter_profile = twitter_profile.strip('@') if twitter_profile.startswith('@') else twitter_profile
                twitter_data = dadosUsuario(twitter_profile)

                if twitter_data and 'error' not in twitter_data:
                    # Analisar tweets
                    analysis_result = analisaTweets(twitter_data)

                    # Gerar recomendações com os dados do usuário
                    user_data = {
                        'interests': {
                            'games': eval(user['games']) if user['games'] else []  # Converte string para lista
                        }
                    }
                    recommendations = generate_recommendations(user_data)

                    # Retornar todos os dados necessários
                    return jsonify({
                        'name': user['name'],
                        'email': user['email'],
                        'total_score': analysis_result['total_score'],
                        'tweet_analysis': analysis_result['tweet_analysis'],
                        'recommendations': recommendations.get('recommendations', [])
                    })


            # Se não houver perfil do Twitter ou análise falhar, retornar dados básicos
            return jsonify({
                'name': user['name'],
                'email': user['email'],
                'total_score': 0,
                'tweet_analysis': [],
                'recommendations': []
            })


        return jsonify({"error": "Nenhum usuário encontrado"}), 404

    except Exception as e:
        app.logger.error(f'Erro ao buscar dados do dashboard: {str(e)}')
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/chatbot/send', methods=['POST'])
def chatbot_send():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'Mensagem não fornecida'}), 400
            
        # Usar a função bot do chat_bot.py para gerar a resposta
        from chat_bot import bot
        bot_response = bot(user_message)
        
        if not bot_response:
            bot_response = "Desculpe, não consegui processar sua mensagem."
            
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"Erro no chatbot: {str(e)}")  # Para debug
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    flash('Arquivo muito grande. O tamanho máximo permitido é 16MB.', 'error')
    return redirect(url_for('show_form'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)