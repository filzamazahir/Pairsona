'use strict';

angular.module('app')
    .directive('searchResults', function () {
        return {
            restrict: 'E',
            templateUrl: 'search-results.html',
            scope: {},
            controller: 'SearchResultsController'
        };
    });

angular.module('app')
    .controller('SearchResultsController', ['$log', '$scope', '$rootScope', '$location',
        function ($log, $scope, $rootScope, $location) {

            $scope.gotoProfile = function (persona) {
                $rootScope.profileInfo = persona;
                $location.url("/profile");
            };

            $scope.data =  {
                "searchresults": [
                    {
                        "country_origin": "Syria",
                        "created_at": "Sun, 31 Jul 2016 10:10:58 GMT",
                        "description": "Description is here",
                        "email": "firstperson@gmail.com",
                        "first_name": "Filza M.",
                        "helper": 0,
                        "id": 1,
                        "last_name": "Person",
                        "password": "$2b$12$W6LqIey7qNbMI550K5QzjuF.tZvoB0eKnh6KTNrNHsDswssR6jxNK",
                        "updated_at": "Sun, 31 Jul 2016 10:10:58 GMT",
                        "username": "Filza",
                        "services": ['Social visits', 'Financial advice'],
                        "zipcode": "93456",
                        "profileImg": "pic.png",
                        "btnText": "Connect"
                    },
                    {
                        "country_origin": "Germany",
                        "created_at": "Sun, 31 Jul 2016 10:12:27 GMT",
                        "description": "Description is here",
                        "email": "thirdhelper@gmail.com",
                        "first_name": "Marissa S.",
                        "helper": 1,
                        "id": 3,
                        "last_name": "Helper",
                        "password": "$2b$12$OG7q0pFH1GfYvIgApDtg0OU.0IpVJeoLUzwMzgGT5eNSpRv.uHyte",
                        "updated_at": "Sun, 31 Jul 2016 10:12:27 GMT",
                        "username": "Marissa",
                        "services": ['Former Immigrant', 'English Tutoring', 'Language Translator'],
                        "zipcode": "93456",
                        "profileImg": "pic4.jpg",
                        "btnText": "Connect"
                    }
                ]
            };

            $scope.searchResults = $scope.data.searchresults;


                /*[
                    {
                        'username': 'Filza M.',
                        'country': 'Pakistan',
                        'services': ['Social Visits', 'Language Translator', 'English Tutoring']
                    },
                    {
                        'username': 'Filza M.',
                        'country': 'Pakistan',
                        'services': ['Social Visits', 'Language Translator', 'English Tutoring']
                    },
                    {
                        'username': 'Filza M.',
                        'country': 'Pakistan',
                        'services': ['Social Visits', 'Language Translator', 'English Tutoring']
                    },
                    {
                        'username': 'Filza M.',
                        'country': 'Pakistan',
                        'services': ['Social Visits', 'Language Translator', 'English Tutoring']
                    }
                ];*/

        }]
    );