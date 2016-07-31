'use strict';

// Declare app level module which depends on views, and components
angular.module('app', [
  'ngRoute'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  when("/home", {
    templateUrl: "components/home/home.html",
    controller: "HomeController"
  }).
  when("/login", {
    templateUrl: "components/login/login.html",
    controller: "LoginController"
  }).
  when("/register", {
    templateUrl: "components/register/register.html",
    controller: "RegisterController"
  }).
  when("/landing", {
    templateUrl: "components/landing/landing.html",
    controller: "LandingController"
  }).
  when("/profile", {
    templateUrl: "components/profile/profile.html",
    controller: "ProfileController"
  }).
  when("/results", {
    templateUrl: "components/search-results/search-results.html",
    controller: "SearchResultsController"
  }).
  when("/search", {
    templateUrl: "components/search/search.html",
    controller: "SearchController"
  }).
  when("/connections", {
    templateUrl: "components/connections/connections.html",
    controller: "ConnectionsController"
  }).
  otherwise({
    redirectTo: '/landing'
  });
}]);
