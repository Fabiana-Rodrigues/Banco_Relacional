from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask ('clientes')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_ClinicaVetBD'

meu_bd = SQLAlchemy(app)
class Clientes(meu_bd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = meu_bd.Column(meu_bd.Integer, primary_key=True)
    nome = meu_bd.Column(meu_bd.String(100))
    endereco = meu_bd.Column(meu_bd.String(100))
    telefone = meu_bd.Column(meu_bd.String(100))

    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }

# --------------------------------------------
# 1. GET CLIENTES
# --------------------------------------------    

@app.route('/clientes', methods = ['GET'])
def pet_vet():
    cliente_select = Clientes.query.all()
    cliente_json = [cliente.to_json()
                  for cliente in cliente_select]
    return gera_resposta(200, {} , cliente_json)

# --------------------------------------------
# CLASS PETS
# --------------------------------------------

class Pet(meu_bd.Model):
    __tablename__ = 'tb_pets'
    id_pet = meu_bd.Column(meu_bd.Integer, primary_key=True, autoincrement=True)
    nome = meu_bd.Column(meu_bd.String(255))
    tipo = meu_bd.Column(meu_bd.String(255))
    raca = meu_bd.Column(meu_bd.String(255))
    data_nascimento = meu_bd.Column(meu_bd.Date())
    id_cliente = meu_bd.Column(meu_bd.Integer, meu_bd.ForeignKey('tb_clientes.id_cliente'), nullable=False)
    idade = meu_bd.Column(meu_bd.Integer)

    def pets_to_json(self):
        return{
            "id_pet": self.id_pet,
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "data_nascimento": str(self.data_nascimento),
            "id_cliente": self.id_cliente,
            "idade": self.idade
        }

# --------------------------------------------
# 1. GET PETS
# --------------------------------------------

@app.route('/pets', methods = ['GET'])
def pet():
    pet_select = Pet.query.all()
    pet_json = [pet.pets_to_json()
                  for pet in pet_select]
    return gera_resposta(200, {} , pet_json)

    
# --------------------------------------------
# 2. POST CLIENTES
# --------------------------------------------

@app.route('/clientes', methods=['POST'])
def criar_novo_cliente():
    requisicao = request.get_json()

    try:
        cliente = Clientes(
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone'],
        )

        meu_bd.session.add(cliente)

        meu_bd.session.commit()

        return gera_resposta(201, cliente.to_json(), 'Cliente criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao cadastrar!")
    
# --------------------------------------------
# 2. POST PETS
# --------------------------------------------

@app.route('/pets', methods = ['POST'])
def inserir_pet():
    requisicao = request.get_json()

    try:
        pet_vet = Pet(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_cliente = requisicao['id_cliente'],
            idade = requisicao['idade']
        )

        meu_bd.session.add(pet_vet)

        meu_bd.session.commit()

        return gera_resposta(201, pet_vet.pets_to_json(), 'Pet criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao cadastrar!")


# --------------------------------------------
# 3. DELETE CLIENTES
# --------------------------------------------

@app.route('/clientes/<id_cliente_pam>', methods = ['DELETE'])
def deletar_cliente(id_cliente_pam):
    cliente = Clientes.query.filter_by(id_cliente = id_cliente_pam).first()

    try:
        meu_bd.session.delete(cliente)
        meu_bd.session.commit()
        return gera_resposta(200, cliente.to_json(), "Cliente deletado com sucesso!")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao deletar cliente!")


# --------------------------------------------
# 3. DELETE PETS
# --------------------------------------------

@app.route('/pets/<id_pet_pam>', methods = ['DELETE'])
def deletar_pet(id_pet_pam):
    pet_vet = Pet.query.filter_by(id_pet = id_pet_pam).first()

    try:
        meu_bd.session.delete(pet_vet)
        meu_bd.session.commit()
        return gera_resposta(200, pet_vet.pets_to_json(), "Pet deletado com sucesso!")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao deletar pet!")


# --------------------------------------------
# 4. PUT CLIENTES
# --------------------------------------------

@app.route('/clientes/<id_cliente_pam>', methods=['PUT'])
def atualizar_cliente(id_cliente_pam):
    cliente = Clientes.query.filter_by(id_cliente = id_cliente_pam).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            cliente.nome = requisicao['nome']

        if('endereco' in requisicao):
            cliente.endereco = requisicao['endereco']
        
        if('telefone' in requisicao):
            cliente.telefone = requisicao['telefone']

    
        meu_bd.session.add(cliente)
        meu_bd.session.commit()

        return gera_resposta(200, cliente.to_json(), "Cliente atualizado com sucesso!")
    
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, cliente.to_json(), "Erro ao atualizar !")

# --------------------------------------------
# 4. PUT PETS
# --------------------------------------------

@app.route('/pets/<id_pet_pam>', methods=['PUT'])
def atualizar_pet(id_pet_pam):
    pet_vet = Pet.query.filter_by(id_pet = id_pet_pam).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            pet_vet.nome = requisicao['nome']

        if('tipo' in requisicao):
            pet_vet.tipo = requisicao['tipo']
        
        if('raca' in requisicao):
            pet_vet.raca = requisicao['raca']

        if('data_nascimento' in requisicao):
            pet_vet.data_nascimento = requisicao['data_nascimento']

        if('id_cliente' in requisicao):
            pet_vet.id_cliente = requisicao['id_cliente']

        if('idade' in requisicao):
            pet_vet.idade = requisicao['idade']

    
        meu_bd.session.add(pet_vet)
        meu_bd.session.commit()

        return gera_resposta(200, pet_vet.pets_to_json(), "Pet atualizado com sucesso!")
    
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400, pet_vet.pets_to_json(), "Erro ao atualizar!")


def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body["resultado"] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype= 'application/jason')

app.run(port=5000, host='localhost', debug=True)