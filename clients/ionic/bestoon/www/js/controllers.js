angular.module('starter.controllers', [])


  .controller('ConfigCtrl', function($scope, $http, $state, $ionicHistory) {
    $scope.loggedin = false;
    token = storage.getItem('token');
    if (token) {
      $scope.loggedin = true;
    }

    $scope.login = function() { // check passwsord and user name with webservice
      $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
      $http.post(
          bestoonURL + '/accounts/login/',
          'username=' + $scope.username + '&password=' + $scope.password
        )
        .success(function(data) {
          if (data.result == 'ok') {
            token = data['token'];
            storage.setItem('token', token);
            $scope.loggedin = true;
            console.log('logged in with token:' + token);
            $ionicHistory.clearCache([$state.current.name]).then(function() {
              $state.reload();
            })
          } else {
            // request was fine, but error on username / password
            // TODO: toast message about failed login
          }
        })
        .error(function() {
          $scope.message = 'erorr logging in' //TODO: show some error to user
          console.log('error on login request')
        })
    }

    $scope.logout = function() {
      console.log('logout');
      storage.removeItem('token');
      $scope.loggedin = false;
      token = null;
      $ionicHistory.clearCache([$state.current.name]).then(function() {
        $state.reload();
      })
    }
  })
  .controller('NewsCtrl', function($scope, $http) {
      $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
      $http.post(bestoonURL + '/news/').success(function(data) {
          $scope.news = JSON.parse(data);
        }).error(function() {
          $scope.message = 'erorr reading news' //TODO: show some error to user       console.log('error on request')
        })
  })
  .controller('DashCtrl', function($scope, $http, $state) {
          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(
                bestoonURL + '/q/generalstat/',
                'token=' + token
              )
              .success(function(data) {
                $scope.generalstat = data;
              })
              .error(function() {
                $scope.message = 'erorr reading from bestoon stats' //TODO: show some error to user
                console.log('error on request')
              })
          });
        })

        .controller('ExpenseCtrl', function($scope, $http, $state) {
          // With the new view caching in Ionic, Controllers are only called
          // when they are recreated or on app start, instead of every page change.
          // To listen for when this page is active (for example, to refresh data),
          // listen for the $ionicView.enter event:
          //
          //$scope.$on('$ionicView.enter', function(e) {
          //});
          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }
          })

          $scope.submit = function() {
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(
                bestoonURL + '/submit/expense/',
                'token=' + token + '&text=' + $scope.text + '&amount=' + $scope.amount
              )
              .success(function(data) {
                $scope.text = '';
                $scope.amount = '';
                // show a TOAST
              })
              .error(function() {
                $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
                console.log('error while submitting expense')
              })
          }

        })

        .controller('ExpenseDetailCtrl', function($scope, $stateParams, $state, Expense) {
          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }
          })

          $scope.expense = Expense.get($stateParams.expenseId);
        })

        .controller('IncomeCtrl', function($scope, $http, $state) {
          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }
          })

          $scope.submit = function() {
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(
                bestoonURL + '/submit/income/',
                'token=' + token + '&text=' + $scope.text + '&amount=' + $scope.amount
              )
              .success(function(data) {
                $scope.text = '';
                $scope.amount = '';
                // show a TOAST
              })
              .error(function() {
                $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
                console.log('error while submitting income')
              })
          }
        });
