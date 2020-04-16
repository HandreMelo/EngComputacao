import React from 'react';

import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Main from './pages/main/main';
import Register from  './pages/register/register';

const Routes = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path="/" component={Main} />
            <Route path="/register" component={Register} />
        </Switch>
    </BrowserRouter>
);

export default Routes;