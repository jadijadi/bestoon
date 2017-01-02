angular.module('starter.controllers', [])

.controller('DashCtrl', function($scope, $http) {
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
  $http.post(
    'http://bestoon.ir/q/generalstat/',
    'token=test'
  )
  .success(function(data){
    $scope.generalstat = data;
  })
  .error(function() {
    $scope.message = 'erorr reading from bestoon stats' //TODO: show some error to user
    console.log('error on request')
  })
})

.controller('ExpenseCtrl', function($scope, Expense) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.expense = Expense.all();
  $scope.remove = function(expense) {
    Expense.remove(expense);
  };
})

.controller('ExpenseDetailCtrl', function($scope, $stateParams, Expense) {
  $scope.expense = Expense.get($stateParams.expenseId);
})

.controller('IncomeCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
});
