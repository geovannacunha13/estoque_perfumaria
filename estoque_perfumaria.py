class Cliente:
    def __init__(self, id_cliente, cpf, celular, nome):
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.celular = celular
        self.nome = nome

class Pedido:
    def __init__(self, id_pedido, moto_boy, endereco):
        self.id_pedido = id_pedido
        self.moto_boy = moto_boy
        self.endereco = endereco

class Perfume:
    def __init__(self, id_perfume, nome_perfume, quantidade, preco):
        self.id_perfume = id_perfume
        self.nome_perfume = nome_perfume
        self.quantidade = quantidade
        self.preco = preco

class Pagamento:
    def __init__(self, id_pagamento, tipo_pagamento):
        self.id_pagamento = id_pagamento
        self.tipo_pagamento = tipo_pagamento
