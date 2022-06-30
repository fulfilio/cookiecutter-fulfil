import React  from 'react';
import ReactDom from 'react-dom';
import {AppProvider} from '@shopify/polaris';
import {HashRouter} from 'react-router-dom';

import App from './app/app.js'

const app = (
  <AppProvider>
    <HashRouter>
      <App />
    </HashRouter>
  </AppProvider>
);

ReactDom.render(app, document.getElementById('app'));
