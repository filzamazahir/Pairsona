'use strict';

angular.module('app')
    .directive('profile', function () {
        return {
            restrict: 'E',
            templateUrl: 'profile.html',
            scope: {},
            controller: 'ProfileController'
        };
    });

angular.module('app')
    .controller('ProfileController', ['$log', '$scope', '$rootScope',
        function ($log, $scope, $rootScope) {


            $scope.profileInfo = $rootScope.profileInfo;
            $log.debug($scope.profileInfo);

            /*var btnText = { 'btnText' : 'Connect' };

            $scope.profileInfo = $scope.profileInfo.map(function(obj) {
                return angular.extend(obj, btnText);
            });*/
            /*{
                'username': 'Filza M.',
                'country': 'Pakistan',
                'languages': ['Urdu', 'Hindi', 'English'],
                'arrivalDate': '03/2015',
                'btnText': 'Connect',
                'helper': true,
                'services': ['Social visits', 'Financial advice']
            }*/

        }]
    );