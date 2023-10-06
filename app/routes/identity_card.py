from flask import Blueprint

from services.ValidateCard import ValidateCard

identity_card = Blueprint('identity_card', __name__)

@identity_card.route('/', methods=['POST'])
def validate_identity_card():
    # crear imagen
    
    validate_card = ValidateCard()
    
    return validate_card.apply_validation()
