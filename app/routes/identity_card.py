from flask import Blueprint, request

from services.ValidateCard import ValidateCard

identity_card = Blueprint('identity_card', __name__)

@identity_card.route('/', methods=['POST'])
def validate_identity_card():
    data = request.get_json()

    image_front = data['image_front']
    image_reverse = data['image_reverse']

    validate_card = ValidateCard()
    
    return validate_card.apply_validation(image_front, image_reverse)
