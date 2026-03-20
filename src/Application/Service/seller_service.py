from src.Infrastructure.http.whats_app import WhatsAppService
import random
from src.Domain.seller import SellerDomain
from src.Infrastructure.Model.seller import Seller
from src.config.data_base import db
import bcrypt

class SellerService:

    @staticmethod
    def create_seller(name, cnpj, email, password, cellphone):

        #criptogradar senha    
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #gerar código de ativação
        activation_code = str(random.randint(1000,9999))

        seller = Seller(name=name, cnpj=cnpj, email=email, password=hashed_password.decode('utf-8'), cellphone=cellphone, status='inativo', activation_code=activation_code)

        db.session.add(seller)
        db.session.commit()

        try:
            whatsapp = WhatsAppService()
            mensagem = f"Seu código de ativação é: {activation_code}"
            whatsapp.send_message(cellphone, mensagem)
        
        except Exception as e:
            print("Erro ao enviar WhatsApp:", e)


        return SellerDomain(seller.id, seller.name, seller.cnpj, seller.email, seller.password, seller.cellphone, seller.status)


    @staticmethod
    def authenticate_seller(email, password):

        seller = Seller.query.filter_by(email=email).first()

        if not seller:
            return None

        if not bcrypt.checkpw(password.encode('utf-8'), seller.password.encode('utf-8')):
            return None

        return seller


    @staticmethod
    def active_seller():
        pass