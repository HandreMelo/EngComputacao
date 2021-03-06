# Projeto: CRUD de Usuários + Reconhecimento Facial

#### Descrição
Projeto desenvolvido para manutenção de dados de usuários através de um site e com o uso de reconhecimento facial para buscar estas informações.

------------

#### Workflow da aplicação

##### Cadastro
	Usuário é cadastrado com dados pessoais + foto através do site.
	Os dados são enviados para o Firebase (Banco de dados não-relacional) através de uma API.
	O ID retornado do Firebase é enviado ao servidor CherryPy junto à foto.
	A foto é analisada e os descritores da foto são armazenados localmente associados ao ID do usuário.
##### Busca
	Para retormar os dados, através do site é enviado um pedido de reconhecimento para o servidor que habilita <br> a câmera que tiver sido configurada.
	Se o usuário for reconhecido então seu ID é retornado ao site através do servidor.

------------


#### Tecnologias e bibliotecas utilizadas

- **SITE:**
-- Linguagem: Vue.js, Javascript ES6 e HTML

- **SERVIDOR:**
-- Linguagem: Python
-- Bibliotecas: CherryPy, Requests

- **BANCO DE DADOS**
-- Tecnologias: Utilização do SDK do banco de dados não-relacional Firebase via CDN.
-- Linguagem: API em Javascript fornecida pelo Firebase

- **RECONHECIMENTO FACIAL:**
-- Linguagem: Python
-- Bibliotecas: Face Recognition


------------
#### Configurando o Projeto

Alguns passos são necessários para poder ter o projeto funcionado.


##### SITE



##### SERVIDOR

##### BANCO DE DADOS

##### RECONHECIMENTO FACIAL
