#!python3
#distutils: language = c++


__all__ = (
    "bernoulli", "random_int", "random_below",
    "binomial", "negative_binomial", "geometric", "poisson",
    "generate_canonical", "random_float", "normalvariate", "lognormvariate",
    "expovariate", "gammavariate", "weibullvariate", "extreme_value",
    "chi_squared", "cauchy", "fisher_f", "student_t",
    "distribution_timer", "timer", "quick_test", "numeric_tests"
)


cdef extern from "RNG.hpp":
    long long _min_int              "RNG::min_int"()
    long long _max_int              "RNG::max_int"()
    double    _min_float            "RNG::min_float"()
    double    _max_float            "RNG::max_float"()
    double    _min_below            "RNG::min_below"()
    double    _min_above            "RNG::min_above"()
    int       _bernoulli            "RNG::bernoulli"(double)
    long long _random_int           "RNG::random_int"(long long, long long)
    long long _random_below         "RNG::random_below"(long long)
    long long _binomial             "RNG::binomial"(long long, double)
    long long _negative_binomial    "RNG::negative_binomial"(long long, double)
    long long _geometric            "RNG::geometric"(double)
    long long _poisson              "RNG::poisson"(double)
    double    _generate_canonical   "RNG::generate_canonical"()
    double    _random_float         "RNG::random_float"(double, double)
    double    _expovariate          "RNG::expovariate"(double)
    double    _gammavariate         "RNG::gammavariate"(double, double)
    double    _weibullvariate       "RNG::weibullvariate"(double, double)
    double    _normalvariate        "RNG::normalvariate"(double, double)
    double    _lognormvariate       "RNG::lognormvariate"(double, double)
    double    _extreme_value        "RNG::extreme_value"(double, double)
    double    _chi_squared          "RNG::chi_squared"(double)
    double    _cauchy               "RNG::cauchy"(double, double)
    double    _fisher_f             "RNG::fisher_f"(double, double)
    double    _student_t            "RNG::student_t"(double)


# RANDOM BOOLEAN #
def bernoulli(ratio_of_truth) -> bool:
    return _bernoulli(ratio_of_truth) == 1


# RANDOM INTEGER #
def random_int(left_limit, right_limit) -> int:
    return _random_int(left_limit, right_limit)

def random_below(upper_bound) -> int:
    return _random_below(upper_bound)

def binomial(number_of_trials, probability) -> int:
    return _binomial(number_of_trials, probability)

def negative_binomial(number_of_trials, probability) -> int:
    return _negative_binomial(number_of_trials, probability)

def geometric(probability) -> int:
    return _geometric(probability)

def poisson(mean) -> int:
    return _poisson(mean)


# RANDOM FLOATING POINT #
def generate_canonical():
    return _generate_canonical()

def random_float(left_limit, right_limit) -> float:
    return _random_float(left_limit, right_limit)
    
def expovariate(lambda_rate) -> float:
    return _expovariate(lambda_rate)
    
def gammavariate(shape, scale) -> float:
    return _gammavariate(shape, scale)
    
def weibullvariate(shape, scale) -> float:
    return _weibullvariate(shape, scale)
    
def extreme_value(location, scale) -> float:
    return _extreme_value(location, scale)
    
def normalvariate(mean, std_dev) -> float:
    return _normalvariate(mean, std_dev)
    
def lognormvariate(log_mean, log_deviation) -> float:
    return _lognormvariate(log_mean, log_deviation)
    
def chi_squared(degrees_of_freedom) -> float:
    return _chi_squared(degrees_of_freedom)
    
def cauchy(location, scale) -> float:
    return _cauchy(location, scale)
    
def fisher_f(degrees_of_freedom_1, degrees_of_freedom_2) -> float:
    return _fisher_f(degrees_of_freedom_1, degrees_of_freedom_2)
    
def student_t(degrees_of_freedom) -> float:
    return _student_t(degrees_of_freedom)


# DISTRIBUTION & PERFORMANCE TEST SUITE #
def timer(func: staticmethod, *args, **kwargs):
    import time as _time
    import statistics as _statistics

    results = []
    outer_cycles = 32
    inner_cycles = 32
    for _ in range(outer_cycles):
        start = _time.time_ns()
        for _ in range(inner_cycles):
            func(*args, **kwargs)
        end = _time.time_ns()
        results.append((end - start) // inner_cycles)
    output = (
        f"Min: {min(results)}ns",
        f"Mid: {int(_statistics.median(results))}ns",
        f"Max: {max(results)}ns",
    )
    print(f"Approximate Single Execution Time: {', '.join(output)}")


def distribution(func: staticmethod, *args, num_cycles, post_processor=None, **kwargs):
    import statistics as _statistics

    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    print(f"Test Samples: {num_cycles}")
    ave = _statistics.mean(results)
    median_lo = _statistics.median_low(results)
    median_hi = _statistics.median_high(results)
    median = median_lo if median_lo == median_hi else (median_lo, median_hi)
    std_dev = _statistics.stdev(results, ave)
    output = (
        f" Minimum: {min(results)}",
        f" Median: {median}",
        f" Maximum: {max(results)}",
        f" Mean: {ave}",
        f" Std Deviation: {std_dev}",
    )
    if post_processor is None:
        print("Sample Statistics:")
        print("\n".join(output))
        processed_results = results
        unique_results = list(set(results))
        print(f"Sample Distribution:")
    else:
        print("Pre-processor Statistics:")
        print("\n".join(output))
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution using {post_processor.__name__} method:")
    unique_results.sort()
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=100000, label="", post_processor=None, **kwargs):
    def samples(func, *args, **kwargs):
        return f', '.join(str(func(*args, **kwargs)) for _ in range(5))

    arguments = ', '.join([str(v) for v in args] + [f'{k}={v}' for k, v in kwargs.items()])
    if label:
        print(f"Output Analysis: {label}({arguments})")
    elif hasattr(func, "__qualname__"):
        print(f"Output Distribution: {func.__qualname__}({arguments})")
    elif hasattr(func, "__name__"):
        print(f"Output Distribution: {func.__name__}({arguments})")
    else:
        print(f"Output Analysis: {func}({arguments})")
    timer(func, *args, **kwargs)
    print(f"Raw Samples: {samples(func, *args, **kwargs)}")
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")


def numeric_tests():
    output = (
        "Round Trip Numeric Limits:",
        f" Min Integer: {_min_int()}",
        f" Max Integer:  {_max_int()}",
        f" Min Float: {_min_float()}",
        f" Max Float:  {_max_float()}",
        f" Min Below Zero: {_min_below()}",
        f" Min Above Zero:  {_min_above()}",
    )
    return "\n".join(output)


def quick_test(n=10000):
    import time as _time
    import math as _math
    import random as _random

    def floor_mod_10(x):
        return _math.floor(x) % 10

    print("\nQuick Test: RNG Storm Engine\n")
    start = _time.time()
    print(numeric_tests())
    print("\n\nBinary Tests\n")
    distribution_timer(bernoulli, 1/3, num_cycles=n)
    print("\nInteger Tests\n")
    distribution_timer(_random.randint, 1, 6, num_cycles=n)
    distribution_timer(random_int, 1, 6, num_cycles=n)
    distribution_timer(_random.randrange, 6, num_cycles=n)
    distribution_timer(random_below, 6, num_cycles=n)
    distribution_timer(binomial, 4, 0.5, num_cycles=n)
    distribution_timer(negative_binomial, 5, 0.75, num_cycles=n)
    distribution_timer(geometric, 0.75, num_cycles=n)
    distribution_timer(poisson, 4.5, num_cycles=n)
    print("\nFloating Point Tests\n")
    distribution_timer(_random.random, num_cycles=n, post_processor=round)
    distribution_timer(generate_canonical, num_cycles=n, post_processor=round)
    distribution_timer(random_float, 0.0, 10.0, num_cycles=n, post_processor=_math.floor)
    distribution_timer(_random.expovariate, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(expovariate, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(_random.gammavariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(gammavariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(_random.weibullvariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(weibullvariate, 1.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(extreme_value, 0.0, 1.0, num_cycles=n, post_processor=round)
    distribution_timer(_random.gauss, 5.0, 2.0, num_cycles=n, post_processor=round)
    distribution_timer(normalvariate, 5.0, 2.0, num_cycles=n, post_processor=round)
    distribution_timer(_random.lognormvariate, 1.6, 0.25, num_cycles=n, post_processor=round)
    distribution_timer(lognormvariate, 1.6, 0.25, num_cycles=n, post_processor=round)
    distribution_timer(chi_squared, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(cauchy, 0.0, 1.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(fisher_f, 8.0, 8.0, num_cycles=n, post_processor=floor_mod_10)
    distribution_timer(student_t, 8.0, num_cycles=n, post_processor=round)
    end = _time.time()
    duration = round(end - start, 4)
    print()
    print('=' * 73)
    print(f"Total Test Time: {duration} seconds\n\n")
