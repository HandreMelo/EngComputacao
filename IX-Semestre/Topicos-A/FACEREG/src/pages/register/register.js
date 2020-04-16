import React, { Component } from 'react';

export default class Register extends Component {

    state = {
        valueName: '',
        valueEmail: '',
        valueTelephone: '',
        valueAddress: '',
        valueNameDog: '',
        valueFaceDog: ''
    }




    save = () => {
        //aqui requisição
    }

    render() {

        return (
            <div>
                <form id="infoRegister">
                    <h6>Seu nome:</h6>
                    <input type="text" value={this.setState.valueName} id="name" />
                    <h6>Email:</h6>
                    <input type="text" value={this.setState.valueEmail} id="email" />
                    <h6>Telefone:</h6>
                    <input type="text" value={this.setState.valueTelephone} id="telephone" />
                    <h6>Endereço:</h6>
                    <input type="text" value={this.setState.valueAddress} id="address" />
                    <h6>Nome do cachorro:</h6>
                    <input type="text" value={this.setState.valueNameDog} id="nameDog" />
                    <h6>Foto do cachorro:</h6>
                    <input type="file" value={this.setState.valueFaceDog} id="faceDog" />
                </form>

                <button onClick={this.save} id="register">Add</button>
            </div>
        );

    }
}