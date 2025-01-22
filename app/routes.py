from flask import Blueprint, request, jsonify
from app.dubbing import create_dub_from_url  # Assurez-vous que la fonction est bien définie dans app/dubbing.py

bp = Blueprint('routes', __name__)

@bp.route('/double', methods=['POST'])
def double_video():
    # Récupération des données envoyées par Laravel
    data = request.json
    
    # Vérification des données
    source_url = data.get('source_url')
    source_language = data.get('source_language')
    target_language = data.get('target_language')
    
    if not source_url or not source_language or not target_language:
        return jsonify({'error': 'Missing required data'}), 400  # Si des données manquent, retourner une erreur
    
    # Appel de la fonction de doublage
    dubbing_result = create_dub_from_url(source_url, source_language, target_language)
    
    if dubbing_result:
        return jsonify({'file_path': dubbing_result}), 200  # Retourne le chemin du fichier doublé
    else:
        return jsonify({'error': 'Error during dubbing'}), 500  # Erreur de doublage
