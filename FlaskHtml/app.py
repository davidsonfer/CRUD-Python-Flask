from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_aqui'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5432/cursos.udemy'


db = SQLAlchemy(app)
#Aqui, você está criando uma instância do SQLAlchemy chamada db e a associando à sua aplicação Flask app. Isso significa que você pode usar db para definir modelos de dados (classes que representam tabelas do banco de dados) e executar operações de banco de dados, como consultas e atualizações, usando a funcionalidade do SQLAlchemy.


frutas = []
registros = []

class cursos(db.Model): #Ao herdar da classe db.Model, você está dizendo ao SQLAlchemy que a sua classe Python é um modelo de dados. Isso significa que você pode usar os recursos do SQLAlchemy para interagir com o banco de dados.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    #Este é o início da definição do método __init__. Ele recebe quatro parâmetros, incluindo self que é uma referência à própria instância do objeto.
    def __init__(self, nome, descricao,ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch



@app.route('/', methods=['POST', 'GET'])
def principal():

    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))

    return render_template('index.html', frutas=frutas)


@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    # notas = {'Davidson': 5.0, "Sheilla": 7.0, "Jéssica": 9.0, "Jarbas": 1.0}
    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({'aluno': request.form.get('aluno'), 'nota': request.form.get('nota') })
    return render_template('sobre.html', registros=registros)



@app.route('/filmes/<propriedade>')
def filmes(propriedade):

    if propriedade == 'populares':
        #Aqui, você define a variável url com a URL da API do The Movie Database (TMDb) para buscar informações sobre filmes.
        url = 'https://api.themoviedb.org/3/discover/movie?sort_by=pularity.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13'
    elif propriedade == 'kids':
        url = 'https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13'
    elif propriedade == '2010':
        url = 'https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13'
    elif propriedade == 'drama':
        url = 'https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=3ddc9b92db4de6c6559569c67bd88a13'
    elif propriedade == 'tom_cruise':
        url = 'https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13'


    resposta = urllib.request.urlopen(url)
    #Esta linha utiliza urllib.request.urlopen() para abrir a URL especificada e obter a resposta da requisição.

    dados = resposta.read()
    #response.read() é usado para ler os dados da resposta HTTP obtida da URL. Neste caso, os dados provavelmente são em formato JSON.

    jsondata = json.loads(dados)
    #json.loads() é usado para analisar (parsear) os dados JSON obtidos. Isso transforma os dados JSON em um objeto Python que pode ser facilmente manipulado.

    return render_template('filmes.html', filmes=jsondata['results'])


#Retorna uma pagina Html

@app.route('/cursos')
def lista_cursos():
    return render_template('cursos.html', cursos=cursos.query.all())#Este método é usado para recuperar e ler todos os registros de uma tabela do banco de dados que correspondem a uma determinada consulta.



@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')
    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do fomulário", "erro")
        else:
            curso = cursos(nome, descricao, ch )
        #você está indicando que deseja adicionar o objeto especificado (que geralmente é uma instância de uma classe de modelo de dados) à sessão do banco de dados. Isso é frequentemente feito antes de commitar a transação para persistir as alterações no banco de dados.
            db.session.add(curso)
        #é chamado após adicionar um novo usuário à sessão. Essa chamada efetiva a adição no banco de dados. Sem o commit(), as alterações não seriam persistidas no banco, e o novo usuário não seria realmente adicionado.
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    return render_template('novo_curso.html')


@app.route('/<int:id>/atualiza_curso', methods=['GET', 'POST'])
def atualiza_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        ch = request.form['ch']
        cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})
        db.session.commit()
        return redirect(url_for('lista_cursos'))
    return render_template('atualiza_curso.html', curso=curso)


@app.route('/<int:id>/remove_curso', methods=['GET', 'POST'])
def remove_curso(id):
    pass
    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))


if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no banco de dados
        db.create_all()
    app.run(debug=True)