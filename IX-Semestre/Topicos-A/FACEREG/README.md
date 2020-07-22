# Projeto: CRUD de Usuários + Reconhecimento Facial

#### Descrição
Projeto desenvolvido para manutenção de dados de usuários através de um site e com o uso de reconhecimento facial para buscar estas informações.

------------

#### Workflow da aplicação

#####Cadastro
	Usuário é cadastrado com dados pessoais + foto através do site.
	Os dados são enviados para o Firebase (Banco de dados não-relacional).
	O ID retornado do Firebase é enviado ao servidor CherryPy junto à foto.
	A foto é analisada e os descritores da foto são armazenados localmente associados ao ID do usuário.
#####Busca
	Para retormar os dados, através do site é enviado um pedido de reconhecimento para o servidor que habilita a câmera que tiver sido configurada.
	Se o usuário for reconhecido então seu ID é retornado ao site através do servidor.

------------


#### Tecnologias e bibliotecas utilizadas

**- Site: **
--Linguagem: Vue.js, Javascript ES6 e HTML
**- Servidor:**
-- Linguagem: Python
-- Bibliotecas: CherryPy, Requests
**- Reconhecimento Facial:**
--Linguagem: Python
--Bibliotecas: Face Recognition
**-Banco de Dados**
--Tecnologia: Firebase

------------

