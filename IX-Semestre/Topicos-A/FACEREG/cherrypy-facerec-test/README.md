<h1> Teste de Upload de fotos para reconhecimento facial </h1>

Para tudo dar certo:

Python == 3.7.4 \n
pip install face_recognition==1.3.0
pip install face_recognition_models==0.3.0 (acho que já vem com o face_recognition)
pip install dlib==19.19.0
pip install scikit-learn==0.22.2.post1
pip install cherrypy

> Ainda faltam vários ajustes, estes são arquivos de teste. Mas já é possível implementá-los no site. 
> Para cadastro, enviar foto e nome para o método cadastrar com os parâmetros arquivo, stringNome. 
> Para testar se a pessoa da foto está cadastrada, usar o método procurar com o parâmetro arquivo,
    onde retorna o nome da pessoa (não id ainda) ou que não encontrou nada.

<h2> Demo </h2>
python -m nomeServidor (aqui o arquivo é nomeServidor.py, mas não usa o .py)
abrir o localhost:8080 e pronto
