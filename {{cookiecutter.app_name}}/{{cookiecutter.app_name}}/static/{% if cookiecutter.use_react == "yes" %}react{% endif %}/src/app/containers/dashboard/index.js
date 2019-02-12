import React from 'react';
import PropTypes from 'prop-types';

import { AppProvider, Frame, ActionList, Card, TopBar, Navigation, Link, Button, Spinner } from '@shopify/polaris';
import Api from '../../api/index.js';
import style from './style.css';


const theme = {
  colors: {
    topBar: {
      background: '#1e3d58',
    },
  },
  logo: {
    width: 140,
    topBarSource:
      'https://cdn.fulfil.io/assets/logo/full-transparent-white.png',
    contextualSaveBarSource:
      'https://cdn.fulfil.io/assets/logo/icon-transparent.png',
    url: '#',
    accessibilityLabel: 'Fulfil.io Logo',
  },
};


class FrameComponent extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      userName: ''
    };
    this.userMenuActions = [
      {
        items: [
          {content: 'Logout', icon: 'logOut',
            onAction: () => { this.onLogout() }
          }
        ],
      },
    ];
  }

  componentDidMount() {
    debugger;
    Api.user().then((res) => {
      this.setState({
        userName: res.data.name,
        userEmail: res.data.email,
        loading: false
      })
    })
  }

  onLogout() {
    window.location.href = '/logout'
  }

  toggleState(key) {
    return () => this.setState((prevState) => ({ [key]: !prevState[key] }));
  };

  getInitials(name) {
    var initials = name.match(/\b\w/g) || [];
    initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
    return initials
  }

  renderTopBar() {
    const { userMenuOpen, userName, userEmail } = this.state;

    var initials = this.getInitials(userName)

    const userMenuMarkup = (
      <TopBar.UserMenu
        actions={this.userMenuActions}
        name={userName}
        detail={userEmail}
        initials={initials}
        open={userMenuOpen}
        onToggle={this.toggleState('userMenuOpen')}
      />
    );

    const topBarMarkup = (
      <TopBar
        showNavigationToggle={true}
        userMenu={userMenuMarkup}
        onNavigationToggle={this.toggleState('showMobileNavigation')}
      />
    );

     return topBarMarkup;
  }

  renderNavigation() {
    const { userName } = this.state;

    var initials = this.getInitials(userName)

    const navigationUserMenuMarkup = (
      <Navigation.UserMenu
        actions={this.userMenuActions}
        name={userName}
        avatarInitials={initials}
      />
    );

    const navigationMarkup = (
      <Navigation location="/" userMenu={navigationUserMenuMarkup}>
        <Navigation.Section
          items={[
            {
              label: 'Dashboard',
              icon: 'home',
            }
          ]}/>
          <Navigation.Section
            title='Navigation'
            items={[]} />
          </Navigation>
    );

    return navigationMarkup;
  }

  render() {
    const { showMobileNavigation, loading } = this.state;
    if (loading) {
      return <div className={style.loading}><Spinner /></div>
    }

    return(
      <AppProvider theme={theme}>
        <Frame
          topBar={this.renderTopBar()}
          navigation={this.renderNavigation()}
          showMobileNavigation={showMobileNavigation}
          onNavigationDismiss={this.toggleState('showMobileNavigation')}
        >
        </Frame>
      </AppProvider>
    )
  }
}

export default FrameComponent;
