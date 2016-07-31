'use strict';

angular.module('app')
    .directive('landing', function () {
        return {
            restrict: 'E',
            templateUrl: 'landing.html',
            scope: {},
            controller: 'LandingController'
        };
    });

angular.module('app')
    .controller('LandingController', ['$log', '$scope', '$rootScope', '$location',
        function ($log, $scope, $rootScope, $location) {
            $scope.languages = [
                {id: '', disabled: true, name: 'Select a language'},
                {id: '1', disabled: false, name: 'English'},
                {id: '2', disabled: true, name: 'Ukranian'},
                {id: '3', disabled: true, name: 'Urdu'},
                {id: '4', disabled: true, name: 'Russian'}
            ];

            $scope.selectedLanguage = 'Select a language';

            $scope.selectLanguage= function () {
                $log.debug("In select language");
                $location.url('/home');
            };
        }]
    );