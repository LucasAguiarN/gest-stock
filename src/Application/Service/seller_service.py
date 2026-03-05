from src.Domain.seller import SellerDomain
from src.Infrastructure.Model.seller import Seller
from src.config.data_base import db 

class SellerService:
    @staticmethod
    def create_seller(name, cnpj, email, password, cellphone):        
        seller = Seller(name=name, cnpj=cnpj, email=email, password=password, cellphone=cellphone)        
        db.session.add(seller)
        db.session.commit()       
        return SellerDomain(seller.id, seller.name, seller.cnpj, seller.email, seller.password, seller.cellphone)

    @staticmethod
    def active_seller():
        pass