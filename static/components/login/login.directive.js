'use strict';

angular.module('app')
    .directive('login', function () {
        return {
            restrict: 'E',
            templateUrl: 'login.html',
            scope: {},
            controller: 'LoginController'
        };
    });

angular.module('app')
    .controller('LoginController', ['$log', '$scope', '$rootScope',
        function ($log, $scope, $rootScope) {

        }]
    );