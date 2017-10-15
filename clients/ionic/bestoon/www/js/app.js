// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
    .state('tab', {
    url: '/tab',
    abstract: true,
    templateUrl: 'templates/tabs.html',
    controller: 'TabsCtrl'
  })

  // Each tab has its own nav history stack:

  .state('tab.dash', {
    url: '/dash',
    views: {
      'tab-dash': {
        templateUrl: 'templates/tab-dash.html',
        controller: 'DashCtrl'
      }
    }
  })

  .state('tab.expense', {
      url: '/expense',
      views: {
        'tab-expense': {
          templateUrl: 'templates/tab-expense.html',
          controller: 'ExpenseCtrl'
        }
      }
    })
    .state('tab.expense-detail', {
      url: '/expense/:expenseId',
      views: {
        'tab-expense': {
          templateUrl: 'templates/expense-detail.html',
          controller: 'ExpenseDetailCtrl'
        }
      }
    })

  .state('tab.income', {
    url: '/income',
    views: {
      'tab-income': {
        templateUrl: 'templates/tab-income.html',
        controller: 'IncomeCtrl'
      }
    }
  })

  .state('tab.config', {
    url: '/config',
    views: {
      'tab-config': {
        templateUrl: 'templates/tab-config.html',
        controller: 'ConfigCtrl'
      }
    }
  });


  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/tab/dash');
});


function back_to_login_page($scope, $state) {
  token = null;
  $scope.loggedin = false;
  storage.removeItem('token');
  $state.go('tab.config');
}

var storage = window.localStorage;

var token = storage.getItem('token');
//bestoonURL = 'http://localhost:8000';
bestoonURL = 'http://bestoon.ir'; //comment when releasing
