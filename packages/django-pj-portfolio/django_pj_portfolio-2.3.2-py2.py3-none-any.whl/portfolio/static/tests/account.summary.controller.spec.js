(function () {
    'use strict';

    describe('AccountSummaryController', function() {

        var ctrl;
        var $rootScope, $q, $timeout, $httpBackend;
        var deferreds =  {};
        var Positions, Securities, Accounts, Currencies;
        var vm;

        function resolvePromises() {
            /* Resolve the promises */

            deferreds.Positions.all.resolve({
                data: getJSONFixture('positions_detail.json')
            });

            deferreds.Securities.all.resolve({
                data: getJSONFixture('securities.json')
            });

            deferreds.Accounts.all.resolve({
                data: getJSONFixture('positions_detail.json')
            });

            deferreds.Currencies.all.resolve({
                data: getJSONFixture('currencies.json')
            });


            deferreds.Positions.google_local_quote.resolve({
                data: getJSONFixture('google_quote.json')
            });

            /* Promises are processed upon each digest cycle.
               Do that now
            */
            $rootScope.$digest();

            /* getLivePrices will call itself after timer has been expired.
               Cancel that timer to prevent that from happening
            */
            $timeout.cancel(vm.liveTimer);

            /* flush the timers */
            $timeout.flush();
        }

        beforeEach(function () {
            module('portfolio')
            inject(function($controller, _$rootScope_, _$q_, _$timeout_,
                            _$httpBackend_, $location) {

                $rootScope = _$rootScope_;
                $q = _$q_;
                $timeout = _$timeout_;
                $httpBackend = _$httpBackend_

                /* Mock the services */
                deferreds.Positions = {
                    all: $q.defer(),
                    google_quote: $q.defer(),
                    yahoo_quote: $q.defer(),
                    google_local_quote: $q.defer()
                };

                deferreds.Securities = {
                    all: $q.defer()
                };

                deferreds.Accounts = {
                    all: $q.defer()
                };

                deferreds.Currencies = {
                    all: $q.defer()
                };

                jasmine.getJSONFixtures()
                    .fixturesPath='base/portfolio/static/tests/mock';

                Positions = {
                    all: jasmine.createSpy('Positions', ['all'])
                        .and.returnValue(deferreds.Positions.all.promise),
                    google_quote: jasmine.createSpy('Positions',
                                                    ['google_quote'])
                        .and.returnValue(deferreds.Positions.google_quote.promise),
                    yahoo_quote: jasmine.createSpy('Positions',
                                                    ['yahoo_quote'])
                        .and.returnValue(
                            deferreds.Positions.yahoo_quote.promise),
                    google_local_quote: jasmine.createSpy('Positions',
                                                    ['google_local_quote'])
                        .and.returnValue(
                            deferreds.Positions.google_local_quote.promise)
                };

                Securities = {
                    all: jasmine.createSpy('Securities', ['all'])
                        .and.returnValue(deferreds.Securities.all.promise)
                };

                Accounts = {
                    all: jasmine.createSpy('Accounts', ['all'])
                        .and.returnValue(deferreds.Accounts.all.promise)
                };

                Currencies = {
                    all: jasmine.createSpy('Currencies', ['all'])
                        .and.returnValue(deferreds.Currencies.all.promise)
                };

                vm = $controller('AccountSummaryController', {
                    $rootScope: $rootScope,
                    Positions: Positions,
                    Securities: Securities,
                    Accounts: Accounts,
                    Currencies: Currencies
                });

            });
        });


        afterEach(function() {
            $timeout.verifyNoPendingTasks();
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should have controller defined', function() {
            expect(vm).toBeDefined();
        });

        it('should have Positions defined', function() {

            resolvePromises();
            expect(vm.positions['Whitestone REIT']['price']).toBeDefined();
        });
        
        it('should calculate market value correctly', function() {
            var usdRate = 1.054407

            /* Initial values are for Elisa */
            var price = 30.01;
            var count = 972;
            var expectedMarketValue;
            
            
            resolvePromises();
            /* Currency for Elisa is EUR, hence the market value need no
               exchange rate correction */

            expectedMarketValue = price * count;
            expect(vm.positions['Elisa']['mktval'])
                .toBeCloseTo(expectedMarketValue, 2);

            /* WSR */
            price = 14.0;
            count = 1500;
            
            /* WSR is in USD, convert to EUR */
            expectedMarketValue = price * count / usdRate;
            expect(vm.positions['Whitestone REIT']['mktval'])
                .toBeCloseTo(expectedMarketValue, 1); 

        });
    });
})();
