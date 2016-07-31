'use strict';

angular.module('app')
    .directive('register', function () {
        return {
            restrict: 'E',
            templateUrl: 'register.html',
            scope: {},
            controller: 'RegisterController'
        };
    });

angular.module('app')
    .controller('RegisterController', ['$log', '$scope', '$rootScope',
        function ($log, $scope, $rootScope) {

        }]
    );