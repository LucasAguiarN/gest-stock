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

        if seller.status != 'ativo':
            return 'inativo'

        return seller


    @staticmethod
    def active_seller(cellphone, code):
        seller = Seller.query.filter_by(cellphone=cellphone, status="inativo").order_by(Seller.id.desc()).first()

        if not seller:
            print(f"Erro: Seller com celular {cellphone} não encontrado.")
            return None
        if str(seller.activation_code) == str(code):
            seller.status = 'ativo'
            seller.activation_code = None            
            db.session.commit()    

            return SellerDomain(
                id=seller.id,
                name=seller.name,
                cnpj=seller.cnpj,
                email=seller.email,
                password=seller.password,
                cellphone=seller.cellphone,
                status=seller.status   
            )

        print(f"Erro: Código {code} não confere com o salvo ({seller.activation_code})")
        return None

    @staticmethod
    def update_seller(seller_id, data):
        seller = Seller.query.get(seller_id)

        if not seller:
            return None

        seller.name = data.get('nome', seller.name)
        seller.email = data.get('email', seller.email)
        seller.cellphone = data.get('celular', seller.cellphone)
        db.session.commit()

        return SellerDomain(
            seller.id, 
            seller.name, 
            seller.cnpj, 
            seller.email, 
            seller.password, 
            seller.cellphone, 
            seller.status
        )