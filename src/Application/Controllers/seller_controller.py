from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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

    @staticmethod
    def activate_seller():
        data = request.get_json()
        cellphone = data.get('celular')
        code = data.get('codigo')

        if not cellphone or not code:
            return make_response(jsonify({"erro": "celular e/ou código são obrigatórios"}), 400)

        activated_seller = SellerService.active_seller(cellphone, code)
        if activated_seller:
            return make_response(jsonify({
                "mensagem": "conta ativada com sucesso!",
                "seller": activated_seller.to_dict()
            }), 200)
        return make_response(jsonify({"erro": "código inválido ou celular não encontrado"}), 400)

    @staticmethod
    def login_seller():
        data = request.get_json()

        email = data.get("email")
        password = data.get("senha")

        if not email or not password:
            return make_response(jsonify({"erro": "Email e senha são obrigatórios"}), 400)

        seller = SellerService.authenticate_seller(email, password)

        if not seller:
            return make_response(jsonify({"erro": "Email ou senha inválidos"}), 401)

        if seller.status == "inativo":
            return make_response(jsonify({"erro": "Seller ainda não ativado"}), 403)

        token = create_access_token(identity=seller.id)

        return make_response(jsonify({
            "mensagem": "Login realizado com sucesso",
            "token": token,
            "seller": seller.to_dict()
        }), 200)

    @staticmethod
    @jwt_required()
    def update_seller():
        current_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return make_response(jsonify({"erro": "Dados para atualização não fornecidos"}), 400)

        update_seller = SellerService.update_seller(current_id, data)
        if not update_seller:
            return make_response(jsonify({"erro": "não foi possível atualizar os dados"}), 400)
        return make_response(jsonify({
            "mensagem": "perfil atualizado!",
            "seller": update_seller.to_dict()
        }), 200)