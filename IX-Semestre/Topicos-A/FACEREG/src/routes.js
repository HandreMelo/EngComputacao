import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Main from './pages/main/main';
import Create from  './components/Create';
import Edit from './components/Edit';
import Show from './components/Show';
import Detalhe from './components/Detalhes';

const Routes = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path="/" component={Main} />
            <Route path="/create" component={Create} />
            <Route path="/edit/:id" component={Edit} />
            <Route path="/show" component={Show} />
            <Route path="/detalhe/:id" component={Detalhe} />
        </Switch>
    </BrowserRouter>
);

export default Routes;