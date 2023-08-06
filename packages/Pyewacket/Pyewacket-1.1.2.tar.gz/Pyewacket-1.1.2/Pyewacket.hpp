#pragma once
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace Pyewacket {
    using Integer = long long;
    using Float = double;

    struct Storm {
        using MT64_SCRAM = std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256>;
        std::random_device hardware_seed;
        MT64_SCRAM hurricane { hardware_seed() };
        template <typename D>
        auto operator()(D distribution) {
            return distribution(hurricane);
        }
        auto set_seed(unsigned long long seed) -> void {
            MT64_SCRAM cyclone { seed == 0 ? hardware_seed() : seed };
            hurricane = cyclone;
        }
    } storm;

    template <typename Function, typename Number, typename Size>
    auto analytic_continuation(Function && func, Number number, Size offset) -> Number {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return -offset;
    }

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(storm.hurricane);
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

    auto random_range(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop) return random_int(-1, 0);
        auto const width = Integer { std::abs(start - stop) - 1 };
        if (step > 0) return std::min(start, stop) + step * random_below((width + step) / step);
        if (step < 0) return std::max(start, stop) - step * random_below((width - step) / step);
        return random_int(-1, 0);
    }

    auto betavariate(Float alpha, Float beta) -> Float {
        auto const y = Float { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) -> Float {
        auto const u = Float { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        static auto const PI = Float { 4 * std::atan(1) };
        static auto const TAU = Float { 2 * PI };
        if (kappa <= 0.000001) return TAU * generate_canonical();
            auto const s = Float { 0.5 / kappa };
            auto const r = Float { s + std::sqrt(1 + s * s) };
            auto u1 = Float {0};
            auto z = Float {0};
            auto d = Float {0};
            auto u2 = Float {0};
            while (true) {
                u1 = generate_canonical();
                z = std::cos(PI * u1);
                d = z / (r + z);
                u2 = generate_canonical();
                if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
            }
        auto const q = Float { 1.0 / r };
        auto const f = Float { (q + z) / (1.0 + q * z) };
        auto const u3 = Float { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        else return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) -> Float {
        if (high - low == 0) return low;
        auto u = Float { generate_canonical() };
        auto c = Float { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            auto const temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }

} // end namespace
