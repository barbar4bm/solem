from flask import jsonify

class ValidateCard():
    def apply_validation(self):
        # normalizar
        self.normzalize_card()
        # ecualizar
        self.equalize_card()

        return jsonify({'success': True})
    
    def normzalize_card(self):
        pass

    def equalize_card(self):
        pass
