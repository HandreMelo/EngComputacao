import React from 'react';
import { Jumbotron, Container } from 'reactstrap';

const ArticleAddUser = (props) => {
  return (
    <div>
      <Jumbotron fluid>
        <Container fluid>
          <h1 className="display-3">Cadastrar usuário</h1>
          <p className="lead">Conteúdo do artigo. This is a modified jumbotron that occupies the entire horizontal space of its parent.</p>
        </Container>
      </Jumbotron>
    </div>
  );
};

export default ArticleAddUser;