#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>

namespace py = pybind11;

std::vector<double> two_way_shark_fin(
        py::array_t<double> price_path, // 2D array of price paths
        double high_price_trigger,
        double low_price_threshold,
        double k1 = 0.0185,
        double k2 = 0.0165,
        double participate_rate = 0.1002)
        {
    auto paths = price_path.unchecked<2>();
    std::vector<double> k3_yield(paths.shape(1));

    for (ssize_t i = 0; i < paths.shape(1); i++) {
        bool knocked_out = false;
        for (ssize_t j = 0; j < paths.shape(0); j++) {
            if (paths(j, i) > high_price_trigger || paths(j, i) < low_price_threshold) {
                knocked_out = true;
                break;
            }
        }
        if (knocked_out) {
            k3_yield[i] = k1;
        } else {
            k3_yield[i] = k2 + participate_rate * std::abs(paths(paths.shape(0) - 1, i) - 1);
        }
    }

    return k3_yield;
}

std::vector<double> one_way_shark_fin(
        py::array_t<double> price_path,
        const std::string &direction,
        double high_price_trigger,
        double low_price_threshold,
        double k1, double k3,
        double participate_rate = 0.1002) {
    auto paths = price_path.unchecked<2>();
    std::vector<double> final_yield(paths.shape(1));

    for (ssize_t i = 0; i < paths.shape(1); i++) {
        double lp = paths(paths.shape(0) - 1, i);
        if (direction == "long") {
            bool max_exceeds_trigger = false;
            for (ssize_t j = 0; j < paths.shape(0); j++) {
                if (paths(j, i) > high_price_trigger) {
                    max_exceeds_trigger = true;
                    break;
                }
            }
            if (max_exceeds_trigger) {
                final_yield[i] = k3;
            } else if (lp < low_price_threshold) {
                final_yield[i] = k1;
            } else {
                final_yield[i] = k1 + participate_rate * (lp - low_price_threshold);
            }
        } else {
            bool min_exceeds_threshold = false;
            for (ssize_t j = 0; j < paths.shape(0); j++) {
                if (paths(j, i) < low_price_threshold) {
                    min_exceeds_threshold = true;
                    break;
                }
            }
            if (min_exceeds_threshold) {
                final_yield[i] = k3;
            } else if (lp > high_price_trigger) {
                final_yield[i] = k1;
            } else {
                final_yield[i] = k1 + participate_rate * (high_price_trigger - lp);
            }
        }
    }

    return final_yield;
}

PYBIND11_MODULE(shark_fin, m) {
    m.def("two_way_shark_fin", &two_way_shark_fin, "Calculate two-way shark fin expected return",
          py::arg("price_path"), py::arg("high_price_trigger"), py::arg("low_price_threshold"),
          py::arg("k1") = 0.0185, py::arg("k2") = 0.0165, py::arg("participate_rate") = 0.1002);
    m.def("one_way_shark_fin", &one_way_shark_fin, "Calculate one-way shark fin expected return",
          py::arg("price_path"), py::arg("direction"), py::arg("high_price_trigger"), py::arg("low_price_threshold"),
          py::arg("k1"), py::arg("k3"), py::arg("participate_rate") = 0.1002);
}
