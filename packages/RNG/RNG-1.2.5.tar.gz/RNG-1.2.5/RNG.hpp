#pragma once
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace RNG {
    using Integer = long long;
    using Float = double;

    static std::random_device hardware_seed {};
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256> hurricane{hardware_seed()};

    template <typename D>
    auto storm(D distribution) {
        return distribution(hurricane);
    }

    template <typename Number>
    auto smart_clamp(Number target, Number left_limit, Number right_limit) -> Number {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number, typename Size>
    auto analytic_continuation(Function && func, Number number, Size offset) -> Number {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return -offset;
    }

    auto min_int() -> Integer { return -std::numeric_limits<Integer>::max(); }
    auto max_int() -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() -> Float { return -std::numeric_limits<Float>::max(); }
    auto max_float() -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
    }

    auto random_float(Float left_limit, Float right_limit) -> Float {
        auto const distribution = std::uniform_real_distribution<Float> { left_limit, right_limit };
        return storm(distribution);
    }

    auto random_int(Integer left_limit, Integer right_limit) -> Integer {
        auto const distribution = std::uniform_int_distribution<Integer> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return storm(distribution);
    }

    auto random_below(Integer number) -> Integer {
        if (number > 0) {
            auto const distribution = std::uniform_int_distribution<Integer> { 0, number - 1 };
            return storm(distribution);
        }
        else return analytic_continuation(random_below, number, 0);
    }

    auto bernoulli(Float truth_factor) -> bool {
        auto const distribution = std::bernoulli_distribution {
            smart_clamp(truth_factor, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto binomial(Integer number_of_trials, Float probability) -> Integer {
        auto const distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) -> Integer {
        auto const distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return storm(distribution);
    }

    auto geometric(Float probability) -> Integer {
        auto const distribution = std::geometric_distribution<Integer> { smart_clamp(probability, 0.0, 1.0) };
        return storm(distribution);
    }

    auto poisson(Float mean) -> Integer {
        auto const distribution = std::poisson_distribution<Integer> { mean };
        return storm(distribution);
    }

    auto expovariate(Float lambda_rate) -> Float {
        auto const distribution = std::exponential_distribution<Float> { lambda_rate };
        return storm(distribution);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        auto const distribution = std::gamma_distribution<Float> { shape, scale };
        return storm(distribution);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        auto const distribution = std::weibull_distribution<Float> { shape, scale };
        return storm(distribution);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        auto const distribution = std::normal_distribution<Float> { mean, std_dev };
        return storm(distribution);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        auto const distribution = std::lognormal_distribution<Float> { log_mean, log_deviation };
        return storm(distribution);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        auto const distribution = std::extreme_value_distribution<Float> { location, scale };
        return storm(distribution);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        auto const distribution = std::chi_squared_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return storm(distribution);
    }

    auto cauchy(Float location, Float scale) -> Float {
        auto const distribution = std::cauchy_distribution<Float> { location, scale };
        return storm(distribution);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        auto const distribution = std::fisher_f_distribution<Float> {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return storm(distribution);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        auto const distribution = std::student_t_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return storm(distribution);
    }

} // end namespace
