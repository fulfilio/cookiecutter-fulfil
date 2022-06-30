import React from 'react';
import { Route, Redirect, Switch } from 'react-router-dom';

// Containers
import DashboardPage from '../containers/dashboard/index.js';


const Routes = () => {
    return (
        <Switch>
            <Route path="/" component={DashboardPage} />
        </Switch>
    )
}

export default Routes;
