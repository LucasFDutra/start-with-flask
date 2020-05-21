# Instalar

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
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

Se quiser apenas testar a aplicação e seus endpoints faça o seguinte:

- Importe o arquivo `Insomnia_2020-05-21.json` para dentro do insomnia ou para o postman 
- rode no terminal o comando `python3 server.py`.

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

#### Insomnia

- endpoint: `http://localhost:5000/api`
- response: 
    ```json
    {
        "hello_response": "Hello to api route"
    }
    ``` 

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
        'hello_response': 'Hello to params route', 
        'param_response': param_value
    })

os.environ['FLASK_ENV'] = 'development'
app.run()
```

#### Insomnia

- endpoint: `http://localhost:5000/api/test_params/12`
- response: 
    ```json
    {
        "hello_response": "Hello to params route",
        "param_response": "12"
    }
    ``` 

### query params

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

#### Insomnia

- endpoint: `http://localhost:5000/api/test_query_params?param_value=12`
- response: 
    ```json
    {
        "hello_response": "Hello to query params route",
        "param_response": "12"
    }
    ``` 

### header

Assim como os query params os parâmetros vindos do header não gera a necessidade de modificar a descrição da rota. E para usá-los dentro da função basta utilizar `request.headers['nome_do_parâmetro']`.

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

#### Insomnia

- endpoint: `http://localhost:5000/api/test_header`
- header: `param_value = 12`
- response: 
    ```json
    {
        "hello_response": "Hello to header route",
        "param_response": "12"
    }
    ```

### body

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

#### Insomnia

- endpoint: `http://localhost:5000/api/test_body`
- body:
    ```json
    {
        "param_value": 12
    }
    ```
- response: 
    ```json
    {
        "hello_response": "Hello to body route",
        "param_response": 12
    }
    ``` 

# Metodos HTTP
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

# Depoy
Rode o servidor sem passar a variável de ambiente. você verá que o flask retorna a seguinte mensagem:

```sh
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
```

Isso porque o flask cria um servidor muito simples, que não é ideal para ambientes de produção. Logo precisa-se de um servidor WSGI para isso. Existem várias formas de criar um, que se econtram na própria [documentação do flask](https://flask.palletsprojects.com/en/1.1.x/deploying/). Porém o que melhor funcionou para mim foi o `Gunicorn`. Para utilizá-lo primeiro precisamos fazer uma modificações na nossa aplicação, pois se rodarmos do jeito que está, obteremos um erro. O erro ocorre por conta do comando `app.run()` que tenta iniciar o servidor flask, ou seja, estamos tentando iniciar dois servidores, o que não é uma boa ideia. Para evitar isso vou colocar o comando `app.run()` da seguinte forma

```py
if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run()
```

esse if faz com que o comando dentro dele seja executado automaticamente quando a aplicação for o objeto principal de execução. Ou seja, se mandarmos o arquivo `server.py` rodar ele é o objeto principal logo o if é executado, já com o comando do Gunicorn ele não será (logo verá isso). 

Meio complicado né? mas em resumo, quando digitamos `python3 arquivo.py` o arquivo é o objeto principal de execução, logo entrará nesse if assim que executar.

Ou seja, quando rodarmos o comando `python3 server.py` o servidor flask irá iniciar. E se quisermos que inicie um servidor gunicorn vamos rodar o comando 
```sh
$ gunicorn -w 4 server:app
```

> OBS.: como a variável de ambiente pertence ao flask eu também deixei sua definição dentro do if

vendo mais de perto esse comando temos um `-w 4`, isso é o número de workers para cada nucleo de processamento disponível. Na [documentação](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) do gunicorn ele estabelece a seguinte recomentação `w = (2 x $num_cores) + 1`.

Agora note que o seu servidor está rodando em localhost na porta 8000, isso porque não definimos o host e nem a port que o servidor executará. O comando para executar o servidor para que ele fique acessível externamente é:

```sh
$ gunicorn -w 4 --bind 0.0.0.0:8000 server:app
```

## Outra opção

Se quiser executar o servidor por dentro da aplicação assim como o flask, para que possamos executar o comando `python3 server.py` e o gunicorn irá criar o servidor, basta colocar o seguite código na aplicação

```py
from flask import Flask, request, jsonify
from gunicorn.app.base import BaseApplication
import os

app = Flask(__name__)

# Rotas....

class StartServer(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
     options = {
        'bind': '%s:%s' % ('0.0.0.0', '8000'),
        'workers': 4,
    }
    StartServer(app, options).run()
```

Só que com isso acabamos obtendo apenas um jeito de startar nossa aplicação, sem a opção de usar o flask e temos que definir a porta para localhost dentro do código caso precisamos.

Não que não possamos deixar sempre assim, afinal o gunicorn gera um ambiente que atualiza dinamicamente assim como o flask, mas me parece desperdicio. Então vamos fazer uma lógica que ao passarmos uma flag `--prod` no comando `python3 server.py` indicando que queremos iniciar com o gunicorn, e se não passarmos nada ele inicará com o flask.

> OBS.: Userei a lib `multiprocessing` que consegue ver quantos nucleos a máquina tem e com isso irei fazer o calculo do número de workers dinamicamente

```py
from flask import Flask, request, jsonify
from gunicorn.app.base import BaseApplication
import os
import sys
import multiprocessing

app = Flask(__name__)

# Rotas...

# Classe...

if __name__ == '__main__':
    if('--prod' in sys.argv):
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '8000'),
            'workers': (multiprocessing.cpu_count() * 2) + 1,
        }
        StartServer(app, options).run()
    else:
        os.environ['FLASK_ENV'] = "development"
        app.run()
```

com a lib `sys` nos conseguimos pegar argumentos passados na execução da aplicação através do terminal. Isso possibilita dinamismo ao rodar a aplicação, podemos por exemplo definir bancos de dados diferentes caso estejamos rodando em ambiente de desenvolvimente ou produção.

- Para rodar em dev:
    ```sh
    $ python3 server.py
    ```

- Para rodar em prod:
    ```sh
    $ python3 server.py --prod
    ```