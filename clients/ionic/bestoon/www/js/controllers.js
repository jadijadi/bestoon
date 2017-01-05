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

.controller('ExpenseCtrl', function($scope, $http) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});
  $scope.submit = function() {
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $http.post(
      'http://bestoon.ir/submit/expense/',
      'token=test&text='+$scope.text+'&amount='+$scope.amount
    )
    .success(function(data){
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

.controller('ExpenseDetailCtrl', function($scope, $stateParams, Expense) {
  $scope.expense = Expense.get($stateParams.expenseId);
})

.controller('IncomeCtrl', function($scope, $http) {
  $scope.submit = function() {
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $http.post(
      'http://bestoon.ir/submit/income/',
      'token=test&text='+$scope.text+'&amount='+$scope.amount
    )
    .success(function(data){
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
