"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from enum import Enum
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class LiquidityMeasure(EnumBase, Enum):    
    
    """A list of the different liquidity measures to choose from."""

    Summary = 'Summary'
    Constituents = 'Constituents'
    Largest_Holdings_By_Weight = 'Largest Holdings By Weight'
    Least_Liquid_Holdings = 'Least Liquid Holdings'
    ADV_Percent_Buckets = 'ADV Percent Buckets'
    Market_Cap_Buckets = 'Market Cap Buckets'
    Region_Buckets = 'Region Buckets'
    Country_Buckets = 'Country Buckets'
    Sector_Buckets = 'Sector Buckets'
    Industry_Buckets = 'Industry Buckets'
    Risk_Buckets = 'Risk Buckets'
    Factor_Risk_Buckets = 'Factor Risk Buckets'
    Exposure_Buckets = 'Exposure Buckets'
    Factor_Exposure_Buckets = 'Factor Exposure Buckets'
    Percent_Of_Trade_Complete_Over_Time = 'Percent Of Trade Complete Over Time'
    Execution_Cost_With_Different_Time_Horizons = 'Execution Cost With Different Time Horizons'
    Participation_Rate_With_Different_Time_Horizons = 'Participation Rate With Different Time Horizons'
    Risk_With_Different_Time_Horizons = 'Risk With Different Time Horizons'
    Historical_ADV_Percent_Curve = 'Historical ADV Percent Curve'
    Time_Series_Data = 'Time Series Data'
    
    def __repr__(self):
        return self.value


class MarketDataShockType(EnumBase, Enum):    
    
    """Market data shock type"""

    Absolute = 'Absolute'
    Proportional = 'Proportional'
    Invalid = 'Invalid'
    Override = 'Override'
    StdDev = 'StdDev'
    AutoDefault = 'AutoDefault'
    CSWFFR = 'CSWFFR'
    StdVolFactor = 'StdVolFactor'
    StdVolFactorProportional = 'StdVolFactorProportional'
    
    def __repr__(self):
        return self.value


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Delta = 'Delta'
    DeltaLocalCcy = 'DeltaLocalCcy'
    Dollar_Price = 'Dollar Price'
    Forward_Price = 'Forward Price'
    Price = 'Price'
    DV01 = 'DV01'
    Gamma = 'Gamma'
    OAS = 'OAS'
    PNL = 'PNL'
    PV = 'PV'
    Spot = 'Spot'
    Theta = 'Theta'
    Vanna = 'Vanna'
    Vega = 'Vega'
    VegaLocalCcy = 'VegaLocalCcy'
    Volga = 'Volga'
    Annual_Implied_Volatility = 'Annual Implied Volatility'
    Annual_ATMF_Implied_Volatility = 'Annual ATMF Implied Volatility'
    Daily_Implied_Volatility = 'Daily Implied Volatility'
    Resolved_Instrument_Values = 'Resolved Instrument Values'
    
    def __repr__(self):
        return self.value


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    
    def __repr__(self):
        return self.value


class RiskModel(EnumBase, Enum):    
    
    """Axioma risk model identifier."""

    AXUS2M = 'AXUS2M'
    AXWW21M = 'AXWW21M'
    AXUS3M = 'AXUS3M'
    AXUS3MMACRO = 'AXUS3MMACRO'
    AXUS4M = 'AXUS4M'
    AXUS4S = 'AXUS4S'
    AXEU21M = 'AXEU21M'
    STSWWFR = 'STSWWFR'
    AXWW21S = 'AXWW21S'
    AXCNM = 'AXCNM'
    AXEM21M = 'AXEM21M'
    AXJP2M = 'AXJP2M'
    AXAPxJP21M = 'AXAPxJP21M'
    AXAP21M = 'AXAP21M'
    AXAP21S = 'AXAP21S'
    AXAU4M = 'AXAU4M'
    AXJP4M = 'AXJP4M'
    AXTWM = 'AXTWM'
    
    def __repr__(self):
        return self.value


class SortByTerm(EnumBase, Enum):    
    
    """Term to sort risk models by."""

    Short = 'Short'
    Medium = 'Medium'
    
    def __repr__(self):
        return self.value


class AdvCurveTick(Base):
               
    def __init__(self, date: datetime.date = None, value: float = None):
        super().__init__()
        self.__date = date
        self.__value = value

    @property
    def date(self) -> datetime.date:
        """Date of the tick in ISO 8601 format."""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value
        self._property_changed('date')        

    @property
    def value(self) -> float:
        """Value of the advPct."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class CoordinatesRequest(Base):
               
    def __init__(self, asOf: datetime.date, instruments: Tuple[Priceable, ...]):
        super().__init__()
        self.__asOf = asOf
        self.__instruments = instruments

    @property
    def asOf(self) -> datetime.date:
        return self.__asOf

    @asOf.setter
    def asOf(self, value: datetime.date):
        self.__asOf = value
        self._property_changed('asOf')        

    @property
    def instruments(self) -> Tuple[Priceable, ...]:
        return self.__instruments

    @instruments.setter
    def instruments(self, value: Tuple[Priceable, ...]):
        self.__instruments = value
        self._property_changed('instruments')        


class CoordinatesResponse(Base):
               
    def __init__(self, results: Tuple[MarketDataCoordinate, ...]):
        super().__init__()
        self.__results = results

    @property
    def results(self) -> Tuple[MarketDataCoordinate, ...]:
        return self.__results

    @results.setter
    def results(self, value: Tuple[MarketDataCoordinate, ...]):
        self.__results = value
        self._property_changed('results')        


class CurveScenario(Base):
        
    """A scenario to manipulate curve shape"""
       
    def __init__(self, marketDataAssets: Tuple[str, ...] = None, annualisedParallelShiftSize: float = None, annualisedSlopeShiftSize: float = None, pivotPoint: float = None, cutoff: float = None):
        super().__init__()
        self.__marketDataAssets = marketDataAssets
        self.__annualisedParallelShiftSize = annualisedParallelShiftSize
        self.__annualisedSlopeShiftSize = annualisedSlopeShiftSize
        self.__pivotPoint = pivotPoint
        self.__cutoff = cutoff

    @property
    def scenarioType(self) -> str:
        """CurveScenario"""
        return 'CurveScenario'        

    @property
    def marketDataAssets(self) -> Tuple[str, ...]:
        """Assets (currencies, indices etc) to which this scenario applies"""
        return self.__marketDataAssets

    @marketDataAssets.setter
    def marketDataAssets(self, value: Tuple[str, ...]):
        self.__marketDataAssets = value
        self._property_changed('marketDataAssets')        

    @property
    def annualisedParallelShiftSize(self) -> float:
        """Size of the parallel shift (in bps)"""
        return self.__annualisedParallelShiftSize

    @annualisedParallelShiftSize.setter
    def annualisedParallelShiftSize(self, value: float):
        self.__annualisedParallelShiftSize = value
        self._property_changed('annualisedParallelShiftSize')        

    @property
    def annualisedSlopeShiftSize(self) -> float:
        """Size of the slope shift (in bps)"""
        return self.__annualisedSlopeShiftSize

    @annualisedSlopeShiftSize.setter
    def annualisedSlopeShiftSize(self, value: float):
        self.__annualisedSlopeShiftSize = value
        self._property_changed('annualisedSlopeShiftSize')        

    @property
    def pivotPoint(self) -> float:
        """Pivot point"""
        return self.__pivotPoint

    @pivotPoint.setter
    def pivotPoint(self, value: float):
        self.__pivotPoint = value
        self._property_changed('pivotPoint')        

    @property
    def cutoff(self) -> float:
        """The cutoff point (in years)"""
        return self.__cutoff

    @cutoff.setter
    def cutoff(self, value: float):
        self.__cutoff = value
        self._property_changed('cutoff')        


class ExecutionCostForHorizon(Base):
               
    def __init__(self, minutesExpired: int = None, executionCost: float = None, executionCostLong: float = None, executionCostShort: float = None):
        super().__init__()
        self.__minutesExpired = minutesExpired
        self.__executionCost = executionCost
        self.__executionCostLong = executionCostLong
        self.__executionCostShort = executionCostShort

    @property
    def minutesExpired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutesExpired

    @minutesExpired.setter
    def minutesExpired(self, value: int):
        self.__minutesExpired = value
        self._property_changed('minutesExpired')        

    @property
    def executionCost(self) -> float:
        """Estimated transaction cost for the set of positions."""
        return self.__executionCost

    @executionCost.setter
    def executionCost(self, value: float):
        self.__executionCost = value
        self._property_changed('executionCost')        

    @property
    def executionCostLong(self) -> float:
        """Estimated transaction cost for the set of long positions."""
        return self.__executionCostLong

    @executionCostLong.setter
    def executionCostLong(self, value: float):
        self.__executionCostLong = value
        self._property_changed('executionCostLong')        

    @property
    def executionCostShort(self) -> float:
        """Estimated transaction cost for the set of short positions."""
        return self.__executionCostShort

    @executionCostShort.setter
    def executionCostShort(self, value: float):
        self.__executionCostShort = value
        self._property_changed('executionCostShort')        


class LiquidityBucket(Base):
        
    """Positions bucketed by a certain characteristic."""
       
    def __init__(self, name: str = None, description: str = None, netExposure: float = None, grossExposure: float = None, netWeight: float = None, grossWeight: float = None, transactionCost: float = None, marginalCost: float = None, adv22DayPct: float = None, numberOfPositions: float = None, betaAdjustedExposure: float = None, longWeight: float = None, longExposure: float = None, longTransactionCost: float = None, longMarginalCost: float = None, longAdv22DayPct: float = None, longNumberOfPositions: float = None, longBetaAdjustedExposure: float = None, shortWeight: float = None, shortExposure: float = None, shortTransactionCost: float = None, shortMarginalCost: float = None, shortAdv22DayPct: float = None, shortNumberOfPositions: float = None, shortBetaAdjustedExposure: float = None):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__netExposure = netExposure
        self.__grossExposure = grossExposure
        self.__netWeight = netWeight
        self.__grossWeight = grossWeight
        self.__transactionCost = transactionCost
        self.__marginalCost = marginalCost
        self.__adv22DayPct = adv22DayPct
        self.__numberOfPositions = numberOfPositions
        self.__betaAdjustedExposure = betaAdjustedExposure
        self.__longWeight = longWeight
        self.__longExposure = longExposure
        self.__longTransactionCost = longTransactionCost
        self.__longMarginalCost = longMarginalCost
        self.__longAdv22DayPct = longAdv22DayPct
        self.__longNumberOfPositions = longNumberOfPositions
        self.__longBetaAdjustedExposure = longBetaAdjustedExposure
        self.__shortWeight = shortWeight
        self.__shortExposure = shortExposure
        self.__shortTransactionCost = shortTransactionCost
        self.__shortMarginalCost = shortMarginalCost
        self.__shortAdv22DayPct = shortAdv22DayPct
        self.__shortNumberOfPositions = shortNumberOfPositions
        self.__shortBetaAdjustedExposure = shortBetaAdjustedExposure

    @property
    def name(self) -> str:
        """Name of the bucket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def description(self) -> str:
        """A description of the bucket."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def netExposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: float):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def grossExposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: float):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def netWeight(self) -> float:
        """Net weight of the constituent."""
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value: float):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def grossWeight(self) -> float:
        """Gross weight of the constituent."""
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value: float):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def transactionCost(self) -> float:
        """The average estimated transaction cost for the positions in the bucket."""
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: float):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def marginalCost(self) -> float:
        """The average estimated transaction cost of the positions in this bucket multiplied by the bucket's gross weight in the portfolio."""
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: float):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def adv22DayPct(self) -> float:
        """The average 22 day ADV percent of the positions in the bucket."""
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value: float):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def numberOfPositions(self) -> float:
        """Number of positions in the bucket."""
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value: float):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def betaAdjustedExposure(self) -> float:
        """Net exposure of the positions in the bucket adjusted by the beta."""
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value: float):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def longWeight(self) -> float:
        """Gross weight of the long positions in the bucket."""
        return self.__longWeight

    @longWeight.setter
    def longWeight(self, value: float):
        self.__longWeight = value
        self._property_changed('longWeight')        

    @property
    def longExposure(self) -> float:
        """Long exposure of the positions in the bucket."""
        return self.__longExposure

    @longExposure.setter
    def longExposure(self, value: float):
        self.__longExposure = value
        self._property_changed('longExposure')        

    @property
    def longTransactionCost(self) -> float:
        """The average estimated transaction cost of the long positions in the bucket."""
        return self.__longTransactionCost

    @longTransactionCost.setter
    def longTransactionCost(self, value: float):
        self.__longTransactionCost = value
        self._property_changed('longTransactionCost')        

    @property
    def longMarginalCost(self) -> float:
        """The estimated transaction cost of the long positions in this bucket multiplied by the sum of these positions' normalized weight with respect to all long positions in the portfolio."""
        return self.__longMarginalCost

    @longMarginalCost.setter
    def longMarginalCost(self, value: float):
        self.__longMarginalCost = value
        self._property_changed('longMarginalCost')        

    @property
    def longAdv22DayPct(self) -> float:
        """The average 22 day ADV percent of the long positions in the bucket."""
        return self.__longAdv22DayPct

    @longAdv22DayPct.setter
    def longAdv22DayPct(self, value: float):
        self.__longAdv22DayPct = value
        self._property_changed('longAdv22DayPct')        

    @property
    def longNumberOfPositions(self) -> float:
        """Number of long positions in the bucket."""
        return self.__longNumberOfPositions

    @longNumberOfPositions.setter
    def longNumberOfPositions(self, value: float):
        self.__longNumberOfPositions = value
        self._property_changed('longNumberOfPositions')        

    @property
    def longBetaAdjustedExposure(self) -> float:
        """Long exposure of the positions in the bucket adjusted by the beta."""
        return self.__longBetaAdjustedExposure

    @longBetaAdjustedExposure.setter
    def longBetaAdjustedExposure(self, value: float):
        self.__longBetaAdjustedExposure = value
        self._property_changed('longBetaAdjustedExposure')        

    @property
    def shortWeight(self) -> float:
        """Gross weight of the short positions in the bucket."""
        return self.__shortWeight

    @shortWeight.setter
    def shortWeight(self, value: float):
        self.__shortWeight = value
        self._property_changed('shortWeight')        

    @property
    def shortExposure(self) -> float:
        """Short exposure of the positions in the bucket."""
        return self.__shortExposure

    @shortExposure.setter
    def shortExposure(self, value: float):
        self.__shortExposure = value
        self._property_changed('shortExposure')        

    @property
    def shortTransactionCost(self) -> float:
        """The average estimated transaction cost of the long positions in the bucket."""
        return self.__shortTransactionCost

    @shortTransactionCost.setter
    def shortTransactionCost(self, value: float):
        self.__shortTransactionCost = value
        self._property_changed('shortTransactionCost')        

    @property
    def shortMarginalCost(self) -> float:
        """The estimated transaction cost of the short positions in this bucket multiplied by the sum of these positions' normalized weight with respect to all short positions in the portfolio."""
        return self.__shortMarginalCost

    @shortMarginalCost.setter
    def shortMarginalCost(self, value: float):
        self.__shortMarginalCost = value
        self._property_changed('shortMarginalCost')        

    @property
    def shortAdv22DayPct(self) -> float:
        """The average 22 day ADV percent of the short positions in the bucket."""
        return self.__shortAdv22DayPct

    @shortAdv22DayPct.setter
    def shortAdv22DayPct(self, value: float):
        self.__shortAdv22DayPct = value
        self._property_changed('shortAdv22DayPct')        

    @property
    def shortNumberOfPositions(self) -> float:
        """Number of short positions in the bucket."""
        return self.__shortNumberOfPositions

    @shortNumberOfPositions.setter
    def shortNumberOfPositions(self, value: float):
        self.__shortNumberOfPositions = value
        self._property_changed('shortNumberOfPositions')        

    @property
    def shortBetaAdjustedExposure(self) -> float:
        """Short exposure of the positions in the bucket adjusted by the beta."""
        return self.__shortBetaAdjustedExposure

    @shortBetaAdjustedExposure.setter
    def shortBetaAdjustedExposure(self, value: float):
        self.__shortBetaAdjustedExposure = value
        self._property_changed('shortBetaAdjustedExposure')        


class LiquidityConstituent(Base):
        
    """A constituent of the portfolio enriched with liquidity and estimated transaction cost information."""
       
    def __init__(self, assetId: str = None, name: str = None, exchange: str = None, quantity: float = None, grossWeight: float = None, netWeight: float = None, currency: Union[Currency, str] = None, grossExposure: float = None, netExposure: float = None, adv22DayPct: float = None, transactionCost: float = None, marginalCost: float = None, bidAskSpread: float = None, country: str = None, region: Union[Region, str] = None, type: Union[AssetType, str] = None, marketCap: float = None, marketCapUSD: float = None, est1DayCompletePct: float = None, inRiskModel: bool = None, inCostPredictModel: bool = None, beta: float = None, dailyRisk: float = None, annualizedRisk: float = None, oneDayPriceChangePct: float = None, betaAdjustedExposure: float = None, advBucket=None, settlementDate: datetime.date = None):
        super().__init__()
        self.__assetId = assetId
        self.__name = name
        self.__exchange = exchange
        self.__quantity = quantity
        self.__grossWeight = grossWeight
        self.__netWeight = netWeight
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__grossExposure = grossExposure
        self.__netExposure = netExposure
        self.__adv22DayPct = adv22DayPct
        self.__transactionCost = transactionCost
        self.__marginalCost = marginalCost
        self.__bidAskSpread = bidAskSpread
        self.__country = country
        self.__region = region if isinstance(region, Region) else get_enum_value(Region, region)
        self.__type = type if isinstance(type, AssetType) else get_enum_value(AssetType, type)
        self.__marketCap = marketCap
        self.__marketCapUSD = marketCapUSD
        self.__est1DayCompletePct = est1DayCompletePct
        self.__inRiskModel = inRiskModel
        self.__inCostPredictModel = inCostPredictModel
        self.__beta = beta
        self.__dailyRisk = dailyRisk
        self.__annualizedRisk = annualizedRisk
        self.__oneDayPriceChangePct = oneDayPriceChangePct
        self.__betaAdjustedExposure = betaAdjustedExposure
        self.__advBucket = advBucket
        self.__settlementDate = settlementDate

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def quantity(self) -> float:
        """The quantity of shares."""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def grossWeight(self) -> float:
        """Gross weight of the constituent."""
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value: float):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def netWeight(self) -> float:
        """Net weight of the constituent."""
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value: float):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def grossExposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: float):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def netExposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: float):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def adv22DayPct(self) -> float:
        """Percentage of the constituent's notional to it's 22 day average daily dollar volume."""
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value: float):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def transactionCost(self) -> float:
        """The estimated transaction cost for the position."""
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: float):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def marginalCost(self) -> float:
        """The estimated transaction cost multiplied by the position's gross weight in the portfolio."""
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: float):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def bidAskSpread(self) -> float:
        """The difference between the bid and ask prices for this asset."""
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value: float):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def country(self) -> str:
        """Country name of asset."""
        return self.__country

    @country.setter
    def country(self, value: str):
        self.__country = value
        self._property_changed('country')        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self.__region = value if isinstance(value, Region) else get_enum_value(Region, value)
        self._property_changed('region')        

    @property
    def type(self) -> Union[AssetType, str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetType, str]):
        self.__type = value if isinstance(value, AssetType) else get_enum_value(AssetType, value)
        self._property_changed('type')        

    @property
    def marketCap(self) -> float:
        """Market capitalization of a given asset denominated in the currency given in the liquidity parameters."""
        return self.__marketCap

    @marketCap.setter
    def marketCap(self, value: float):
        self.__marketCap = value
        self._property_changed('marketCap')        

    @property
    def marketCapUSD(self) -> float:
        """Market capitalization of a given asset denominated in USD."""
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value: float):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def est1DayCompletePct(self) -> float:
        """Estimated percentage of the position traded in one day."""
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value: float):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def inRiskModel(self) -> bool:
        """Whether or not the asset is in the risk model universe."""
        return self.__inRiskModel

    @inRiskModel.setter
    def inRiskModel(self, value: bool):
        self.__inRiskModel = value
        self._property_changed('inRiskModel')        

    @property
    def inCostPredictModel(self) -> bool:
        """Whether or not the asset is in the cost prediction model universe."""
        return self.__inCostPredictModel

    @inCostPredictModel.setter
    def inCostPredictModel(self, value: bool):
        self.__inCostPredictModel = value
        self._property_changed('inCostPredictModel')        

    @property
    def beta(self) -> float:
        """Beta of the constituent with respect to the risk model universe."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def dailyRisk(self) -> float:
        """Daily risk of the position in bps."""
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value: float):
        self.__dailyRisk = value
        self._property_changed('dailyRisk')        

    @property
    def annualizedRisk(self) -> float:
        """Annualized risk of the position in bps."""
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value: float):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def oneDayPriceChangePct(self) -> float:
        """One day percentage change in price."""
        return self.__oneDayPriceChangePct

    @oneDayPriceChangePct.setter
    def oneDayPriceChangePct(self, value: float):
        self.__oneDayPriceChangePct = value
        self._property_changed('oneDayPriceChangePct')        

    @property
    def betaAdjustedExposure(self) -> float:
        """Beta adjusted exposure."""
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value: float):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def advBucket(self):
        """Category based off of the position's notional with respect to it's ADV."""
        return self.__advBucket

    @advBucket.setter
    def advBucket(self, value):
        self.__advBucket = value
        self._property_changed('advBucket')        

    @property
    def settlementDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: datetime.date):
        self.__settlementDate = value
        self._property_changed('settlementDate')        


class LiquidityFactor(Base):
               
    def __init__(self, name: str = None, value: float = None):
        super().__init__()
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        """Name of the factor."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def value(self) -> float:
        """Value of the factor."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class LiquiditySummarySection(Base):
        
    """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
       
    def __init__(self, adv10DayPct=None, adv22DayPct=None, adv5DayPct: float = None, annualizedRisk: float = None, annualizedTrackingError: float = None, beta: float = None, betaAdjustedExposure=None, betaAdjustedNetExposure=None, bidAskSpread: float = None, correlation: float = None, dailyRisk: float = None, dailyTrackingError: float = None, est1DayCompletePct=None, fiveDayPriceChangeBps=None, grossExposure: float = None, marginalCost: float = None, marketCapUSD: float = None, minutesToTrade100Pct: float = None, netExposure: float = None, numberOfPositions=None, transactionCost: float = None):
        super().__init__()
        self.__adv10DayPct = adv10DayPct
        self.__adv22DayPct = adv22DayPct
        self.__adv5DayPct = adv5DayPct
        self.__annualizedRisk = annualizedRisk
        self.__annualizedTrackingError = annualizedTrackingError
        self.__beta = beta
        self.__betaAdjustedExposure = betaAdjustedExposure
        self.__betaAdjustedNetExposure = betaAdjustedNetExposure
        self.__bidAskSpread = bidAskSpread
        self.__correlation = correlation
        self.__dailyRisk = dailyRisk
        self.__dailyTrackingError = dailyTrackingError
        self.__est1DayCompletePct = est1DayCompletePct
        self.__fiveDayPriceChangeBps = fiveDayPriceChangeBps
        self.__grossExposure = grossExposure
        self.__marginalCost = marginalCost
        self.__marketCapUSD = marketCapUSD
        self.__minutesToTrade100Pct = minutesToTrade100Pct
        self.__netExposure = netExposure
        self.__numberOfPositions = numberOfPositions
        self.__transactionCost = transactionCost

    @property
    def adv10DayPct(self):
        return self.__adv10DayPct

    @adv10DayPct.setter
    def adv10DayPct(self, value):
        self.__adv10DayPct = value
        self._property_changed('adv10DayPct')        

    @property
    def adv22DayPct(self):
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def adv5DayPct(self) -> float:
        return self.__adv5DayPct

    @adv5DayPct.setter
    def adv5DayPct(self, value: float):
        self.__adv5DayPct = value
        self._property_changed('adv5DayPct')        

    @property
    def annualizedRisk(self) -> float:
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value: float):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def annualizedTrackingError(self) -> float:
        return self.__annualizedTrackingError

    @annualizedTrackingError.setter
    def annualizedTrackingError(self, value: float):
        self.__annualizedTrackingError = value
        self._property_changed('annualizedTrackingError')        

    @property
    def beta(self) -> float:
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def betaAdjustedExposure(self):
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def betaAdjustedNetExposure(self):
        return self.__betaAdjustedNetExposure

    @betaAdjustedNetExposure.setter
    def betaAdjustedNetExposure(self, value):
        self.__betaAdjustedNetExposure = value
        self._property_changed('betaAdjustedNetExposure')        

    @property
    def bidAskSpread(self) -> float:
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value: float):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def correlation(self) -> float:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def dailyRisk(self) -> float:
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value: float):
        self.__dailyRisk = value
        self._property_changed('dailyRisk')        

    @property
    def dailyTrackingError(self) -> float:
        return self.__dailyTrackingError

    @dailyTrackingError.setter
    def dailyTrackingError(self, value: float):
        self.__dailyTrackingError = value
        self._property_changed('dailyTrackingError')        

    @property
    def est1DayCompletePct(self):
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def fiveDayPriceChangeBps(self):
        return self.__fiveDayPriceChangeBps

    @fiveDayPriceChangeBps.setter
    def fiveDayPriceChangeBps(self, value):
        self.__fiveDayPriceChangeBps = value
        self._property_changed('fiveDayPriceChangeBps')        

    @property
    def grossExposure(self) -> float:
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: float):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def marginalCost(self) -> float:
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: float):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def marketCapUSD(self) -> float:
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value: float):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def minutesToTrade100Pct(self) -> float:
        return self.__minutesToTrade100Pct

    @minutesToTrade100Pct.setter
    def minutesToTrade100Pct(self, value: float):
        self.__minutesToTrade100Pct = value
        self._property_changed('minutesToTrade100Pct')        

    @property
    def netExposure(self) -> float:
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: float):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def numberOfPositions(self):
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def transactionCost(self) -> float:
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: float):
        self.__transactionCost = value
        self._property_changed('transactionCost')        


class LiquidityTableRow(Base):
               
    def __init__(self, assetId: str = None, name: str = None, adv22DayPct: float = None, shares: float = None, netWeight: float = None, grossWeight: float = None, grossExposure: float = None, netExposure: float = None, transactionCost: float = None, marginalCost: float = None, oneDayPriceChangePct: float = None, normalizedPerformance: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None):
        super().__init__()
        self.__assetId = assetId
        self.__name = name
        self.__adv22DayPct = adv22DayPct
        self.__shares = shares
        self.__netWeight = netWeight
        self.__grossWeight = grossWeight
        self.__grossExposure = grossExposure
        self.__netExposure = netExposure
        self.__transactionCost = transactionCost
        self.__marginalCost = marginalCost
        self.__oneDayPriceChangePct = oneDayPriceChangePct
        self.__normalizedPerformance = normalizedPerformance

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def adv22DayPct(self) -> float:
        """Percentage of the constituent's notional to it's 22 day average daily dollar volume."""
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value: float):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def shares(self) -> float:
        """The quantity of shares."""
        return self.__shares

    @shares.setter
    def shares(self, value: float):
        self.__shares = value
        self._property_changed('shares')        

    @property
    def netWeight(self) -> float:
        """Net weight of the constituent."""
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value: float):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def grossWeight(self) -> float:
        """Gross weight of the constituent."""
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value: float):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def grossExposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: float):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def netExposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: float):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def transactionCost(self) -> float:
        """The estimated transaction cost for the position."""
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: float):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def marginalCost(self) -> float:
        """The estimated transaction cost multiplied by the position's gross weight in the portfolio."""
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: float):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def oneDayPriceChangePct(self) -> float:
        """One day percentage change in price."""
        return self.__oneDayPriceChangePct

    @oneDayPriceChangePct.setter
    def oneDayPriceChangePct(self, value: float):
        self.__oneDayPriceChangePct = value
        self._property_changed('oneDayPriceChangePct')        

    @property
    def normalizedPerformance(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of normalized performance."""
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        


class LiquidityTimeSeriesItem(Base):
               
    def __init__(self, name: str = None, normalizedPerformance: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, annualizedReturn: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, annualizedVolatility: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, annualizedSharpRatio: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, maxDrawdown: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, netExposure: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None, cumulativePnl: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None):
        super().__init__()
        self.__name = name
        self.__normalizedPerformance = normalizedPerformance
        self.__annualizedReturn = annualizedReturn
        self.__annualizedVolatility = annualizedVolatility
        self.__annualizedSharpRatio = annualizedSharpRatio
        self.__maxDrawdown = maxDrawdown
        self.__netExposure = netExposure
        self.__cumulativePnl = cumulativePnl

    @property
    def name(self) -> str:
        """Name of the time series item."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def normalizedPerformance(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of normalized performance."""
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        

    @property
    def annualizedReturn(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized return."""
        return self.__annualizedReturn

    @annualizedReturn.setter
    def annualizedReturn(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualizedReturn = value
        self._property_changed('annualizedReturn')        

    @property
    def annualizedVolatility(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized volatility."""
        return self.__annualizedVolatility

    @annualizedVolatility.setter
    def annualizedVolatility(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualizedVolatility = value
        self._property_changed('annualizedVolatility')        

    @property
    def annualizedSharpRatio(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized sharp ratio."""
        return self.__annualizedSharpRatio

    @annualizedSharpRatio.setter
    def annualizedSharpRatio(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualizedSharpRatio = value
        self._property_changed('annualizedSharpRatio')        

    @property
    def maxDrawdown(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of max drawdown."""
        return self.__maxDrawdown

    @maxDrawdown.setter
    def maxDrawdown(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__maxDrawdown = value
        self._property_changed('maxDrawdown')        

    @property
    def netExposure(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of net exposure."""
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def cumulativePnl(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of cumulative PnL."""
        return self.__cumulativePnl

    @cumulativePnl.setter
    def cumulativePnl(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__cumulativePnl = value
        self._property_changed('cumulativePnl')        


class MarketDataPattern(Base):
        
    """A pattern used to match market coordinates"""
       
    def __init__(self, marketDataType: str = None, marketDataAsset: str = None, pointClass: str = None, marketDataPoint: Tuple[str, ...] = None, quotingStyle: str = None, isActive: bool = None, isInvestmentGrade: bool = None, currency: Union[Currency, str] = None, countryCode: Union[CountryCode, str] = None, gicsSector: str = None, gicsIndustryGroup: str = None, gicsIndustry: str = None, gicsSubIndustry: str = None):
        super().__init__()
        self.__marketDataType = marketDataType
        self.__marketDataAsset = marketDataAsset
        self.__pointClass = pointClass
        self.__marketDataPoint = marketDataPoint
        self.__quotingStyle = quotingStyle
        self.__isActive = isActive
        self.__isInvestmentGrade = isInvestmentGrade
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__countryCode = countryCode if isinstance(countryCode, CountryCode) else get_enum_value(CountryCode, countryCode)
        self.__gicsSector = gicsSector
        self.__gicsIndustryGroup = gicsIndustryGroup
        self.__gicsIndustry = gicsIndustry
        self.__gicsSubIndustry = gicsSubIndustry

    @property
    def marketDataType(self) -> str:
        """The Market Data Type, e.g. IR, IR_BASIS, FX, FX_Vol"""
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value: str):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def marketDataAsset(self) -> str:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value: str):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def pointClass(self) -> str:
        """The market data pointClass, e.g. Swap, Cash."""
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value: str):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def marketDataPoint(self) -> Tuple[str, ...]:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: Tuple[str, ...]):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def quotingStyle(self) -> str:
        return self.__quotingStyle

    @quotingStyle.setter
    def quotingStyle(self, value: str):
        self.__quotingStyle = value
        self._property_changed('quotingStyle')        

    @property
    def isActive(self) -> bool:
        """Is the asset active"""
        return self.__isActive

    @isActive.setter
    def isActive(self, value: bool):
        self.__isActive = value
        self._property_changed('isActive')        

    @property
    def isInvestmentGrade(self) -> bool:
        """Is the asset investment grade"""
        return self.__isInvestmentGrade

    @isInvestmentGrade.setter
    def isInvestmentGrade(self, value: bool):
        self.__isInvestmentGrade = value
        self._property_changed('isInvestmentGrade')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def countryCode(self) -> Union[CountryCode, str]:
        """ISO Country code"""
        return self.__countryCode

    @countryCode.setter
    def countryCode(self, value: Union[CountryCode, str]):
        self.__countryCode = value if isinstance(value, CountryCode) else get_enum_value(CountryCode, value)
        self._property_changed('countryCode')        

    @property
    def gicsSector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gicsSector

    @gicsSector.setter
    def gicsSector(self, value: str):
        self.__gicsSector = value
        self._property_changed('gicsSector')        

    @property
    def gicsIndustryGroup(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gicsIndustryGroup

    @gicsIndustryGroup.setter
    def gicsIndustryGroup(self, value: str):
        self.__gicsIndustryGroup = value
        self._property_changed('gicsIndustryGroup')        

    @property
    def gicsIndustry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gicsIndustry

    @gicsIndustry.setter
    def gicsIndustry(self, value: str):
        self.__gicsIndustry = value
        self._property_changed('gicsIndustry')        

    @property
    def gicsSubIndustry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gicsSubIndustry

    @gicsSubIndustry.setter
    def gicsSubIndustry(self, value: str):
        self.__gicsSubIndustry = value
        self._property_changed('gicsSubIndustry')        


class PRateForHorizon(Base):
               
    def __init__(self, minutesExpired: int = None, participationRate: float = None, participationRateLong: float = None, participationRateShort: float = None):
        super().__init__()
        self.__minutesExpired = minutesExpired
        self.__participationRate = participationRate
        self.__participationRateLong = participationRateLong
        self.__participationRateShort = participationRateShort

    @property
    def minutesExpired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutesExpired

    @minutesExpired.setter
    def minutesExpired(self, value: int):
        self.__minutesExpired = value
        self._property_changed('minutesExpired')        

    @property
    def participationRate(self) -> float:
        """Estimated participation rate needed to trade the set of positions."""
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value: float):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def participationRateLong(self) -> float:
        """Estimated participation rate needed to trade the set of long positions."""
        return self.__participationRateLong

    @participationRateLong.setter
    def participationRateLong(self, value: float):
        self.__participationRateLong = value
        self._property_changed('participationRateLong')        

    @property
    def participationRateShort(self) -> float:
        """Estimated participation rate needed to trade the set of short positions."""
        return self.__participationRateShort

    @participationRateShort.setter
    def participationRateShort(self, value: float):
        self.__participationRateShort = value
        self._property_changed('participationRateShort')        


class PricingDateAndMarketDataAsOf(Base):
        
    """Pricing date and market data as of (date or time)"""
       
    def __init__(self, pricingDate: datetime.date, marketDataAsOf: Union[datetime.date, datetime.datetime]):
        super().__init__()
        self.__pricingDate = pricingDate
        self.__marketDataAsOf = marketDataAsOf

    @property
    def pricingDate(self) -> datetime.date:
        """The date for which to perform the calculation"""
        return self.__pricingDate

    @pricingDate.setter
    def pricingDate(self, value: datetime.date):
        self.__pricingDate = value
        self._property_changed('pricingDate')        

    @property
    def marketDataAsOf(self) -> Union[datetime.date, datetime.datetime]:
        """The date or time to source market data"""
        return self.__marketDataAsOf

    @marketDataAsOf.setter
    def marketDataAsOf(self, value: Union[datetime.date, datetime.datetime]):
        self.__marketDataAsOf = value
        self._property_changed('marketDataAsOf')        


class RiskAtHorizon(Base):
               
    def __init__(self, minutesExpired: int = None, risk: int = None, riskLong: float = None, riskShort: float = None):
        super().__init__()
        self.__minutesExpired = minutesExpired
        self.__risk = risk
        self.__riskLong = riskLong
        self.__riskShort = riskShort

    @property
    def minutesExpired(self) -> int:
        """Exchange minutes expired since the start of trading."""
        return self.__minutesExpired

    @minutesExpired.setter
    def minutesExpired(self, value: int):
        self.__minutesExpired = value
        self._property_changed('minutesExpired')        

    @property
    def risk(self) -> int:
        """Risk of the portfolio in bps."""
        return self.__risk

    @risk.setter
    def risk(self, value: int):
        self.__risk = value
        self._property_changed('risk')        

    @property
    def riskLong(self) -> float:
        """Risk of the long positions in bps."""
        return self.__riskLong

    @riskLong.setter
    def riskLong(self, value: float):
        self.__riskLong = value
        self._property_changed('riskLong')        

    @property
    def riskShort(self) -> float:
        """Risk of the short positions in bps."""
        return self.__riskShort

    @riskShort.setter
    def riskShort(self, value: float):
        self.__riskShort = value
        self._property_changed('riskShort')        


class RiskPosition(Base):
               
    def __init__(self, instrument: Priceable, quantity: float):
        super().__init__()
        self.__instrument = instrument
        self.__quantity = quantity

    @property
    def instrument(self) -> Priceable:
        """Instrument or Id  
To specify a Marquee asset use the asset Id.
For listed products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin': 'US912810SD19' }.
To specify an instrument use one of the listed types"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Priceable):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        


class TradeCompleteAtHorizon(Base):
               
    def __init__(self, minutesExpired: int = None, positionsComplete: int = None, positionsCompletePct: float = None, notionalCompletePct: float = None):
        super().__init__()
        self.__minutesExpired = minutesExpired
        self.__positionsComplete = positionsComplete
        self.__positionsCompletePct = positionsCompletePct
        self.__notionalCompletePct = notionalCompletePct

    @property
    def minutesExpired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutesExpired

    @minutesExpired.setter
    def minutesExpired(self, value: int):
        self.__minutesExpired = value
        self._property_changed('minutesExpired')        

    @property
    def positionsComplete(self) -> int:
        """Number of the portfolio's positions that have been fully traded."""
        return self.__positionsComplete

    @positionsComplete.setter
    def positionsComplete(self, value: int):
        self.__positionsComplete = value
        self._property_changed('positionsComplete')        

    @property
    def positionsCompletePct(self) -> float:
        """Percentage of the portfolio's positions that have been fully traded."""
        return self.__positionsCompletePct

    @positionsCompletePct.setter
    def positionsCompletePct(self, value: float):
        self.__positionsCompletePct = value
        self._property_changed('positionsCompletePct')        

    @property
    def notionalCompletePct(self) -> float:
        """Percentage of the portfolio's notional that have been traded."""
        return self.__notionalCompletePct

    @notionalCompletePct.setter
    def notionalCompletePct(self, value: float):
        self.__notionalCompletePct = value
        self._property_changed('notionalCompletePct')        


class WeightedPosition(Base):
               
    def __init__(self, assetId: str, weight: float):
        super().__init__()
        self.__assetId = assetId
        self.__weight = weight

    @property
    def assetId(self) -> str:
        """Marquee unique identifier"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def weight(self) -> float:
        """Relative net weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
        self._property_changed('weight')        


class LiquidityFactorCategory(Base):
               
    def __init__(self, name: str = None, subFactors: Tuple[LiquidityFactor, ...] = None):
        super().__init__()
        self.__name = name
        self.__subFactors = subFactors

    @property
    def name(self) -> str:
        """Name of the factor category."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def subFactors(self) -> Tuple[LiquidityFactor, ...]:
        return self.__subFactors

    @subFactors.setter
    def subFactors(self, value: Tuple[LiquidityFactor, ...]):
        self.__subFactors = value
        self._property_changed('subFactors')        


class LiquiditySummary(Base):
        
    """Summary of the liquidity analytics data."""
       
    def __init__(self, total: LiquiditySummarySection, long: LiquiditySummarySection = None, short: LiquiditySummarySection = None, longVsShort: LiquiditySummarySection = None):
        super().__init__()
        self.__total = total
        self.__long = long
        self.__short = short
        self.__longVsShort = longVsShort

    @property
    def total(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__total

    @total.setter
    def total(self, value: LiquiditySummarySection):
        self.__total = value
        self._property_changed('total')        

    @property
    def long(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__long

    @long.setter
    def long(self, value: LiquiditySummarySection):
        self.__long = value
        self._property_changed('long')        

    @property
    def short(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__short

    @short.setter
    def short(self, value: LiquiditySummarySection):
        self.__short = value
        self._property_changed('short')        

    @property
    def longVsShort(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__longVsShort

    @longVsShort.setter
    def longVsShort(self, value: LiquiditySummarySection):
        self.__longVsShort = value
        self._property_changed('longVsShort')        


class MarketDataShock(Base):
        
    """A shock to apply to market coordinate values"""
       
    def __init__(self, shockType: Union[MarketDataShockType, str], value: float, precision: float = None, cap: float = None, floor: float = None, coordinateCap: float = None, coordinateFloor: float = None):
        super().__init__()
        self.__shockType = shockType if isinstance(shockType, MarketDataShockType) else get_enum_value(MarketDataShockType, shockType)
        self.__value = value
        self.__precision = precision
        self.__cap = cap
        self.__floor = floor
        self.__coordinateCap = coordinateCap
        self.__coordinateFloor = coordinateFloor

    @property
    def shockType(self) -> Union[MarketDataShockType, str]:
        """Market data shock type"""
        return self.__shockType

    @shockType.setter
    def shockType(self, value: Union[MarketDataShockType, str]):
        self.__shockType = value if isinstance(value, MarketDataShockType) else get_enum_value(MarketDataShockType, value)
        self._property_changed('shockType')        

    @property
    def value(self) -> float:
        """The amount by which to shock matching coordinates"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        

    @property
    def precision(self) -> float:
        """The precision to which the shock will be rounded"""
        return self.__precision

    @precision.setter
    def precision(self, value: float):
        self.__precision = value
        self._property_changed('precision')        

    @property
    def cap(self) -> float:
        """Upper bound on the shocked value"""
        return self.__cap

    @cap.setter
    def cap(self, value: float):
        self.__cap = value
        self._property_changed('cap')        

    @property
    def floor(self) -> float:
        """Lower bound on the shocked value"""
        return self.__floor

    @floor.setter
    def floor(self, value: float):
        self.__floor = value
        self._property_changed('floor')        

    @property
    def coordinateCap(self) -> float:
        """Upper bound on the pre-shocked value of matching coordinates"""
        return self.__coordinateCap

    @coordinateCap.setter
    def coordinateCap(self, value: float):
        self.__coordinateCap = value
        self._property_changed('coordinateCap')        

    @property
    def coordinateFloor(self) -> float:
        """Lower bound on the pre-shocked value of matching coordinates"""
        return self.__coordinateFloor

    @coordinateFloor.setter
    def coordinateFloor(self, value: float):
        self.__coordinateFloor = value
        self._property_changed('coordinateFloor')        


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a measure type, and a unit."""
       
    def __init__(self, assetClass: Union[AssetClass, str] = None, measureType: Union[RiskMeasureType, str] = None, unit: Union[RiskMeasureUnit, str] = None):
        super().__init__()
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__measureType = measureType if isinstance(measureType, RiskMeasureType) else get_enum_value(RiskMeasureType, measureType)
        self.__unit = unit if isinstance(unit, RiskMeasureUnit) else get_enum_value(RiskMeasureUnit, unit)

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

    @property
    def measureType(self) -> Union[RiskMeasureType, str]:
        """The type of measure to perform risk on. e.g. Greeks"""
        return self.__measureType

    @measureType.setter
    def measureType(self, value: Union[RiskMeasureType, str]):
        self.__measureType = value if isinstance(value, RiskMeasureType) else get_enum_value(RiskMeasureType, value)
        self._property_changed('measureType')        

    @property
    def unit(self) -> Union[RiskMeasureUnit, str]:
        """The unit of change of underlying in the risk computation."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[RiskMeasureUnit, str]):
        self.__unit = value if isinstance(value, RiskMeasureUnit) else get_enum_value(RiskMeasureUnit, value)
        self._property_changed('unit')        


class RiskModelRequest(Base):
        
    """Object representation of a risk model request"""
       
    def __init__(self, assetIds: Tuple[str, ...] = None, asOfDate: datetime.date = None, sortByTerm: Union[SortByTerm, str] = None):
        super().__init__()
        self.__assetIds = assetIds
        self.__asOfDate = asOfDate
        self.__sortByTerm = sortByTerm if isinstance(sortByTerm, SortByTerm) else get_enum_value(SortByTerm, sortByTerm)

    @property
    def assetIds(self) -> Tuple[str, ...]:
        """Assets to calculate on"""
        return self.__assetIds

    @assetIds.setter
    def assetIds(self, value: Tuple[str, ...]):
        self.__assetIds = value
        self._property_changed('assetIds')        

    @property
    def asOfDate(self) -> datetime.date:
        """The date or time for which to check risk model availability"""
        return self.__asOfDate

    @asOfDate.setter
    def asOfDate(self, value: datetime.date):
        self.__asOfDate = value
        self._property_changed('asOfDate')        

    @property
    def sortByTerm(self) -> Union[SortByTerm, str]:
        """Term to sort risk models by."""
        return self.__sortByTerm

    @sortByTerm.setter
    def sortByTerm(self, value: Union[SortByTerm, str]):
        self.__sortByTerm = value if isinstance(value, SortByTerm) else get_enum_value(SortByTerm, value)
        self._property_changed('sortByTerm')        


class LiquidityRequest(Base):
        
    """Required parameters in order to get liquidity information on a set of positions"""
       
    def __init__(self, positions: dict, notional: float = None, riskModel: Union[RiskModel, str] = None, date: datetime.date = None, currency: Union[Currency, str] = None, participationRate: float = None, benchmarkId: str = None, measures: Tuple[Union[LiquidityMeasure, str], ...] = None, timeSeriesBenchmarkIds: Tuple[str, ...] = None, timeSeriesStartDate: datetime.date = None, timeSeriesEndDate: datetime.date = None, format: Union[Format, str] = None):
        super().__init__()
        self.__notional = notional
        self.__positions = positions
        self.__riskModel = riskModel if isinstance(riskModel, RiskModel) else get_enum_value(RiskModel, riskModel)
        self.__date = date
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__participationRate = participationRate
        self.__benchmarkId = benchmarkId
        self.__measures = measures
        self.__timeSeriesBenchmarkIds = timeSeriesBenchmarkIds
        self.__timeSeriesStartDate = timeSeriesStartDate
        self.__timeSeriesEndDate = timeSeriesEndDate
        self.__format = format if isinstance(format, Format) else get_enum_value(Format, format)

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def positions(self) -> dict:
        """A set of quantity or weighted positions."""
        return self.__positions

    @positions.setter
    def positions(self, value: dict):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def riskModel(self) -> Union[RiskModel, str]:
        """Axioma risk model identifier."""
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value: Union[RiskModel, str]):
        self.__riskModel = value if isinstance(value, RiskModel) else get_enum_value(RiskModel, value)
        self._property_changed('riskModel')        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value
        self._property_changed('date')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def participationRate(self) -> float:
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value: float):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def benchmarkId(self) -> str:
        """Marquee unique asset identifier of the benchmark."""
        return self.__benchmarkId

    @benchmarkId.setter
    def benchmarkId(self, value: str):
        self.__benchmarkId = value
        self._property_changed('benchmarkId')        

    @property
    def measures(self) -> Tuple[Union[LiquidityMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[LiquidityMeasure, str], ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def timeSeriesBenchmarkIds(self) -> Tuple[str, ...]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__timeSeriesBenchmarkIds

    @timeSeriesBenchmarkIds.setter
    def timeSeriesBenchmarkIds(self, value: Tuple[str, ...]):
        self.__timeSeriesBenchmarkIds = value
        self._property_changed('timeSeriesBenchmarkIds')        

    @property
    def timeSeriesStartDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__timeSeriesStartDate

    @timeSeriesStartDate.setter
    def timeSeriesStartDate(self, value: datetime.date):
        self.__timeSeriesStartDate = value
        self._property_changed('timeSeriesStartDate')        

    @property
    def timeSeriesEndDate(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__timeSeriesEndDate

    @timeSeriesEndDate.setter
    def timeSeriesEndDate(self, value: datetime.date):
        self.__timeSeriesEndDate = value
        self._property_changed('timeSeriesEndDate')        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self.__format = value if isinstance(value, Format) else get_enum_value(Format, value)
        self._property_changed('format')        


class LiquidityResponse(Base):
        
    """Liquidity information for a set of weighted positions."""
       
    def __init__(self, assetsNotInRiskModel: Tuple[str, ...] = None, assetsNotInCostPredictModel: Tuple[str, ...] = None, asOfDate: datetime.date = None, riskModel: Union[RiskModel, str] = None, currency: Union[Currency, str] = None, report: str = None, summary: LiquiditySummary = None, constituents: Tuple[LiquidityConstituent, ...] = None, largestHoldingsByWeight: Tuple[LiquidityTableRow, ...] = None, leastLiquidHoldings: Tuple[LiquidityTableRow, ...] = None, advBuckets: Tuple[LiquidityBucket, ...] = None, regionBuckets: Tuple[LiquidityBucket, ...] = None, countryBuckets: Tuple[LiquidityBucket, ...] = None, sectorBuckets: Tuple[LiquidityBucket, ...] = None, industryBuckets: Tuple[LiquidityBucket, ...] = None, marketCapBuckets: Tuple[LiquidityBucket, ...] = None, executionCostsWithDifferentTimeHorizons: Tuple[ExecutionCostForHorizon, ...] = None, timeToTradeWithDifferentParticipationRates: Tuple[PRateForHorizon, ...] = None, riskOverTime: Tuple[RiskAtHorizon, ...] = None, tradeCompletePercentOverTime: Tuple[TradeCompleteAtHorizon, ...] = None, advPercentOverTime: Tuple[AdvCurveTick, ...] = None, riskBuckets: Tuple[LiquidityFactor, ...] = None, factorRiskBuckets: Tuple[LiquidityFactorCategory, ...] = None, exposureBuckets: Tuple[LiquidityFactor, ...] = None, factorExposureBuckets: Tuple[LiquidityFactorCategory, ...] = None, timeseriesData: Tuple[LiquidityTimeSeriesItem, ...] = None, errorMessage: str = None):
        super().__init__()
        self.__assetsNotInRiskModel = assetsNotInRiskModel
        self.__assetsNotInCostPredictModel = assetsNotInCostPredictModel
        self.__asOfDate = asOfDate
        self.__riskModel = riskModel if isinstance(riskModel, RiskModel) else get_enum_value(RiskModel, riskModel)
        self.__currency = currency if isinstance(currency, Currency) else get_enum_value(Currency, currency)
        self.__report = report
        self.__summary = summary
        self.__constituents = constituents
        self.__largestHoldingsByWeight = largestHoldingsByWeight
        self.__leastLiquidHoldings = leastLiquidHoldings
        self.__advBuckets = advBuckets
        self.__regionBuckets = regionBuckets
        self.__countryBuckets = countryBuckets
        self.__sectorBuckets = sectorBuckets
        self.__industryBuckets = industryBuckets
        self.__marketCapBuckets = marketCapBuckets
        self.__executionCostsWithDifferentTimeHorizons = executionCostsWithDifferentTimeHorizons
        self.__timeToTradeWithDifferentParticipationRates = timeToTradeWithDifferentParticipationRates
        self.__riskOverTime = riskOverTime
        self.__tradeCompletePercentOverTime = tradeCompletePercentOverTime
        self.__advPercentOverTime = advPercentOverTime
        self.__riskBuckets = riskBuckets
        self.__factorRiskBuckets = factorRiskBuckets
        self.__exposureBuckets = exposureBuckets
        self.__factorExposureBuckets = factorExposureBuckets
        self.__timeseriesData = timeseriesData
        self.__errorMessage = errorMessage

    @property
    def assetsNotInRiskModel(self) -> Tuple[str, ...]:
        """Assets in the the portfolio that are not covered in the risk model."""
        return self.__assetsNotInRiskModel

    @assetsNotInRiskModel.setter
    def assetsNotInRiskModel(self, value: Tuple[str, ...]):
        self.__assetsNotInRiskModel = value
        self._property_changed('assetsNotInRiskModel')        

    @property
    def assetsNotInCostPredictModel(self) -> Tuple[str, ...]:
        """Assets in the the portfolio that are not covered in the cost prediction model."""
        return self.__assetsNotInCostPredictModel

    @assetsNotInCostPredictModel.setter
    def assetsNotInCostPredictModel(self, value: Tuple[str, ...]):
        self.__assetsNotInCostPredictModel = value
        self._property_changed('assetsNotInCostPredictModel')        

    @property
    def asOfDate(self) -> datetime.date:
        """Calculation date in ISO 8601 format."""
        return self.__asOfDate

    @asOfDate.setter
    def asOfDate(self, value: datetime.date):
        self.__asOfDate = value
        self._property_changed('asOfDate')        

    @property
    def riskModel(self) -> Union[RiskModel, str]:
        """Axioma risk model identifier."""
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value: Union[RiskModel, str]):
        self.__riskModel = value if isinstance(value, RiskModel) else get_enum_value(RiskModel, value)
        self._property_changed('riskModel')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def report(self) -> str:
        return self.__report

    @report.setter
    def report(self, value: str):
        self.__report = value
        self._property_changed('report')        

    @property
    def summary(self) -> LiquiditySummary:
        """Summary of the liquidity analytics data."""
        return self.__summary

    @summary.setter
    def summary(self, value: LiquiditySummary):
        self.__summary = value
        self._property_changed('summary')        

    @property
    def constituents(self) -> Tuple[LiquidityConstituent, ...]:
        """Constituents of the portfolio enriched with liquidity and estimated transaction cost information."""
        return self.__constituents

    @constituents.setter
    def constituents(self, value: Tuple[LiquidityConstituent, ...]):
        self.__constituents = value
        self._property_changed('constituents')        

    @property
    def largestHoldingsByWeight(self) -> Tuple[LiquidityTableRow, ...]:
        """The five largest holdings by gross weight in the portfolio."""
        return self.__largestHoldingsByWeight

    @largestHoldingsByWeight.setter
    def largestHoldingsByWeight(self, value: Tuple[LiquidityTableRow, ...]):
        self.__largestHoldingsByWeight = value
        self._property_changed('largestHoldingsByWeight')        

    @property
    def leastLiquidHoldings(self) -> Tuple[LiquidityTableRow, ...]:
        """The five least liquid holdings in the portfolio."""
        return self.__leastLiquidHoldings

    @leastLiquidHoldings.setter
    def leastLiquidHoldings(self, value: Tuple[LiquidityTableRow, ...]):
        self.__leastLiquidHoldings = value
        self._property_changed('leastLiquidHoldings')        

    @property
    def advBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__advBuckets

    @advBuckets.setter
    def advBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__advBuckets = value
        self._property_changed('advBuckets')        

    @property
    def regionBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__regionBuckets

    @regionBuckets.setter
    def regionBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__regionBuckets = value
        self._property_changed('regionBuckets')        

    @property
    def countryBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__countryBuckets

    @countryBuckets.setter
    def countryBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__countryBuckets = value
        self._property_changed('countryBuckets')        

    @property
    def sectorBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__sectorBuckets

    @sectorBuckets.setter
    def sectorBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__sectorBuckets = value
        self._property_changed('sectorBuckets')        

    @property
    def industryBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__industryBuckets

    @industryBuckets.setter
    def industryBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__industryBuckets = value
        self._property_changed('industryBuckets')        

    @property
    def marketCapBuckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__marketCapBuckets

    @marketCapBuckets.setter
    def marketCapBuckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__marketCapBuckets = value
        self._property_changed('marketCapBuckets')        

    @property
    def executionCostsWithDifferentTimeHorizons(self) -> Tuple[ExecutionCostForHorizon, ...]:
        """Execution costs at different time horizons."""
        return self.__executionCostsWithDifferentTimeHorizons

    @executionCostsWithDifferentTimeHorizons.setter
    def executionCostsWithDifferentTimeHorizons(self, value: Tuple[ExecutionCostForHorizon, ...]):
        self.__executionCostsWithDifferentTimeHorizons = value
        self._property_changed('executionCostsWithDifferentTimeHorizons')        

    @property
    def timeToTradeWithDifferentParticipationRates(self) -> Tuple[PRateForHorizon, ...]:
        """Participation rates required at different time horizons."""
        return self.__timeToTradeWithDifferentParticipationRates

    @timeToTradeWithDifferentParticipationRates.setter
    def timeToTradeWithDifferentParticipationRates(self, value: Tuple[PRateForHorizon, ...]):
        self.__timeToTradeWithDifferentParticipationRates = value
        self._property_changed('timeToTradeWithDifferentParticipationRates')        

    @property
    def riskOverTime(self) -> Tuple[RiskAtHorizon, ...]:
        """Risk at different time horizons."""
        return self.__riskOverTime

    @riskOverTime.setter
    def riskOverTime(self, value: Tuple[RiskAtHorizon, ...]):
        self.__riskOverTime = value
        self._property_changed('riskOverTime')        

    @property
    def tradeCompletePercentOverTime(self) -> Tuple[TradeCompleteAtHorizon, ...]:
        """Trade completion information at different time horizons."""
        return self.__tradeCompletePercentOverTime

    @tradeCompletePercentOverTime.setter
    def tradeCompletePercentOverTime(self, value: Tuple[TradeCompleteAtHorizon, ...]):
        self.__tradeCompletePercentOverTime = value
        self._property_changed('tradeCompletePercentOverTime')        

    @property
    def advPercentOverTime(self) -> Tuple[AdvCurveTick, ...]:
        """Historical ADV Percent curve of the portfolio."""
        return self.__advPercentOverTime

    @advPercentOverTime.setter
    def advPercentOverTime(self, value: Tuple[AdvCurveTick, ...]):
        self.__advPercentOverTime = value
        self._property_changed('advPercentOverTime')        

    @property
    def riskBuckets(self) -> Tuple[LiquidityFactor, ...]:
        """Risk buckets."""
        return self.__riskBuckets

    @riskBuckets.setter
    def riskBuckets(self, value: Tuple[LiquidityFactor, ...]):
        self.__riskBuckets = value
        self._property_changed('riskBuckets')        

    @property
    def factorRiskBuckets(self) -> Tuple[LiquidityFactorCategory, ...]:
        """Factor risk buckets."""
        return self.__factorRiskBuckets

    @factorRiskBuckets.setter
    def factorRiskBuckets(self, value: Tuple[LiquidityFactorCategory, ...]):
        self.__factorRiskBuckets = value
        self._property_changed('factorRiskBuckets')        

    @property
    def exposureBuckets(self) -> Tuple[LiquidityFactor, ...]:
        """Exposure buckets."""
        return self.__exposureBuckets

    @exposureBuckets.setter
    def exposureBuckets(self, value: Tuple[LiquidityFactor, ...]):
        self.__exposureBuckets = value
        self._property_changed('exposureBuckets')        

    @property
    def factorExposureBuckets(self) -> Tuple[LiquidityFactorCategory, ...]:
        """Factor exposures buckets."""
        return self.__factorExposureBuckets

    @factorExposureBuckets.setter
    def factorExposureBuckets(self, value: Tuple[LiquidityFactorCategory, ...]):
        self.__factorExposureBuckets = value
        self._property_changed('factorExposureBuckets')        

    @property
    def timeseriesData(self) -> Tuple[LiquidityTimeSeriesItem, ...]:
        """Timeseries data."""
        return self.__timeseriesData

    @timeseriesData.setter
    def timeseriesData(self, value: Tuple[LiquidityTimeSeriesItem, ...]):
        self.__timeseriesData = value
        self._property_changed('timeseriesData')        

    @property
    def errorMessage(self) -> str:
        """Marquee Liquidity error message"""
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value: str):
        self.__errorMessage = value
        self._property_changed('errorMessage')        


class MarketDataPatternAndShock(Base):
        
    """A shock to apply to market coordinate values matching the supplied pattern"""
       
    def __init__(self, pattern: MarketDataPattern, shock: MarketDataShock):
        super().__init__()
        self.__pattern = pattern
        self.__shock = shock

    @property
    def pattern(self) -> MarketDataPattern:
        """A pattern used to match market coordinates"""
        return self.__pattern

    @pattern.setter
    def pattern(self, value: MarketDataPattern):
        self.__pattern = value
        self._property_changed('pattern')        

    @property
    def shock(self) -> MarketDataShock:
        """A shock to apply to market coordinate values"""
        return self.__shock

    @shock.setter
    def shock(self, value: MarketDataShock):
        self.__shock = value
        self._property_changed('shock')        


class MarketDataShockBasedScenario(Base):
        
    """A scenario comprised of user-defined market data shocks"""
       
    def __init__(self, shocks: Tuple[MarketDataPatternAndShock, ...]):
        super().__init__()
        self.__shocks = shocks

    @property
    def scenarioType(self) -> str:
        """MarketDataShockBasedScenario"""
        return 'MarketDataShockBasedScenario'        

    @property
    def shocks(self) -> Tuple[MarketDataPatternAndShock, ...]:
        return self.__shocks

    @shocks.setter
    def shocks(self, value: Tuple[MarketDataPatternAndShock, ...]):
        self.__shocks = value
        self._property_changed('shocks')        


class MarketDataScenario(Base):
        
    """A market data scenario to apply to the calculation"""
       
    def __init__(self, scenario: Union[CurveScenario, MarketDataShockBasedScenario], subtractBase: bool = False):
        super().__init__()
        self.__scenario = scenario
        self.__subtractBase = subtractBase

    @property
    def scenario(self) -> Union[CurveScenario, MarketDataShockBasedScenario]:
        """Market data scenarios"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: Union[CurveScenario, MarketDataShockBasedScenario]):
        self.__scenario = value
        self._property_changed('scenario')        

    @property
    def subtractBase(self) -> bool:
        """Subtract values computed under the base market data state, to return a diff, if true"""
        return self.__subtractBase

    @subtractBase.setter
    def subtractBase(self, value: bool):
        self.__subtractBase = value
        self._property_changed('subtractBase')        


class RiskRequest(Base):
        
    """Object representation of a risk calculation request"""
       
    def __init__(self, positions: Tuple[RiskPosition, ...], measures: Tuple[RiskMeasure, ...], asOf: datetime.date = None, marketDataAsOf: Union[datetime.date, datetime.datetime] = None, pricingAndMarketDataAsOf: Tuple[PricingDateAndMarketDataAsOf, ...] = None, pricingLocation: Union[PricingLocation, str] = 'NYC', marketDataVendor: Union[MarketDataVendor, str] = 'Goldman Sachs', waitForResults: bool = False, scenario: MarketDataScenario = None):
        super().__init__()
        self.__positions = positions
        self.__measures = measures
        self.__asOf = asOf
        self.__marketDataAsOf = marketDataAsOf
        self.__pricingAndMarketDataAsOf = pricingAndMarketDataAsOf
        self.__pricingLocation = pricingLocation if isinstance(pricingLocation, PricingLocation) else get_enum_value(PricingLocation, pricingLocation)
        self.__marketDataVendor = marketDataVendor if isinstance(marketDataVendor, MarketDataVendor) else get_enum_value(MarketDataVendor, marketDataVendor)
        self.__waitForResults = waitForResults
        self.__scenario = scenario

    @property
    def positions(self) -> Tuple[RiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[RiskPosition, ...]):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def measures(self) -> Tuple[RiskMeasure, ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta', 'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[RiskMeasure, ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def asOf(self) -> datetime.date:
        """DEPRECATED: The date(s) for which to run the calculation and date(s) or time(s) for which to snap market data"""
        return self.__asOf

    @asOf.setter
    def asOf(self, value: datetime.date):
        self.__asOf = value
        self._property_changed('asOf')        

    @property
    def marketDataAsOf(self) -> Union[datetime.date, datetime.datetime]:
        """DEPRECATED: The date or time to source market data"""
        return self.__marketDataAsOf

    @marketDataAsOf.setter
    def marketDataAsOf(self, value: Union[datetime.date, datetime.datetime]):
        self.__marketDataAsOf = value
        self._property_changed('marketDataAsOf')        

    @property
    def pricingAndMarketDataAsOf(self) -> Tuple[PricingDateAndMarketDataAsOf, ...]:
        return self.__pricingAndMarketDataAsOf

    @pricingAndMarketDataAsOf.setter
    def pricingAndMarketDataAsOf(self, value: Tuple[PricingDateAndMarketDataAsOf, ...]):
        self.__pricingAndMarketDataAsOf = value
        self._property_changed('pricingAndMarketDataAsOf')        

    @property
    def pricingLocation(self) -> Union[PricingLocation, str]:
        """The location for pricing and market data"""
        return self.__pricingLocation

    @pricingLocation.setter
    def pricingLocation(self, value: Union[PricingLocation, str]):
        self.__pricingLocation = value if isinstance(value, PricingLocation) else get_enum_value(PricingLocation, value)
        self._property_changed('pricingLocation')        

    @property
    def marketDataVendor(self) -> Union[MarketDataVendor, str]:
        """The market data provider"""
        return self.__marketDataVendor

    @marketDataVendor.setter
    def marketDataVendor(self, value: Union[MarketDataVendor, str]):
        self.__marketDataVendor = value if isinstance(value, MarketDataVendor) else get_enum_value(MarketDataVendor, value)
        self._property_changed('marketDataVendor')        

    @property
    def waitForResults(self) -> bool:
        """For short-running requests this may be set to true and the results will be returned directly. If false, the response will contain the Id to retrieve the results"""
        return self.__waitForResults

    @waitForResults.setter
    def waitForResults(self, value: bool):
        self.__waitForResults = value
        self._property_changed('waitForResults')        

    @property
    def scenario(self) -> MarketDataScenario:
        """A market data scenario to apply to the calculation"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: MarketDataScenario):
        self.__scenario = value
        self._property_changed('scenario')        
