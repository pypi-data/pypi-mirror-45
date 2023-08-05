(function () { 
    'use strict';

    angular
        .module('portfolio', [
            'ngRoute',
            'portfolio.account.summary',
            'portfolio.positions',
            'portfolio.securities',
            'loadingSpinner',
            'portfolio.account',
            'portfolio.currency',
            'portfolio.config',
            'angular-toArrayFilter',
        ]);

    angular
        .module('portfolio.config', []);

})(); 

