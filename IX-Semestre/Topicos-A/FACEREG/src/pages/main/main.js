import React, {Component} from 'react';
import './styles.css';
import { Link } from 'react-router-dom';

export default class Main extends Component {

    render() {
        return (
            <div className="options-list">
                <article >
                    <strong>Cadastrar</strong>
                    <p>cadastrar pessoas</p>
                    <Link to="/register">Acessar</Link>
                </article>
                <article >
                    <strong>Listar</strong>
                    <p>Listar pessoas</p>
                    <a href="">Acessar</a>
                </article>
                <article >
                    <strong>Editar</strong>
                    <p>Editar uma pessoa específica</p>
                    <a href="">Acessar</a>
                </article>
                <article >
                    <strong>Excluir</strong>
                    <p>Exluir pessoas</p>
                    <a href="">Acessar</a>
                </article>
                <article >
                    <strong>Comparar</strong>
                    <p>Comparação de um foto com a foto da pessoa cadastrada</p>
                    <a href="">Acessar</a>
                </article>
            
            </div>
        );
    }
}