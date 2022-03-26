angular.module('starter.controllers', ['ionic'])
  .controller('ConfigCtrl', function($scope, $http, $state, $ionicHistory, ) {
    $scope.loggedin = false;
    $scope.tabTitle = 'ورود';
    token = storage.getItem('token');
    if (token) {
      $scope.loggedin = true;
      $scope.tabTitle = 'تنظیمات';
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
              $ionicHistory.clearCache(['tab']).then(function() {
                $state.reload();
              })
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
        $ionicHistory.clearCache(['tab']).then(function() {
          $state.reload();
        })
      })
    }
  })
  .controller('NewsCtrl', function($scope, $http, $state) {
    $scope.$on('$ionicView.enter', function(e) {
      $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
      $http.post(bestoonURL + '/news/').success(function(data) {
          $scope.news = JSON.parse(data);
        }).error(function() {
          $scope.message = 'erorr reading news' //TODO: show some error to user       console.log('error on request')
        })
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

        .controller('ExpenseCtrl', function($scope, $http, $state, $ionicModal) {
          // With the new view caching in Ionic, Controllers are only called
          // when they are recreated or on app start, instead of every page change.
          // To listen for when this page is active (for example, to refresh data),
          // listen for the $ionicView.enter event:
          //
          //$scope.$on('$ionicView.enter', function(e) {
          //});

          $ionicModal.fromTemplateUrl('expense-edit-modal.html', {
            scope: $scope,
            animation: 'slide-in-left',//'slide-left-right', 'slide-in-up', 'slide-right-left'            
          }).then(function(modal) {
            $scope.modal = modal;
          });


          $scope.openModal = function() {
            $scope.modal.show();
          };
          $scope.submitExpenseModal = function() {
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(
                bestoonURL + '/edit/expense/',
                'token=' + token + '&text=' + $scope.editexpense.text + '&amount=' + $scope.editexpense.amount + '&id=' + $scope.editexpense.pk
              )
              .success(function(data) {

                // show a TOAST
                $scope.modal.hide();
                // update the expenses part, containing the new one
                $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
                $http.post(bestoonURL + '/q/expenses/', 'token='+token).success(function(data) {
                    $scope.expenses = JSON.parse(data);
                  }).error(function() {
                    $scope.message = 'erorr reading previous expenses' //TODO: show some error to user       console.log('error on request')
                })
              })
              .error(function() {
                $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
                console.log('error while submitting expense')
              })
          };
          $scope.closeModal = function() {
            $scope.modal.hide();
          };
          // Cleanup the modal when we're done with it!
          $scope.$on('$destroy', function() {
            $scope.modal.remove();
          });
          // Execute action on hide modal
          $scope.$on('modal.hidden', function() {
            // Execute action
          });
          // Execute action on remove modal
          $scope.$on('modal.removed', function() {
            // Execute action
          });

          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(bestoonURL + '/q/expenses/', 'token='+token).success(function(data) {
                $scope.expenses = JSON.parse(data);
              }).error(function() {
                $scope.message = 'erorr reading previous expenses' //TODO: show some error to user       console.log('error on request')
            })
          })

          $scope.shouldShowDelete = false;
          $scope.listCanSwipe = true

          $scope.edit = function(item) {
            $scope.modal_edit_amount = item.fields.amount;
            $scope.modal_edit_text = item.fields.text;
            $scope.modal_edit_pk = item.pk;
            $scope.editexpense = {amount: item.fields.amount, pk: item.pk, text: item.fields.text}
            $scope.modal.show();
          }

          $scope.delete = function(item) {
            console.log('we are in delete for expense item '+item.pk);
          }


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

                // update the expenses part, containing the new one
                $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
                $http.post(bestoonURL + '/q/expenses/', 'token='+token).success(function(data) {
                    $scope.expenses = JSON.parse(data);
                  }).error(function() {
                    $scope.message = 'erorr reading previous expenses' //TODO: show some error to user       console.log('error on request')
                })
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

        .controller('IncomeCtrl', function($scope, $http, $state, $ionicModal) {

          $ionicModal.fromTemplateUrl('income-edit-modal.html', {
            scope: $scope,
            animation: 'slide-in-left',//'slide-left-right', 'slide-in-up', 'slide-right-left'            
          }).then(function(modal) {
            $scope.modal = modal;
          });


          $scope.openModal = function() {
            $scope.modal.show();
          };
          $scope.submitIncomeModal = function() {
            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(
                bestoonURL + '/edit/income/',
                'token=' + token + '&text=' + $scope.editincome.text + '&amount=' + $scope.editincome.amount + '&id=' + $scope.editincome.pk
              )
              .success(function(data) {

                // show a TOAST
                $scope.modal.hide();
                // update the expenses part, containing the new one
                $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
                $http.post(bestoonURL + '/q/incomes/', 'token='+token).success(function(data) {
                    $scope.incomes = JSON.parse(data);
                  }).error(function() {
                    $scope.message = 'erorr reading previous incomes' //TODO: show some error to user       console.log('error on request')
                })
              })
              .error(function() {
                $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
                console.log('error while submitting expense')
              })
          };
          $scope.closeModal = function() {
            $scope.modal.hide();
          };
          // Cleanup the modal when we're done with it!
          $scope.$on('$destroy', function() {
            $scope.modal.remove();
          });
          // Execute action on hide modal
          $scope.$on('modal.hidden', function() {
            // Execute action
          });
          // Execute action on remove modal
          $scope.$on('modal.removed', function() {
            // Execute action
          });


          $scope.$on('$ionicView.enter', function(e) {
            if (!token) {
              back_to_login_page($scope, $state);
            }

            $scope.shouldShowDelete = false;
            $scope.listCanSwipe = true

            $scope.edit = function(item) {
              $scope.modal_edit_amount = item.fields.amount;
              $scope.modal_edit_text = item.fields.text;
              $scope.modal_edit_pk = item.pk;
              $scope.editincome = {amount: item.fields.amount, pk: item.pk, text: item.fields.text}
              $scope.modal.show();
            }

            $scope.delete = function(item) {
              console.log('we are in delete for income item '+item.pk);
            }

            $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
            $http.post(bestoonURL + '/q/incomes/', 'token='+token).success(function(data) {
                $scope.incomes = JSON.parse(data);
              }).error(function() {
                $scope.message = 'erorr reading previous incomes' //TODO: show some error to user       console.log('error on request')
            })
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

                // update the incomes part, containing the new one
                $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
                $http.post(bestoonURL + '/q/incomes/', 'token='+token).success(function(data) {
                    $scope.incomes = JSON.parse(data);
                  }).error(function() {
                    $scope.message = 'erorr reading previous incomes' //TODO: show some error to user       console.log('error on request')
                })
              })
              .error(function() {
                $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
                console.log('error while submitting income')
              })
          }
        })
  .controller('TabsCtrl', function($scope, $rootScope) {
    token = storage.getItem('token');
    $rootScope.loggedin = (token != null);
  });
