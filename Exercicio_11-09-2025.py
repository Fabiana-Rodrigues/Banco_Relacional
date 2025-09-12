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
    
# 1. GET
@app.route('/clientes', methods = ['GET'])
def cliente_vet():
    cliente_select = Clientes.query.all()
    cliente_json = [cliente.to_json()
                  for cliente in cliente_select]
    return gera_resposta(200, {} , cliente_json)


# 2. POST
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
    

# 3. DELETE

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
    

# 4. PUT

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



def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body["resultado"] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype= 'application/jason')

app.run(port=5000, host='localhost', debug=True)

    
