'use strict';

angular.module('app')
    .directive('search', function () {
        return {
            restrict: 'E',
            templateUrl: 'search.html',
            scope: {},
            controller: 'SearchController'
        };
    });

angular.module('app')
    .controller('SearchController', ['$log', '$scope', '$rootScope', '$location',
        function ($log, $scope, $rootScope, $location) {
            $scope.availableOptions = [
                {id: '1', name: 'Financial Advice'},
                {id: '2', name: 'Real Estate'},
                {id: '3', name: 'Automobile Help'},
                {id: '4', name: 'English Tutoring'},
                {id: '5', name: 'Language Translator'},
                {id: '6', name: 'Social Visits'},
                {id: '7', name: 'Former immigrant'}
            ];

            $scope.search = function () {
                $location.url("/results")
            };
        }]
    );