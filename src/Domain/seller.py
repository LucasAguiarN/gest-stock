class SellerDomain():
    def __init__(self, id, name, cnpj, email, password, cellphone):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.password = password
        self.cellphone = cellphone

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "password": self.password,
            "cellphone": self.cellphone
        }