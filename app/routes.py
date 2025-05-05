#routes
from flask import Blueprint, request, jsonify,render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import database
from ai_processing import analyze_user_data  # Importe sua função
import json

auth_bp= Blueprint('auth',__name__)


# rota protegida(mostra informaçoes do usuario atual)
@auth_bp.route('/dashboard')

def dashboard(): #apos o user logar irá
    user_data = {
        "personal_info": {"name": current_user.id},
        "interests": {
            "games": [current_user.games, 'nao deu certo'],
            "events_attended": [current_user.events, 'nao deu certo'],
            "merch_purchases": [current_user.merch, 'nao deu certo'],
        },
        "social_media": {
            "twitter_profile": [current_user.twitter_profile, 'nao deu certo'],
            "instagram_profile": "@fan_insta",
            "esports_profiles": "esports.gg/fan"
        }
    }

    insights = analyze_user_data(user_data)
    return jsonify({
        "message": f"Bem vindo, {current_user.id}!",
        "user": current_user.id,
        "insights": insights
    }), 200


@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "Logout feito com sucesso"}), 200
