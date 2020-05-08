<h1> Teste de Upload de fotos para reconhecimento facial </h1>

Para tudo dar certo:
>Instalar o CMake x64 (https://cmake.org/download/)
>pip install -r requirements.txt

> Ainda faltam vários ajustes, estes são arquivos de teste. Mas já é possível implementá-los no site. 
> Para cadastro, enviar foto e nome para o método cadastrar com os parâmetros arquivo e o ID retornado do firebase. 
> Para procurar uma pessoa, enviar uma requisição POST com a foto; se encontrar alguém, vai retornar o ID, senão, retorna que não encontrou. (ID igual ao do firebase)
> Para atualizar foto da pessoa, pasta enviar uma requisição POST /atualizar com a foto como parâmetro e o ID da pessoa.
> Para deletar, enviar uma requisição POST /deletar com o ID da pessoa.

<h2> Demo </h2>
python -m nomeServidor (aqui o arquivo é nomeServidor.py, mas não usa o .py)
abrir o localhost:8080 e pronto
