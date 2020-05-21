# Instalar

- [python](https://www.python.org/)
- [flask](https://flask.palletsprojects.com/en/1.1.x/)
```sh
$ pip3 install Falsk
```
- [Gunicorn](https://gunicorn.org/)
```sh
$ pip3 install gunicorn
```

O projeto será simples, então terá apenas um arquivo chamado `server.py`, que irá criar o servidor e cinco rotas. Sendo que uma não receberá nenhum parâmetro e as outras receberão cada uma um parâmetro em lugares diferentes, no `header`, `body`, `params` e `query params`.

Fare com que as rotas iniciem por `/api`, mas poderia ser qualquer coisa, inclusive somente `/`.

> OBS.: Quando uma parâmetro chega na rota ele é sempre uma string. Então fique atento a tipagem do que está recebendo. Mesmo com python não sendo tipado o tipo importa em certas ocasiões.

Para testar as requeste usarei o [Insomnia](https://insomnia.rest/) mas você também pode usar o [Postman](https://www.postman.com/)

# A aplicação
## Como criar uma aplicação flask

Importe o flask e atribua o mesmo para uma variável. Também é importante importar de dentro do flask a classe `request` para ter acesso aos parâmetros que serão passados, e também o `jsonify` para passar as responses em json.

```py
from flask import Flask, request, jsonify

app = Flask(__name__)

app.run()
```

o comando `app.run()` fará com que assim que digitarmos no terminal o comando `$ python3 server.py` o flask inicialize um servidor localhost na porta 5000. 

com apenas esse código o servidor não reinicia automaticamente com nossas mudanças, sendo necessário reinicá-lo sempre que modificarmos algo. 

Para resolver isso basta informar ao flask que estamos em um ambiente de desenvolvimente, para isso basta adicionar uma variável de ambiente em seu sistema operacional para informá-lo disso, você pode fazer isso de duas formas (eu usarei a segunda).

- 1) abra o seu terminal e digite:
```sh
# no linux
$ export FLASK_ENV=development

# no windows
$ set FLASK_ENV=development
```

- 2) no próprio código do python, através da lib `os`.
```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

os.environ['FLASK_ENV'] = 'development'
app.run()
```

> OBS.: o comando deve ser dado antes de `app.run()` para que assim o servidor saiba onde iniciar.

com isso você já tem o reload automatico da aplicação.

## Como criar uma rota

Com a variável `app` defina uma rota, passando como parâmetro da rota o caminho para atingi-la. A função logo abaixo dessa rota será aquela que executará quando a rota for atingida.

```py
from flask import Flask, request, jsonify
import os

@app.route('/api')
def api():
    return jsonify({'hello_response': 'Hello to api route'})

os.environ['FLASK_ENV'] = 'development'
app.run()
```

Ou seja pelo exemplo acima, quando chamarmos a aplicação na rota `/api` ela irá retornar um json com a mensagem `Hello to api route`.

> OBS.: O nome da função e da rota não precisa ser igual.

## Como passar parâmetros

### Params

Se quiser passar parâmetros via url é bem simples, basta definir o nome dos parâmetros entre `<>` na rota e pronto. Para usá-los passe-os como atributos da função da rota.

```py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/test_params/<param_value>')
def testParams(param_value):
    return jsonify({
        'hello_response': 'Hello to api route', 
        'param_response': param_value
    })

os.environ['FLASK_ENV'] = 'development'
app.run()
```

## query params

Se quiser receber um parâmetro dessa forma, basta usar o `request.args.get('nome_do_parâmetro')` dentro da função da rota, a rota em sí não precisa receber nenhum parâmetro

```py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/test_query_params')
def testQueryPamans():
    param_value = request.args.get('param_value')
    return jsonify({
        'hello_response': 'Hello to query params route',
        'param_response': param_value
    })

os.environ['FLASK_ENV'] = 'development'
app.run()
```

## header

Assim como os query params os parâmetros vindos do header não gera a necessidade de modificar a descrição da rota. E para usá-los dentro da função basta utilizar `request.headers['nome_do_parâmetro'].

```py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/test_header')
def testHeader():
    param_value = request.headers['param_value']
    return jsonify({
        'hello_response': 'Hello to header route',
        'param_response': param_value
    })

os.environ['FLASK_ENV'] = 'development'
app.run()
```

## body

Para coletar os valores do body, utilize `request.body[nome_do_parametro]`.

```py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/test_body')
def testBody():
    param_value = request.json['param_value']
    return jsonify({
        'hello_response': 'Hello to body route',
        'param_response': param_value
    })

os.environ['FLASK_ENV'] = 'development'
app.run()
```

# Metodos http
Por padrão o método utilizado é o `GET`, mas isso pode ser especificado na rota.

```py
@app.route('/api', methods='POST')
```

Caso a mesma rota possa acietar multiplos métodos você pode usar a seguinte sintex (exemplo vindo da documentação do flask)

```py
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```

veja que o método `request.method` carrega a informação de qual verbo http foi utilizado.