from flask import request, jsonify, make_response
from src.Application.Service.seller_service import SellerService

class SellerController:
    @staticmethod
    def register_seller():
        data = request.get_json()
        name = data.get('nome')
        cnpj = data.get('cnpj')
        email = data.get('email')
        password = data.get('senha')
        cellphone = data.get('celular')

        if not name or not cnpj or not email or not password or not cellphone:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        seller = SellerService.create_seller(name, cnpj, email, password, cellphone)
        return make_response(jsonify({
            "mensagem": "Seller salvo com sucesso",
            "Seller": seller.to_dict()
        }), 200)