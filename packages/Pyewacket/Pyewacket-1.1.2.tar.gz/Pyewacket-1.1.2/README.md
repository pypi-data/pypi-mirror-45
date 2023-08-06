# Pyewacket
### Fast, fault-tolerant, drop-in replacement for the Python3 random module

Built on top of the RNG Storm Engine for stability and performance. While Storm is a high quality random engine, Pyewacket is not appropriate for cryptography of any kind. Pyewacket is meant for games, data science, A.I. and experimental programming, not security.


**Recommended Installation:** `$ pip install Pyewacket`


### Pyewacket serves three main goals:
1. Provide a feature rich and familiar API for generating random numbers and values.
    - Faithful to the random module API, but not a slave to it.
2. Go fast!
    - The RNG Storm Engine is an order of magnitude faster on average.
3. Fix things. Random.random is NOT broken, however it's not fault tolerant or fast.
    - Exceptions that can be avoided with balance, symmetry and sound mathematics, will be avoided. New behavior will be implemented as needed, but new math will not be invented.
    - Do or do not, there is no try/except. Alright, sometimes `try:` is useful, but it's only needed in truly exceptional cases where lambda calculus fails.
    - All class methods will be implemented as free functions when possible.


## Random Integers
- `Pyewacket.randbelow(n: int) -> int`
    - While randrange(a, b, c) can be handy, it's more complex than needed most of the time. Mathematically, randbelow(n) is equivalent to randrange(n) and they have nearly the same performance characteristics in Pyewacket, 10x - 12x faster than the random module's internal randbelow().
    - @param n :: Pyewacket expands the acceptable input domain to include non-positive values of n.
    - @return :: random integer in range (n, 0] or [0, n) depending on the sign of n.
    - Analytic Continuation about zero is used to achieve full input domain coverage for any function that normally can only take positive, non-zero values as input.
    - Symmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n) if n < 0 else 0` (this is how it works now).
    - The lambda is not the actual implementation, but it represents the idea of AC pretty well. AC will invert the meaning of a function for negative input. Thus turning _randbelow_ into _randabove_ for all negative values of n.

_It is possible that an asymmetric AC would be a better match to how negative numbers work as reverse list indexes in python._

Asymmetric Analytic Continuation: `lambda f, n: f(n) if n > 0 else -f(-n)-1 if n < 0 else None` (this is how it could work).

_This would allow_ `some_list[randbelow(-n)]` _to range over the last n items in a list of size n or larger. The interesting part is that you wouldn't need to know the exact size of the list. Let me know if you think this is a good idea._

```python
from Pyewacket import randbelow


""" Standard """
randbelow(10)       # -> [0, 10)

""" Extras """
randbelow(0)        # -> [0, 0) => 0
randbelow(-10)      # -> (-10, 0]
```

- `Pyewacket.randint(a: int, b: int) -> int`
    - @param a, b :: both are required,
    - @return :: random integer in range [a, b] or [b, a]
    - Inclusive on both sides
    - Removed the asymmetric requirement of a < b
    - When a == b returns a

```python
from Pyewacket import randint


""" Standard """
randint(1, 10)      # -> [1, 10]

""" Extras """
randint(10, 1)      # -> [1, 10]
randint(10, 10)     # -> [10, 10] => 10
```

- `Pyewacket.randrange(start: int, stop: int = 0, step: int = 1) -> int`
    - Fault tolerant and about 20x faster than random.randrange()
    - @param start :: required
    - @param stop :: optional, default=0
    - @parma step :: optional, default=1
    - @return :: random integer in range (stop, start] or [start, stop) by |step|
    - Removed the requirements of start < stop, and step > 0
    - Always returns start for start == stop or step == 0
    - Always inclusive on the lowest side exclusive on the higher side.
    - Ignores sign of step, but it could be a trigger for reversing the inclusivity rule.

```python
from Pyewacket import randrange


""" Standard """
randrange(10)           # -> [0, 10) by whole numbers
randrange(1, 10)        # -> [1, 10) by whole numbers
randrange(1, 10, 2)     # -> [1, 10) by 2, odd numbers

""" Extras """
randrange(0)            # -> [-1, 1)
randrange(-10)          # -> [-10, 0) by 1
randrange(10, 1)        # -> [1, 10) by 1
randrange(10, 0, 2)     # -> [0, 10) by 2, even numbers
randrange(10, 10, 0)    # -> [10, 10) => 10
```

## Random Floating Point
- `Pyewacket.random() -> float`
    - random float in range [0.0, 1.0] or [0.0, 1.0) depending on rounding.
    - This is the only function that doesn't show a performance increase, as expected.
    - Roughly the same speed as random.random()
- `Pyewacket.uniform(a: float, b: float) -> float`
    - random float in [a, b] or [a, b) depending on rounding
    - 4x faster
- `Pyewacket.expovariate(lambd: float) -> float`
    - 5x faster
- `Pyewacket.gammavariate(alpha, beta) -> float`
    - 10x faster
- `Pyewacket.weibullvariate(alpha, beta) -> float`
    - 4x faster
- `Pyewacket.betavariate(alpha, beta) -> float`
    - 16x faster
- `Pyewacket.paretovariate(alpha) -> float`
    - 4x faster
- `Pyewacket.gauss(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.normalvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.lognormvariate(mu: float, sigma: float) -> float`
    - 10x faster
- `Pyewacket.vonmisesvariate(mu: float, kappa: float) -> float`
    - 4x faster
- `Pyewacket.triangular(low: float, high: float, mode: float = None)`
    - 10x faster

## Random Sequence Values
- `Pyewacket.choice(seq: List) -> Value`
    - An order of magnitude faster than random.choice().
    - @param seq :: any zero indexed object like a list or tuple.
    - @return :: random value from the list, can be any object type that can be put into a list.
- `Pyewacket.choices(population, weights=None, *, cum_weights=None, k=1)`
    - @param population :: data values
    - @param weights :: relative weights
    - @param cum_weights :: cumulative weights
    - @param k :: number of samples to be collected
    - Only seeing a 2x performance gain.
- `Pyewacket.cumulative_weighted_choice(table, k=1)`
    - 10x faster than choices, but radically different API and a bit less flexible.
    - Supports Cumulative Weights only. Convert relative weights to cumulative if needed: `cum_weights = tuple(itertools.accumulate(rel_weights))`
    - @param table :: two dimensional list or tuple of weighted value pairs. `[(1, "a"), (10, "b"), (100, "c")...]`
        - The table can be constructed as `tuple(zip(cum_weights, population))` weights always come first.
    - @param k :: number of samples to be collected. Returns a list of size k if k > 1, otherwise returns a single value - not a list of one.
- `Pyewacket.shuffle(array: list) -> None`
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 20 times faster than random.shuffle().
    - Implements Knuth B Shuffle Algorithm. Knuth B is twice as fast as Knuth A or Fisher-Yates for every test case. This is likely due to the combination of walking backward and rotating backward into the back side of the list. With this combination it can never modify the data it still needs to walk through. Fresh snow all the way home, aka very low probability for cache misses.
- `Pyewacket.knuth(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Original Knuth Shuffle Algorithm.
    - Walks forward and rotates backward, but to the front side of the list.
- `Pyewacket.fisher_yates(array: list) -> None`, shuffle alternate.
    - Shuffles a list in place.
    - @param array :: must be a mutable list.
    - Approximately 10 times faster than random.shuffle().
    - Fisher-Yates Shuffle Algorithm. Used in random.shuffle().
    - Walks backward and rotates forward, into oncoming traffic.
- `Pyewacket.sample(population: List, k: int) -> list`
    - @param population :: list or tuple.
    - @param k :: number of unique samples to get.
    - @return :: size k list of unique random samples.
    - Performance gains range (5x to 20x) depending on len(population) and the ratio of k to len(population). Higher performance gains are seen when k ~= pop size.

## Seeding
- `set_seed(seed: int=0) -> None`
    - Hardware seeding is enabled by default. This is used to turn on/off software seeding and set or reset the engine seed. This affects all random functions in the module.
    - @param seed :: any non-zero positive integer less than 2**63 enables software seeding.
    - Calling `set_seed()` or `set_seed(0)` will turn off software seeding and re-enable hardware seeding.
    - While you can toggle software seeding on and off and re-seed the engine at will without error, this function is **not intended or optimized to be used in a loop**. General rule: seed once, or better yet, not at all. Typically, software seeding is for research and development, hardware seeding is used for modeling.

## Testing Suite
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - For the statistical analysis of a non-deterministic numeric output function.
    - @param func :: function, method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles=10000 :: Total number of samples to use for analysis.
    - @optional_kw post_processor=None :: Used to scale a large set of data into a smaller set of groupings for better visualization of the data, esp. useful for distributions of floats. For many functions in quick_test(), math.floor() is used, for others round() is more appropriate. For more complex post processing - lambdas work nicely. Post processing only affects the distribution, the statistics and performance results are unaffected.
- `quick_test() -> None`
    - Runs a battery of tests for each random distribution function in the module.


## Development Log
##### Pyewacket 1.1.2
- Low level clean up

##### Pyewacket 1.1.1
- Docs Update

##### Pyewacket 1.1.0
- Storm Engine Update

##### Pyewacket 1.0.3
- minor typos

##### Pyewacket 1.0.2
- added choices alternative `cumulative_weighted_choice`

##### Pyewacket 1.0.1
- minor typos

##### Pyewacket 1.0.0
- Storm 2 Rebuild.

##### Pyewacket 0.1.22
- Small bug fix.

##### Pyewacket 0.1.21
- Public Release

##### Pyewacket 0.0.2b1
- Added software seeding.

##### Pyewacket v0.0.1b8
- Fixed a small bug in the tests.

##### Pyewacket v0.0.1b7
- Engine Fine Tuning
- Fixed some typos.

##### Pyewacket v0.0.1b6
- Rearranged tests to be more consistent and match the documentation.

##### Pyewacket v0.0.1b5
- Documentation Upgrade
- Minor Performance Tweaks

##### Pyewacket v0.0.1b4
- Public Beta

##### Pyewacket v0.0.1b3
- quick_test()
- Extended Functionality
    - sample()
    - expovariate()
    - gammavariate()
    - weibullvariate()
    - betavariate()
    - paretovariate()
    - gauss()
    - normalvariate()
    - lognormvariate()
    - vonmisesvariate()
    - triangular()

##### Pyewacket v0.0.1b2
- Basic Functionality
    - random()
    - uniform()
    - randbelow()
    - randint()
    - randrange()
    - choice()
    - choices()
    - shuffle()

##### Pyewacket v0.0.1b1
- Initial Design & Planning


## Pywacket Distribution and Performance Test Suite
```
>>> from Pyewacket import quick_test
>>> quick_test()

Pyewacket Distribution & Performance Test Suite

Software Seed Test Passed
Hardware Seed Test Passed

Output Distribution: Random._randbelow(10)
Typical Timing: 734 nano seconds
Raw Samples: 1, 4, 7, 7, 0
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5241
 Std Deviation: 2.8686655633258162
Distribution of 10000 Samples:
 0: 9.78%
 1: 9.93%
 2: 10.1%
 3: 9.75%
 4: 10.05%
 5: 10.04%
 6: 9.92%
 7: 10.34%
 8: 10.08%
 9: 10.01%

Output Distribution: randbelow(10)
Typical Timing: 62 nano seconds
Raw Samples: 1, 2, 0, 8, 3
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4586
 Std Deviation: 2.8576743464340066
Distribution of 10000 Samples:
 0: 9.83%
 1: 10.33%
 2: 10.23%
 3: 10.29%
 4: 10.07%
 5: 10.04%
 6: 9.65%
 7: 10.23%
 8: 9.76%
 9: 9.57%

Output Distribution: Random.randint(1, 10)
Typical Timing: 1250 nano seconds
Raw Samples: 6, 3, 8, 4, 9
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4721
 Std Deviation: 2.8677942768618254
Distribution of 10000 Samples:
 1: 10.01%
 2: 10.08%
 3: 10.34%
 4: 10.03%
 5: 10.03%
 6: 9.89%
 7: 10.03%
 8: 9.95%
 9: 9.8%
 10: 9.84%

Output Distribution: randint(1, 10)
Typical Timing: 62 nano seconds
Raw Samples: 8, 10, 9, 10, 9
Statistics of 10000 Samples:
 Minimum: 1
 Median: 5
 Maximum: 10
 Mean: 5.4907
 Std Deviation: 2.8439975988446653
Distribution of 10000 Samples:
 1: 9.69%
 2: 9.76%
 3: 10.35%
 4: 10.24%
 5: 10.11%
 6: 10.08%
 7: 10.35%
 8: 9.9%
 9: 10.03%
 10: 9.49%

Output Distribution: Random.randrange(0, 10, 2)
Typical Timing: 1312 nano seconds
Raw Samples: 2, 6, 6, 6, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 4.0044
 Std Deviation: 2.817796060303823
Distribution of 10000 Samples:
 0: 19.86%
 2: 19.81%
 4: 20.32%
 6: 20.27%
 8: 19.74%

Output Distribution: randrange(0, 10, 2)
Typical Timing: 93 nano seconds
Raw Samples: 0, 8, 8, 6, 2
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 8
 Mean: 3.9588
 Std Deviation: 2.845753396069154
Distribution of 10000 Samples:
 0: 20.59%
 2: 20.53%
 4: 19.2%
 6: 19.71%
 8: 19.97%

Output Distribution: Random.random()
Typical Timing: 46 nano seconds
Raw Samples: 0.452113773717038, 0.324702374729146, 0.3386199842667629, 0.8945841097968128, 0.3375225724572536
Statistics of 10000 Samples:
 Minimum: 0.00021248617077440635
 Median: (0.4989077496280493, 0.4990924724844241)
 Maximum: 0.9998110181687437
 Mean: 0.5020683052830286
 Std Deviation: 0.287766446380214
Post-processor Distribution of 10000 Samples using round method:
 0: 50.09%
 1: 49.91%

Output Distribution: random()
Typical Timing: 31 nano seconds
Raw Samples: 0.7261941449935847, 0.699146546058287, 0.3027887766016304, 0.1909073997200837, 0.8744320326399283
Statistics of 10000 Samples:
 Minimum: 6.819904890052254e-05
 Median: (0.49678538919141535, 0.4968498623080506)
 Maximum: 0.9998288986023681
 Mean: 0.4990569691294414
 Std Deviation: 0.2878954977209575
Post-processor Distribution of 10000 Samples using round method:
 0: 50.4%
 1: 49.6%

Output Distribution: Random.uniform(0.0, 10.0)
Typical Timing: 218 nano seconds
Raw Samples: 5.601357797675895, 1.4093852987813282, 1.0316682431240765, 9.02536580727955, 3.524633590108831
Statistics of 10000 Samples:
 Minimum: 0.0003229197041909604
 Median: (4.917162355267131, 4.917715178285887)
 Maximum: 9.999811119019265
 Mean: 4.957406571386178
 Std Deviation: 2.8900271903119843
Post-processor Distribution of 10000 Samples using floor method:
 0: 10.3%
 1: 10.09%
 2: 9.9%
 3: 10.1%
 4: 10.47%
 5: 10.29%
 6: 9.25%
 7: 9.88%
 8: 9.73%
 9: 9.99%

Output Distribution: uniform(0.0, 10.0)
Typical Timing: 62 nano seconds
Raw Samples: 8.268355715908017, 8.143902427323841, 0.9053191550838635, 0.5290640646996809, 1.8306909908916555
Statistics of 10000 Samples:
 Minimum: 0.0001728371103980889
 Median: (5.035669261709544, 5.035838792473612)
 Maximum: 9.999817535204219
 Mean: 5.002361729428155
 Std Deviation: 2.8725396174866233
Post-processor Distribution of 10000 Samples using floor method:
 0: 9.94%
 1: 10.06%
 2: 9.73%
 3: 10.07%
 4: 9.83%
 5: 10.11%
 6: 10.54%
 7: 9.78%
 8: 10.45%
 9: 9.49%

Output Distribution: Random.expovariate(1.0)
Typical Timing: 343 nano seconds
Raw Samples: 1.0586644214710865, 0.07420371284222244, 4.268334430317107, 0.5374195958923661, 0.819991670905283
Statistics of 10000 Samples:
 Minimum: 4.00759251971335e-05
 Median: (0.7132666086349649, 0.7136527084708895)
 Maximum: 8.734362300515944
 Mean: 1.0178952010401694
 Std Deviation: 1.0096250042597235
Post-processor Distribution of 10000 Samples using floor method:
 0: 62.1%
 1: 24.1%
 2: 8.59%
 3: 3.15%
 4: 1.31%
 5: 0.52%
 6: 0.17%
 7: 0.02%
 8: 0.04%

Output Distribution: expovariate(1.0)
Typical Timing: 62 nano seconds
Raw Samples: 0.6662922367202619, 1.0518139610068657, 0.34397931090830103, 0.06455661809484374, 0.6905877312843888
Statistics of 10000 Samples:
 Minimum: 2.8540635842762585e-05
 Median: (0.6990352396503747, 0.6992176818987286)
 Maximum: 10.368620015635068
 Mean: 0.9984739127935243
 Std Deviation: 1.0000511960022445
Post-processor Distribution of 10000 Samples using floor method:
 0: 63.05%
 1: 22.97%
 2: 9.2%
 3: 2.9%
 4: 1.2%
 5: 0.46%
 6: 0.09%
 7: 0.08%
 8: 0.04%
 10: 0.01%

Output Distribution: Random.gammavariate(2.0, 1.0)
Typical Timing: 1327 nano seconds
Raw Samples: 1.6517221481951485, 5.601971024635998, 0.7552462080744275, 3.324396896912769, 1.2811196627332926
Statistics of 10000 Samples:
 Minimum: 0.01231853681272534
 Median: (1.689371714776512, 1.68940819573117)
 Maximum: 14.699205616505989
 Mean: 2.0111286753874675
 Std Deviation: 1.4380015575667486
Post-processor Distribution of 10000 Samples using round method:
 0: 9.4%
 1: 34.54%
 2: 27.57%
 3: 14.5%
 4: 7.68%
 5: 3.35%
 6: 1.81%
 7: 0.63%
 8: 0.27%
 9: 0.15%
 10: 0.04%
 11: 0.04%
 13: 0.01%
 15: 0.01%

Output Distribution: gammavariate(2.0, 1.0)
Typical Timing: 125 nano seconds
Raw Samples: 3.1239676714116476, 1.850196243665628, 0.6106383769323012, 4.905856858844702, 1.9057948681935182
Statistics of 10000 Samples:
 Minimum: 0.016463730925098785
 Median: (1.7037590760682038, 1.7042536931581989)
 Maximum: 12.96984673788258
 Mean: 2.0246970743047212
 Std Deviation: 1.4250745479493596
Post-processor Distribution of 10000 Samples using round method:
 0: 8.47%
 1: 35.3%
 2: 27.18%
 3: 15.17%
 4: 7.53%
 5: 3.71%
 6: 1.25%
 7: 0.86%
 8: 0.29%
 9: 0.17%
 10: 0.02%
 11: 0.04%
 13: 0.01%

Output Distribution: Random.weibullvariate(1.0, 1.0)
Typical Timing: 406 nano seconds
Raw Samples: 1.0647428076837189, 0.21763105911672628, 1.2344048322552614, 0.15228626210029217, 0.5411633975687867
Statistics of 10000 Samples:
 Minimum: 2.168944952219487e-05
 Median: (0.701166260299651, 0.7015490208415742)
 Maximum: 9.125263008333706
 Mean: 1.0011071111664056
 Std Deviation: 1.0000999397362862
Post-processor Distribution of 10000 Samples using floor method:
 0: 62.99%
 1: 23.87%
 2: 7.98%
 3: 3.27%
 4: 1.15%
 5: 0.51%
 6: 0.13%
 7: 0.09%
 9: 0.01%

Output Distribution: weibullvariate(1.0, 1.0)
Typical Timing: 93 nano seconds
Raw Samples: 1.0698713841826346, 0.3661784672787673, 3.212955259597982, 0.22683495422675737, 1.8344177096079224
Statistics of 10000 Samples:
 Minimum: 5.172117906815556e-06
 Median: (0.6907224366087179, 0.6907575909971655)
 Maximum: 8.260373812517944
 Mean: 0.9976132269189549
 Std Deviation: 0.999607622438296
Post-processor Distribution of 10000 Samples using floor method:
 0: 63.21%
 1: 23.03%
 2: 8.73%
 3: 3.18%
 4: 1.16%
 5: 0.39%
 6: 0.2%
 7: 0.09%
 8: 0.01%

Output Distribution: Random.betavariate(3.0, 3.0)
Typical Timing: 2625 nano seconds
Raw Samples: 0.47108077835875806, 0.35165036268541944, 0.696077264941614, 0.6194488054464196, 0.5462066156908687
Statistics of 10000 Samples:
 Minimum: 0.020937293452892202
 Median: (0.5006831515218838, 0.5007108510958133)
 Maximum: 0.983832195420959
 Mean: 0.49922947583131483
 Std Deviation: 0.1878584283075059
Post-processor Distribution of 10000 Samples using round method:
 0: 49.92%
 1: 50.08%

Output Distribution: betavariate(3.0, 3.0)
Typical Timing: 187 nano seconds
Raw Samples: 0.4397496153734576, 0.6867008957095052, 0.47572807501417896, 0.4444734346191479, 0.8028977482238089
Statistics of 10000 Samples:
 Minimum: 0.021153301115766746
 Median: (0.49788207308133064, 0.49789142509549095)
 Maximum: 0.972843282288602
 Mean: 0.49843417507446625
 Std Deviation: 0.19053771372941775
Post-processor Distribution of 10000 Samples using round method:
 0: 50.38%
 1: 49.62%

Output Distribution: Random.paretovariate(4.0)
Typical Timing: 281 nano seconds
Raw Samples: 1.6544244423263754, 1.1363754706647962, 1.02119022852101, 1.330441749533436, 1.2156273996001787
Statistics of 10000 Samples:
 Minimum: 1.000110144825699
 Median: (1.1929713738009007, 1.1930316583521086)
 Maximum: 10.12888771113417
 Mean: 1.3356971354933624
 Std Deviation: 0.47287093090770727
Post-processor Distribution of 10000 Samples using floor method:
 1: 93.6%
 2: 5.23%
 3: 0.78%
 4: 0.23%
 5: 0.05%
 6: 0.04%
 7: 0.03%
 8: 0.02%
 9: 0.01%
 10: 0.01%

Output Distribution: paretovariate(4.0)
Typical Timing: 93 nano seconds
Raw Samples: 1.0432160625883176, 1.0163263260652289, 1.1436726505089407, 2.035453520561038, 1.1198066655064416
Statistics of 10000 Samples:
 Minimum: 1.00002673768628
 Median: (1.1869066003563575, 1.186952771158858)
 Maximum: 13.690906972506928
 Mean: 1.33966754580419
 Std Deviation: 0.496719928418268
Post-processor Distribution of 10000 Samples using floor method:
 1: 93.33%
 2: 5.33%
 3: 0.89%
 4: 0.24%
 5: 0.08%
 6: 0.08%
 7: 0.02%
 8: 0.01%
 12: 0.01%
 13: 0.01%

Output Distribution: Random.gauss(1.0, 1.0)
Typical Timing: 593 nano seconds
Raw Samples: 1.632727789949952, 1.2078737104959731, -1.2980089459701243, 2.5382519062748687, 2.5802891445760343
Statistics of 10000 Samples:
 Minimum: -3.0646785865800332
 Median: (1.0047816937175948, 1.004838300803446)
 Maximum: 4.608701646315117
 Mean: 1.0038702218240454
 Std Deviation: 0.9992105831238515
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.01%
 -2: 0.49%
 -1: 6.24%
 0: 24.3%
 1: 37.86%
 2: 24.39%
 3: 6.05%
 4: 0.64%
 5: 0.02%

Output Distribution: gauss(1.0, 1.0)
Typical Timing: 93 nano seconds
Raw Samples: 2.20223892530431, -0.8770116065721415, 1.6339813189411334, 0.11860678111454293, 1.5180387334487528
Statistics of 10000 Samples:
 Minimum: -2.529391710735321
 Median: (1.000801697383217, 1.0008458906234512)
 Maximum: 5.024401796307943
 Mean: 0.9960626373391702
 Std Deviation: 0.9956992511331283
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.02%
 -2: 0.49%
 -1: 6.33%
 0: 23.76%
 1: 38.53%
 2: 24.39%
 3: 5.9%
 4: 0.57%
 5: 0.01%

Output Distribution: Random.normalvariate(0.0, 2.8)
Typical Timing: 718 nano seconds
Raw Samples: -2.873906985267837, 0.14825127718140937, 1.8214826953761216, 1.7470717361431463, 4.556714764251393
Statistics of 10000 Samples:
 Minimum: -9.904958063250993
 Median: (0.011841165423766113, 0.012376938669894953)
 Maximum: 11.2828782684694
 Mean: 0.026945030779767936
 Std Deviation: 2.820767894843342
Post-processor Distribution of 10000 Samples using round method:
 -10: 0.02%
 -9: 0.13%
 -8: 0.22%
 -7: 0.59%
 -6: 1.54%
 -5: 2.94%
 -4: 5.05%
 -3: 7.61%
 -2: 11.05%
 -1: 13.94%
 0: 13.57%
 1: 13.58%
 2: 11.08%
 3: 7.71%
 4: 5.12%
 5: 3.18%
 6: 1.5%
 7: 0.68%
 8: 0.26%
 9: 0.18%
 10: 0.02%
 11: 0.03%

Output Distribution: normalvariate(0.0, 2.8)
Typical Timing: 93 nano seconds
Raw Samples: -2.44606933711722, 0.5423187786193017, 0.31146959405684227, -0.82024289393346, 4.1563961197228165
Statistics of 10000 Samples:
 Minimum: -10.274507708807638
 Median: (0.00424594180991601, 0.004680394150810267)
 Maximum: 11.397876544064367
 Mean: 0.04903095434115078
 Std Deviation: 2.813957706418459
Post-processor Distribution of 10000 Samples using round method:
 -10: 0.02%
 -9: 0.07%
 -8: 0.2%
 -7: 0.6%
 -6: 1.57%
 -5: 2.87%
 -4: 4.51%
 -3: 8.49%
 -2: 11.04%
 -1: 13.26%
 0: 14.56%
 1: 12.39%
 2: 11.29%
 3: 8.07%
 4: 5.14%
 5: 3.15%
 6: 1.61%
 7: 0.73%
 8: 0.29%
 9: 0.11%
 10: 0.01%
 11: 0.02%

Output Distribution: Random.lognormvariate(0.0, 0.5)
Typical Timing: 921 nano seconds
Raw Samples: 1.37997688107477, 1.3266728726542778, 0.6966982569930297, 1.4273729464341807, 0.46635395105336674
Statistics of 10000 Samples:
 Minimum: 0.13913639653726315
 Median: (1.0063981441095902, 1.0064213917011822)
 Maximum: 6.7727877936567635
 Mean: 1.1385189959694435
 Std Deviation: 0.6100295304765773
Post-processor Distribution of 10000 Samples using round method:
 0: 8.31%
 1: 70.31%
 2: 18.0%
 3: 2.73%
 4: 0.5%
 5: 0.14%
 7: 0.01%

Output Distribution: lognormvariate(0.0, 0.5)
Typical Timing: 125 nano seconds
Raw Samples: 1.382263650559175, 1.0967769249837986, 0.9525022353964079, 0.6336998427927555, 3.294643707864458
Statistics of 10000 Samples:
 Minimum: 0.16450560013470697
 Median: (0.9886189220302626, 0.9886380852872596)
 Maximum: 5.906593745266734
 Mean: 1.1258743416602932
 Std Deviation: 0.6014020648183204
Post-processor Distribution of 10000 Samples using round method:
 0: 8.46%
 1: 71.19%
 2: 16.9%
 3: 2.85%
 4: 0.52%
 5: 0.07%
 6: 0.01%

Output Distribution: Random.vonmisesvariate(0, 0)
Typical Timing: 250 nano seconds
Raw Samples: 1.5360522950975362, 1.880106378481605, 2.070352086789122, 3.119591795956658, 0.675769974917279
Statistics of 10000 Samples:
 Minimum: 7.88066058613169e-05
 Median: (3.202394530422687, 3.202796012926651)
 Maximum: 6.282949158839051
 Mean: 3.1740091535846586
 Std Deviation: 1.8082184166134825
Post-processor Distribution of 10000 Samples using floor method:
 0: 15.44%
 1: 15.8%
 2: 15.77%
 3: 16.22%
 4: 15.94%
 5: 16.16%
 6: 4.67%

Output Distribution: vonmisesvariate(0, 0)
Typical Timing: 93 nano seconds
Raw Samples: 5.730196467733814, 4.22118046282148, 0.8652953912693463, 0.12455561455029643, 1.9019128815688269
Statistics of 10000 Samples:
 Minimum: 0.0001867189287552452
 Median: (3.10853458417522, 3.1098657121591415)
 Maximum: 6.281133418171666
 Mean: 3.118226433739434
 Std Deviation: 1.8187032521613016
Post-processor Distribution of 10000 Samples using floor method:
 0: 16.54%
 1: 15.46%
 2: 16.05%
 3: 16.29%
 4: 15.72%
 5: 15.37%
 6: 4.57%

Output Distribution: Random.triangular(0.0, 10.0, 0.0)
Typical Timing: 468 nano seconds
Raw Samples: 0.5587417128877323, 7.99434690489144, 3.7253658650974417, 4.523690517374057, 1.3715281454087922
Statistics of 10000 Samples:
 Minimum: 0.0005064022092575726
 Median: (2.867114618617239, 2.8680228555846927)
 Maximum: 9.875625839062343
 Mean: 3.309575576762302
 Std Deviation: 2.3681554409559102
Post-processor Distribution of 10000 Samples using floor method:
 0: 19.31%
 1: 17.63%
 2: 14.77%
 3: 12.58%
 4: 10.96%
 5: 8.7%
 6: 6.82%
 7: 5.29%
 8: 2.9%
 9: 1.04%

Output Distribution: triangular(0.0, 10.0, 0.0)
Typical Timing: 62 nano seconds
Raw Samples: 3.8338147662369346, 0.7104487672264359, 2.629187119538864, 1.1834775207102732, 0.24047248057069814
Statistics of 10000 Samples:
 Minimum: 0.0007669365472395828
 Median: (2.950798557566369, 2.951027761301488)
 Maximum: 9.932677430995808
 Mean: 3.341968360979483
 Std Deviation: 2.3618624940074078
Post-processor Distribution of 10000 Samples using floor method:
 0: 19.17%
 1: 16.38%
 2: 15.25%
 3: 12.91%
 4: 11.24%
 5: 9.29%
 6: 6.69%
 7: 4.87%
 8: 3.22%
 9: 0.98%

Output Distribution: Random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 781 nano seconds
Raw Samples: 0, 8, 6, 5, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5109
 Std Deviation: 2.8652577825068413
Distribution of 10000 Samples:
 0: 9.71%
 1: 10.05%
 2: 10.08%
 3: 10.13%
 4: 9.89%
 5: 10.1%
 6: 9.83%
 7: 10.01%
 8: 10.42%
 9: 9.78%

Output Distribution: choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Typical Timing: 62 nano seconds
Raw Samples: 5, 6, 4, 2, 1
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.5124
 Std Deviation: 2.8429306121406737
Distribution of 10000 Samples:
 0: 9.3%
 1: 9.91%
 2: 10.28%
 3: 10.47%
 4: 10.13%
 5: 9.86%
 6: 10.39%
 7: 9.78%
 8: 10.18%
 9: 9.7%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 2296 nano seconds
Raw Samples: [6], [1], [0], [5], [2]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 2.9836
 Std Deviation: 2.451720239589607
Distribution of 10000 Samples:
 0: 19.1%
 1: 15.86%
 2: 13.96%
 3: 12.7%
 4: 11.04%
 5: 9.43%
 6: 7.31%
 7: 5.3%
 8: 3.49%
 9: 1.81%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], k=1)
Typical Timing: 1093 nano seconds
Raw Samples: [0], [2], [4], [0], [7]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0193
 Std Deviation: 2.4424422331769158
Distribution of 10000 Samples:
 0: 17.85%
 1: 15.93%
 2: 14.68%
 3: 13.31%
 4: 10.96%
 5: 9.08%
 6: 7.17%
 7: 5.49%
 8: 3.75%
 9: 1.78%

Output Distribution: Random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 1718 nano seconds
Raw Samples: [0], [0], [0], [0], [1]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0384
 Std Deviation: 2.47166671572754
Distribution of 10000 Samples:
 0: 18.26%
 1: 15.52%
 2: 15.04%
 3: 12.27%
 4: 10.78%
 5: 9.64%
 6: 7.08%
 7: 5.69%
 8: 3.68%
 9: 2.04%

Output Distribution: choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cum_weights=[10, 19, 27, 34, 40, 45, 49, 52, 54, 55], k=1)
Typical Timing: 718 nano seconds
Raw Samples: [3], [4], [7], [1], [5]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.0264
 Std Deviation: 2.47905579036882
Distribution of 10000 Samples:
 0: 18.81%
 1: 15.75%
 2: 13.85%
 3: 12.6%
 4: 11.2%
 5: 9.16%
 6: 7.47%
 7: 5.39%
 8: 3.69%
 9: 2.08%

Output Distribution: cumulative_weighted_choice(((10, 0), (19, 1), (27, 2), (34, 3), (40, 4), (45, 5), (49, 6), (52, 7), (54, 8), (55, 9)), k=1)
Typical Timing: 156 nano seconds
Raw Samples: 1, 3, 1, 3, 6
Statistics of 10000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 9
 Mean: 3.032
 Std Deviation: 2.4715150897139733
Distribution of 10000 Samples:
 0: 18.27%
 1: 15.71%
 2: 14.61%
 3: 12.81%
 4: 11.08%
 5: 9.01%
 6: 6.95%
 7: 5.57%
 8: 4.13%
 9: 1.86%

Timer only: _random.shuffle(some_list) of size 10:
Typical Timing: 6875 nano seconds

Timer only: shuffle(some_list) of size 10:
Typical Timing: 375 nano seconds

Timer only: knuth(some_list) of size 10:
Typical Timing: 875 nano seconds

Timer only: fisher_yates(some_list) of size 10:
Typical Timing: 968 nano seconds

Output Distribution: Random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Typical Timing: 4062 nano seconds
Raw Samples: [4, 9, 2], [7, 0, 2], [4, 9, 1], [5, 9, 0], [2, 7, 5]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4708
 Std Deviation: 2.880586248962834
Distribution of 10000 Samples:
 0: 10.49%
 1: 9.39%
 2: 10.61%
 3: 10.13%
 4: 9.99%
 5: 9.98%
 6: 9.75%
 7: 9.72%
 8: 9.78%
 9: 10.16%

Output Distribution: sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
Typical Timing: 781 nano seconds
Raw Samples: [0, 3, 1], [7, 9, 6], [5, 8, 6], [2, 4, 7], [4, 2, 8]
Statistics of 10000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.4801
 Std Deviation: 2.8830253508280763
Distribution of 10000 Samples:
 0: 10.34%
 1: 10.05%
 2: 10.2%
 3: 9.48%
 4: 10.21%
 5: 9.92%
 6: 9.87%
 7: 9.76%
 8: 10.39%
 9: 9.78%


Total Test Time: 1.557 sec

```
