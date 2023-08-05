# -*- coding: utf-8 -*-

"""
Hulkbuster's JackHammer
"""

import pandas as pd
import datetime

import pyfolio as pf
import inspect

from collections import namedtuple

from .helper import *
from .loader import load_dataset
from .calendar import *
from .constructor import rebalancing, adjusting

import vrksa.research.historysets as vh

Result = namedtuple('Result', 'stats returns weights trades')


class ScoreBasedPortfolio(object):
    """
    Basic class for backtesting


    """

    def __init__(self, name, universe=None):
        self._name = None
        self._prices = None
        self._calendar = None
        self._schedule = None
        self._scores = None
        self._scores_fn = None
        self._universe = None
        self._policy = None
        self._optimizer = None
        self._backtest_result = None
        self.name = name  # use setter
        self.universe = universe  # use setter

    def __repr__(self):
        desc = 'ScoreBasedPortfolio\nname: {}\nuniverse: {}\npolicy: {}'
        return desc.format(self._name, self._universe, self._policy)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        name = name.replace(' ', '_')
        self._name = name

    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, universe):
        if universe is None:
            print('Default Universe is [KOSPI & KOSAQ & ETF]')
            universe = 'KRE'

        if universe in 'KRE KOSPI KOSPI200 KOSDAQ ETF'.split():
            self._universe = universe
        else:
            raise ValueError('Universe %r is not supported yet.' % universe)

    @property
    def policy(self):
        return self._policy

    @property
    def schedule(self):
        return self._policy['schedule']

    @schedule.setter
    def schedule(self, schedule):
        self._policy['schedule'] = schedule
        self._schedule = None
        self._backtest_result = None

    @property
    def method(self):
        return self._policy['method']

    @method.setter
    def method(self, method):
        self._policy['method'] = method
        self._backtest_result = None

    @property
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, optimizer):
        self._optimizer = optimizer
        self._backtest_result = None

    @property
    def backtest_result(self):
        if self._backtest_result is None:
            raise NoBacktestResult
        else:
            return self._backtest_result

    def _print_scores(self):
        lines = inspect.getsource(self._scores_fn)
        return lines

    def _add_date_index(self, dt, df):
        ddf = df.copy()
        ddf['date'] = dt
        old_index = df.index.name
        new_index = ['date', old_index]
        ddf.reset_index(inplace=True)
        ddf.set_index(new_index, inplace=True)
        return ddf

    def _generate_scores(self):
        if self._scores is not None:
            return
        print('>>> Generating Scores...')
        self._scores = self._scores_fn()

    def _generate_prices(self):
        if self._prices is not None:
            return
        print('>>> Generating Universe...')
        self._prices = load_dataset('universe', universe=self._universe)

    def _generate_calendar(self):
        if self._calendar is not None:
            return
        print('>>> Generating Calendar...')
        calendar = load_dataset('calendar', universe=self._universe)
        self._calendar = calendar[calendar.BSD == 1]  # Only business days

    def _generate_schedule(self):
        self._generate_calendar()
        if self._schedule is not None:
            return
        print('>>> Generating Schedule...')
        try:
            schedule = self._policy['schedule']
        except TypeError:   # if there is no policy (for blank backtest)
            self._schedule = []
            return

        if isinstance(schedule, str):
            if schedule == 'WSE':  # When Scores Exist : calendar에 리밸런싱 데이 추가
                self._generate_scores()
                self._schedule = self._scores.index.get_level_values(0).unique()
            else:
                try:
                    stdday = schedule[:3]
                    offset = 0 if len(schedule) == 3 else int(schedule[3:])
                    self._schedule = self._calendar[self._calendar.shift(offset)[stdday] == 1].index
                except:
                    raise ValueError('Unsupported schedule option')
        elif isinstance(schedule, list):
            try:
                rebalancing_dates = pd.DatetimeIndex(schedule).tz_localize('utc')
            except TypeError as e:
                pass  # already time zone aware object
            # check if all rebalancing dates are a business day.
            mask = [x not in self._calendar.index for x in rebalancing_dates]
            if np.any(mask):
                raise ValueError('Input date [{}] is not a business day'.format(rebalancing_dates[mask][0]))
            else:
                self._schedule = rebalancing_dates

    def _check_prices_data(self, date, returns, cashouts):
        # Are there any big jump in daily return?
        itms = returns[(returns > 0.31) | (returns < -0.31)].index.values
        for itm in itms:
            rtn = returns.loc[itm]
            print('[{}] ERROR> Abnormal daily return: {} {:+.2f}% --> 0.0%'.format(date.strftime('%Y-%m-%d'), itm, rtn * 100))
            returns.loc[itm] = 0     # 0 처리

        # Are there any cashing out?
        itms = returns[returns.isnull()].index.values
        for itm in itms:
            if itm not in cashouts:
                print('[{}] ERROR> No price data: {} --> Cashing out'.format(date.strftime('%Y-%m-%d'), itm))
                cashouts.add(itm)
        returns.fillna(0, inplace=True)  # batch processing

    def _generate_result(self, returns, weights, trades):
        returns = pd.DataFrame(returns, columns=['date', 'daily_return'])
        returns.set_index('date', inplace=True)
        stats = pf.timeseries.perf_stats(returns.daily_return)
        result = Result(stats, returns, weights, trades)
        self._backtest_result = result
        return result

    def set_rule(self, policy, scores, optimizer=None):
        """
        Set the portfolio construction rule.

        Parameters
        ----------
        scores : function(recommended) or multi-index dataframe
        policy : dictionary(schedule and method)
        optimizer : Jackhammer optimizer object

        Returns
        --------
        None

        """
        # initialize
        if callable(scores):
            self._scores = None  # will be generated when necessary
            self._scores_fn = scores
        elif isinstance(scores, pd.DataFrame):
            self._scores = scores
            self._scores_fn = None
        else:
            raise ValueError('scores must be a function or a dataframe.')

        self._backtest_result = None
        self._policy = policy
        self._optimizer = optimizer

    def run_backtest(self, *, start='1900-01-01', end='2099-12-31', initial_portfolio=None):

        """
        Run the backtest.
        The result will be saved in the <obejct>.backtest_result

        Parameters
        ----------
        start : string, 'yyyy-mm-dd'
        end : string, 'yyyy-mm-dd'
        initial_portfolio : single-index dataframe

        Returns
        -------
        None

        """

        self._generate_prices()

        self._generate_calendar()

        self._generate_schedule()

        print('>>> Backtesting...')

        portfolio = initial_portfolio  # None or dataframe
        portfolios = pd.DataFrame()
        trades = pd.DataFrame()
        portfolio_return = 0.0
        portfolio_returns = []
        cashout_list = set()
        for td in self._calendar.loc[start:end].index:
            # Calculate portfolio's daily return and Adjust weights based on items' daily return.
            if portfolio is not None:
                td_prices = self._prices.xs(td)
                td_returns = portfolio.join(td_prices)['daily_return']
                self._check_prices_data(td, td_returns, cashout_list)
                portfolio_return = (portfolio['weight'] * td_returns).sum()
                portfolio['weight'] *= (1+td_returns) / (1+portfolio_return)

            # Rebalancing
            if td in self._schedule:
                self._generate_scores()
                portfolio, trade = rebalancing(date=td,
                                               scores=self._scores,
                                               policy=self._policy,
                                               optimizer=self._optimizer,
                                               old_portfolio=portfolio)
                trades = trades.append(self._add_date_index(td, trade))
                cashout_list = set()  # reset!!!

            # Adjusting for events
            # portfolio, trade = adjusting(date=td, old_portfolio=tmp_portfolio)
            # trades = trades.append(trade)

            # Logging
            if portfolio is not None:
                portfolios = portfolios.append(self._add_date_index(td, portfolio))
                portfolio_returns.append([td, portfolio_return])

        self._generate_result(portfolio_returns, portfolios, trades)

        print('\n>>> SUCCESS')

    def report_backtest(self, benchmark='KOSPI200', relative=False):
        """
        Show statistics and charts.

        Parameters
        ----------
        benchmark : 'KOSPI', 'KOSPI200', 'KOSDAQ', 'KOSDAQ150'
        relative : True or False

        Returns
        -------
        None

        """
        if isinstance(benchmark, pd.Series):
            bm = benchmark
        else:  # benchmark is string
            bm_list = {'KOSPI': vh.kospi.close,
                       'KOSPI200': vh.kospi200.close,
                       'KOSDAQ': vh.kosdaq.close,
                       'KOSDAQ150': vh.kosdaq_150.close}
            bm = bm_list[benchmark].history()
            bm = bm.pct_change()
            bm.name = benchmark

        rtns = self._backtest_result.returns.daily_return   # series
        wgts = self._backtest_result.weights.weight        # series
        if relative:
            rtns = (rtns - bm).dropna()

        create_report(rtns, wgts, bm)
