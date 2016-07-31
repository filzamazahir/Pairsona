'use strict';

angular.module('app')
    .directive('home', function () {
        return {
            restrict: 'E',
            templateUrl: 'home.html',
            scope: {},
            controller: 'HomeController'
        };
    });

angular.module('app')
    .controller('HomeController', ['$log', '$scope', '$rootScope', '$location',
        function ($log, $scope, $rootScope, $location) {

            $rootScope.loggedIn = true;
            $scope.validateZipCode = function () {
                $scope.zipForm.zip.$valid = /^[0-9]{5}(?:-[0-9]{4})?$/.test(zipcode);
            };

            $scope.needHelp = function () {
                $location.url('/search');
            };

            $scope.offerHelp = function () {
                $location.url('/search');
            };
        }]
    );