# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:38:37 2019

@author: Guest Group
"""

import pandas as pd
import numpy as np
from scipy.optimize import newton

__all__ = ('TEA',)

_DataFrame = pd.DataFrame
_array = np.array
_asarray = np.asarray

# TODO: Add 'SL', 'DB', 'DDB', 'SYD', 'ACRS' and 'MACRS' functions to generate depreciation data

# %% Depreciation data

_MACRS = {'MACRS5':  _array([.2000, .3200, .1920,
                             .1152, .1152, .0576]),
          
          'MACRS7':  _array([.1429, .2449, .1749,
                             .1249, .0893, .0892,
                             .0893, .0446]),
          
          'MACRS10': _array([.1000, .1800, .1440,
                             .1152, .0922, .0737,
                             .0655, .0655, .0656,
                             .0655, .0328]),

          'MACRS15': _array([.0500, .0950, .0855,
                             .0770, .0693, .0623,
                             .0590, .0590, .0591,
                             .0590, .0591, .0590,
                             .0591, .0590, .0591,
                             .0295])}


# %% Cash flow and results info

_cashflow_columns = ('Depreciable capital',
                     'Depreciation',
                     'Fixed capital',
                     'Working capital',
                     'Annual operating cost (excl. depr.)',
                     'Sales',
                     'Net earnings',
                     'Cash flow',
                     'Discounted cash flow',
                     'Cumulative cash flow')


# %% Techno-Economic Analysis

class TEA:
    """Create a TEA object that can perform cash flow analysis on a System object.
    
        **Parameters**
        
            **system:** [System] Should contain feed and product streams.
            
        **Examples**
        
            :doc:`Techno-economic analysis of a biorefinery` 
    
    """
    __slots__ = ('_results', 'system', 'cashflow', '_cached',
                 '_options', '_IRR_guess', '_cost_guess',
                 '_costs', '_costs_data')
    
    #: Default cash flow options
    _default = {'Lang factor': 4.37,
                'Operating days': 330,
                'IRR': 0.15,
                'Wage': 5e4,
                'Year': None,
                'Employees': 50,
                'Fringe benefits': 0.40,
                'Income tax': 0.35,
                'Property tax': 0.001,
                'Property insurance': 0.005,
                'Duration': 20,
                'Supplies': 0.20,
                'Mantainance': 0.01,
                'Administration': 0.005,
                'Working capital': 0.05,
                'Startup': 0,
                'Land': 0,
                'Royalties': 0,
                'Depreciation': 'MACRS7',
                'Startup schedule': (0.4, 0.6),
                'Other recurring costs': 0,
                'Other fixed capital': 0}
    
    _results_units = {'Pay back period': 'yr',
                      'Return on investment': '1/yr',
                      'Net present value': 'USD',
                      'Depreciable capital': 'USD',
                      'Fixed capital investment': 'USD',
                      'Total capital investment': 'USD',
                      'Depreciation': 'USD/yr',
                      'Annual operating cost': 'USD/yr',
                      'Working capital': 'USD',
                      'Utility cost': 'USD/yr',
                      'Material cost': 'USD/yr',
                      'Sales': 'USD/yr',
                      'Labor': 'USD/yr'}
    
    @property
    def options(self):
        """
        [dict] Options for cash flow analysis [-]:
            * **Lang factor:** Used to get fixed capital investment from total purchase cost.
            * **Operating days:** (day).
            * **IRR:** Internal rate of return (fraction).
            * **Wage:** Wage per employee (USD/yr).
            * **Year:** Start year of venture.
            * **Employees:** Number of employees.
            * **Fringe benefits:** Cost of fringe benefits as a fraction of labor cost.
            * **Income tax:** Combined federal and state income tax rate (fraction).
            * **Property tax:** Fee as a fraction of fixed capital investment.
            * **Property insurance:** Fee as a fraction of fixed capital investment.
            * **Duration:** Duration of venture (years).
            * **Supplies:** Yearly fee as a fraction of labor costs.
            * **Mantainance:** Yearly fee as a fraction of fixed capital investment.
            * **Administration:** Yearly fee as a fraction of fixed capital investment.
            * **Working capital:** Fee as a fraction of fixed capital investment.
            * **Startup:** Cost of start up as a fraction of depreciable capital.
            * **Land:** Cost of land as a fraction of depreciable capital.
            * **Royalties:** Cost of royalties as a fraction of depreciable capital.
            * **Depreciation:** 'MACRS' + number of years (e.g. 'MACRS7').
            * **Startup schedule:** tuple of startup investment fractions per year, starting from year 0. For example, for 50% capital investment in year 0 and 50% investment in year 1: (0.5, 0.5).
            * **Other recurring costs:** Any additional recurring costs per year of operation.
            * **Other fixed capital:** Any additional investment not accounted for in equipment cost.
        """
        return self._options
    
    def __init__(self, system):
        self.system = system
        self._options = dict(**self._default)
        
        # [dict] Cached values from '_init' methods:
        #  {operating_days: flowrate_factor,
        #   year_duration: (duration_array, cashflow_data),
        #   depreciation_schedule: (start, Depreciation, D_len, schedule)}
        self._cached = {}
        
        #: [dict] Summarized results of cash flow analysis
        self._results = {}
        
        #: [DataFrame] Cash flow table
        self.cashflow = None
        
        #: Guess IRR for solve_IRR method
        self._IRR_guess = None
        
        #: Guess stream cost for solve_price method
        self._cost_guess = None
        
        units = system._costunits
        units = sorted(units, key=lambda x: x.line)
        costs = [u._totalcosts for u in units]
        
        #: All purchase and utility costs for units
        self._costs_data = costs
        
        index = pd.MultiIndex.from_tuples((u.line, u.ID) for u in units)
        columns = ('Purchase cost (USD)',
                   'Utility cost (USD/hr)')
        
        #: [DataFrame] All purchase and utility costs for units
        self._costs = pd.DataFrame(costs, index, columns)
        
        system._TEA = self

    @property
    def costs(self):
        """[DataFrame] All purchase and utility costs for units."""
        self._costs[:] = self._costs_data
        return self._costs

    def results(self, with_units=True):
        """Return results of techno-economic analysis as a DataFrame object if `with_units` is True or as a Series otherwise."""
        keys = []; addkey = keys.append
        vals = []; addval = vals.append
        if with_units:
            results_units = self._results_units
            for ki, vi in self._results.items():
                addkey(ki)
                addval((results_units.get(ki, ''), vi))
            return pd.DataFrame(vals, keys, ('Units', 'Value'))
        else:
            return pd.Series(self._results)

    def NPV(self):
        """Calculate NPV by cash flow analysis and update the "results" and "cashflow" attributes."""
        flow_factor, cashflow_info, depreciation_data = self._get_cached_data()
        cashflow_data, duration_array = cashflow_info
        parameters = self._calc_parameters(flow_factor)
        self._calc_cashflow(cashflow_data,
                            parameters[:-3],
                            depreciation_data)
        NPV = self._calc_NPV_and_update(self.options['IRR'],
                                        cashflow_data[-3:],
                                        duration_array)
        self._update_results(parameters, cashflow_data[-1, -1])
        return NPV
    
    def production_cost(self, *products):
        """Return production cost of products.
        
        **Parameters**
        
            ***products:** [Stream] Main products of the system
        
        .. Note::
           If there is more than one main product, The production cost is proportionally allocated to each of the main products with respect to their marketing values. The marketing value of each product is determined by the annual production multiplied by its selling price.
        """
        system = self.system
        sysfeeds = system.feeds
        sysproducts = system.products
        o = self.options
        flow_factor = 24*o['Operating days']
        o = self.options
        DC_, UC_ = self.costs.sum(0) # Depreciable capital (USD) and utility cost (USD/hr)
        MC_ = 0 # Material cost USD/hr
        CP_ = 0 # Coproducts USD/hr
        for s in sysfeeds:
            price = s.price
            if price: MC_ += price*s.massnet
        for s in sysproducts:
            if s not in products:
                price = s.price
                if price: CP_ += price*s.massnet
        # Multiply by flow_factor for USD/yr
        UC_ *= flow_factor
        MC_ *= flow_factor
        CP_ *= flow_factor
        DC_ *= o['Lang factor']
        FC_ = DC_ * (1 + o['Startup'] + o['Land'] + o['Royalties']) + o['Other fixed capital']
        fb = o['Fringe benefits'] + o['Supplies']
        f =  (o['Mantainance']
            + o['Administration']
            + o['Property tax']
            + o['Property insurance'])
        d = DC_/o['Duration'] # Depreciation
        L_ = o['Wage']*o['Employees']
        total_operating_cost = UC_ + (1+fb)*L_ + MC_ + f*FC_ + d + o['Other recurring costs']
        market_values = np.array([i.cost for i in products])
        weights = market_values/market_values.sum()
        operating_cost = weights*total_operating_cost
        return operating_cost
    
    def _get_cached_data(self):
        """Return cached data.
        
        **Return**
        
            **flow_factor:** [float] Factor to convert flow rate from kg/hr to kg/yr of operation.
            
            **cashflow_info:** tuple[array] including:
                * cashflow_data: Cash flow data table
                * duration_array: Range from 1 to the end of the project length
        
            **depreciation_data:** [tuple] including:
                * start: Index of year when operation starts
                * Depreciation: Array of depreciation as a fraction of fixed cost
                * D_len: Lenght of depreciation
                * index_startup: Year index and fixed capital investment fractions
            
        """
        # Keys for cached data
        o = self._options
        cached = self._cached
        year_duration = (o['Year'], o['Duration'])
        depreciation_schedule = (o['Depreciation'], o['Startup schedule'])
        operating_days = o['Operating days']
        
        # Get and update cached data
        flow_factor = cached.get(operating_days)
        cashflow_info = cached.get(year_duration)
        depreciation_data = cached.get(depreciation_schedule)
        if not flow_factor:
            cached[operating_days] = flow_factor = 24*operating_days
        if not cashflow_info:
            year, duration = year_duration
            index = tuple(range(year, year + duration)) if year else None
            data = np.zeros((duration, 10))
            self.cashflow = _DataFrame(data, index, _cashflow_columns, dtype=float)
            cashflow_data = _asarray(self.cashflow).transpose()
            duration_array = _array(range(duration))
            cached[year_duration] = cashflow_info = (cashflow_data, duration_array)
        if not depreciation_data:
            depreciation, schedule = depreciation_schedule
            Depreciation = _MACRS[depreciation]
            start = len(schedule)
            end = start + len(Depreciation)
            schedule = np.array(schedule)
            depreciation_data = (start,
                                 Depreciation,
                                 end,
                                 schedule)
            cached[depreciation_schedule] = depreciation_data
        
        return flow_factor, cashflow_info, depreciation_data
    
    def _calc_parameters(self, flow_factor):
        """Return elementary cash flow parameters."""
        # Cash flow parameters (USD or USD/yr)
        # DC_: Depreciable capital
        # FC_: Fixed capital
        # WC_: Working capital
        # UC_: Utility cost
        # MC_: Material cost
        # S_: Sales
        # L_: Labor cost
        # C_: Annual operating cost (excluding depreciation)
        
        system = self.system
        feeds = system.feeds
        products = system.products
        o = self.options
        DC_, UC_ = self.costs.sum(0) # Depreciable capital (USD) and utility cost (USD/hr)
        MC_ = 0 # Material cost USD/hr
        S_  = 0 # Sales USD/hr
        for s in feeds:
            price = s.price
            if price: MC_ += price*(s._mol*s._MW).sum()
        for s in products:
            price = s.price
            if price: S_ += price*(s._mol*s._MW).sum()
        # Multiply by flow_factor for USD/yr
        UC_ *= flow_factor
        MC_ *= flow_factor
        S_ *= flow_factor
        DC_ *= o['Lang factor']
        FC_ = DC_*(1 + o['Startup'] + o['Land'] + o['Royalties']) + o['Other fixed capital']
        fb = o['Fringe benefits'] + o['Supplies']
        f =  (o['Mantainance']
            + o['Administration']
            + o['Property tax']
            + o['Property insurance'])
        WC_ = o['Working capital']*FC_
        L_ = o['Wage']*o['Employees']
        C_ = UC_ + (1+fb)*L_ + MC_ + f*FC_ + o['Other recurring costs']
        return DC_, FC_, WC_, S_, C_, o['Income tax'], UC_, MC_, L_
    
    @staticmethod
    def _calc_cashflow(cashflow_data,
                       parameters,
                       depreciation_data):
        """Perform cash flow analysis and return net present value."""
        # Cash flow data and parameters
        # C_DC: Depreciable capital
        # C_FC: Fixed capital
        # C_WC: Working capital
        # D: Depreciation
        # C: Annual operating cost (excluding depreciation)
        # S: Sales
        # NE: Net earnings
        # CF: Cash flow
        # DCF: Discounted cash flow
        # CPV: Cumulative present value
        start, Depreciation, end, schedule = depreciation_data
        C_DC, D, C_FC, C_WC, C, S, NE, CF, DCF, CPV = cashflow_data
        DC_, FC_, WC_, S_, C_, tax = parameters
        
        # Calculate
        D[:] = 0.0
        C_DC[:start] = DC_*schedule
        C_FC[:start] = FC_*schedule
        D[start:end] = DC_*Depreciation
        C_WC[start] = WC_
        C_WC[-1] = -WC_
        C[start:] = C_
        S[start:] = S_
        NE[:] = (S - C - D)*(1 - tax)
        CF[:] = (NE + D) - C_FC - C_WC
    
    @staticmethod
    def _calc_NPV_and_update(IRR, CF_subset, duration_array):
        """Return NPV at given IRR and cashflow data. Update cash flow subset."""
        CF, DCF, CPV = CF_subset
        DCF[:] = CF/(1+IRR)**duration_array
        CPV[:] = DCF.cumsum()
        return CPV[-1]
    
    @staticmethod
    def _calc_NPV(IRR, CF, duration_array):
        """Return NPV at given IRR and cashflow data."""
        return (CF/(1+IRR)**duration_array).sum()
    
    def _update_results(self, parameters, NPV):
        """Update results attribute."""
        DC, FCI, WC, S, C, tax, UC, MC, L = parameters
        D = FCI/self._options['Duration']
        AOC = C + D
        TCI = FCI + WC
        net_earnings = (1-tax)*(S-AOC)
        ROI = net_earnings/TCI
        PBP = FCI/(net_earnings + D)
        
        r = self._results
        r['Depreciable capital'] = DC
        r['Fixed capital investment'] = FCI
        r['Working capital'] = WC
        r['Total capital investment'] = TCI
        r['Depreciation'] = D
        r['Utility cost'] = UC
        r['Material cost'] = MC
        r['Sales'] = S
        r['Labor'] = L
        r['Annual operating cost'] = AOC
        r['Net present value'] = NPV
        r['Return on investment'] = ROI
        r['Pay back period'] = PBP

    def solve_IRR(self, update=False):
        """Return the IRR at the break even point (NPV = 0) through cash flow analysis.
        
        **Parameters**
        
            **update:** [bool] If True, update IRR, cashflow, and results.
           
        """
        # Calculate cashflow table
        flow_factor, cashflow_info, depreciation_data = self._get_cached_data()
        cashflow_data, duration_array = cashflow_info
        parameters = self._calc_parameters(flow_factor)
        self._calc_cashflow(cashflow_data,
                            parameters[:-3],
                            depreciation_data)
        
        # Guess for solver
        guess = self._IRR_guess
        IRR_guess = guess if guess else self._options['IRR']
        
        # Solve
        if update:
            data_subset = cashflow_data[-3:]
            args = (data_subset, duration_array)
            self._calc_cashflow(cashflow_data,
                                parameters[:-3],
                                depreciation_data)
            self._IRR_guess = IRR = newton(self._calc_NPV_and_update,
                                           IRR_guess, args=args, tol=1e-5)
            self.options['IRR'] = IRR
            self._update_results(parameters, data_subset[-1, -1])
        else:
            self._IRR_guess = IRR = newton(self._calc_NPV, IRR_guess,
                                           args=(cashflow_data[-3], duration_array),
                                           tol=1e-5)
        return IRR
    
    def solve_price(self, stream, update=False):
        """Return the price (USD/kg) of stream at the break even point (NPV = 0) through cash flow analysis. 
        
        **Parameters**
        
            **stream:** [Stream] Stream with variable selling price.
            
            **update:** [bool] If True, update stream price, cashflow, and results.
            
        """
        # Calculate cashflow table
        flow_factor, cashflow_info, depreciation_data = self._get_cached_data()
        cashflow_data, duration_array = cashflow_info
        parameters = self._calc_parameters(flow_factor)
        self._calc_cashflow(cashflow_data,
                            parameters[:-3],
                            depreciation_data)
        
        # Create function that adjusts cash flow with new stream price
        start = depreciation_data[0]
        tax = parameters[-4]
        IRR = self.options['IRR']
        cost_factor = stream.massnet*flow_factor*(1-tax)
        CF = cashflow_data[-3][start:]
        CF_copy = _array(CF)
        system = self.system
        if stream in system.feeds:
            adjust = CF_copy.__sub__
        elif stream in system.products:
            adjust = CF_copy.__add__
        else:
            raise ValueError(f"Stream '{stream.ID}' must be either a feed or a product of the system")
        
        # Guess cost adjustment for solver
        guess = self._cost_guess
        cost_guess = 0 if guess is None else guess
        
        # Solve
        if update:
            calc_NPV = self._calc_NPV_and_update
            data_subset = cashflow_data[-3:]
            def break_even_point(cost):
                CF[:] = adjust(cost)
                return calc_NPV(IRR, data_subset, duration_array)
            self._cost_guess = cost = newton(break_even_point, cost_guess)
            stream.price += cost/cost_factor
            price = stream.price
            parameters = self._calc_parameters(flow_factor)
            self._calc_cashflow(cashflow_data,
                                parameters[:-3],
                                depreciation_data)
            self._update_results(parameters, data_subset[-1, -1])
        else:
            calc_NPV = self._calc_NPV
            data_subset = cashflow_data[-3]
            def break_even_point(cost):
                CF[:] = adjust(cost)
                return calc_NPV(IRR, data_subset, duration_array)
            self._cost_guess = cost = newton(break_even_point, cost_guess)
            price = stream.price + cost/cost_factor
        
        return price
    
    def __repr__(self):
        return f'<{type(self).__name__}: {self.system.ID}>'
    
    def _info(self):
        r = self._results
        out = f'{type(self).__name__}: {self.system.ID}\n'
        IRR = self.options['IRR']*100
        if r:
            NPV = r['Net present value']
            ROI = r['Return on investment']
            PBP = r['Pay back period']
            out += f' NPV: {NPV:.3g} USD at {IRR:.1f}% IRR\n'
            out += f' ROI: {ROI:.3g} 1/yr\n'
            out += f' PBP: {PBP:.3g} yr' 
        else:
            out += f' NPV: None\n'
            out += f' ROI: None\n'
            out += f' PBP: None'
        return out
    
    def show(self):
        """Print information on TEA."""
        print(self._info())
        
        
        
    