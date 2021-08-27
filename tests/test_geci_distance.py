import pytest
import numpy as np
from geci_distance import (
    GECI_Distance,
    hazard_model,
    initialize_hazard_model,
    normalize_histogram,
    calculate_mid_points,
)


X: int = 10
Sigma = 2
Beta: int = 1
DistancesData: np.array = np.array([1, 2, 3, 4, 5, 1, 2, 3, 10, 50])
N_obs_data: np.array = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
HistogramBinsLimits: np.array = np.array([3, 5, 7, 9, 11, 13, 15, 17])
HistogramCenteredBins: np.array = np.array([4, 6, 8, 10, 12, 14, 16])
distancia = GECI_Distance(n_obs=1, distances=1)


def test_hazard_model():
    output = hazard_model(X, Sigma, Beta)
    assert pytest.approx(output) == 0.18126924


def test_initialize_hazard_model():
    obteined_model, obteined_parameters = initialize_hazard_model()
    assert obteined_parameters["sigma"].value == 1
    assert obteined_parameters["sigma"].min == 0
    assert obteined_parameters["beta"].value == 1
    assert obteined_parameters["beta"].min == 0


def test_normalize_histogram():
    HistogramData: np.array = np.array([10, 5, 10, 2, 5, 1, 10])
    obtained_histogram = normalize_histogram(HistogramData)
    NormalizedHistogram: np.array = np.array([1, 0.5, 1, 0.2, 0.5, 0.1, 1])
    np.testing.assert_array_equal(obtained_histogram, NormalizedHistogram)
    HistogramData: np.array = np.array([10, 5, 20, 2, 5, 1, 10])
    obtained_histogram = normalize_histogram(HistogramData)
    NormalizedHistogram: np.array = np.array([0.5, 0.25, 1, 0.1, 0.25, 0.05, 0.5])
    np.testing.assert_array_equal(obtained_histogram, NormalizedHistogram)


def test_calculate_mid_points():
    obtained_centered_bins = calculate_mid_points(HistogramBinsLimits)
    np.testing.assert_array_equal(obtained_centered_bins, HistogramCenteredBins)


def test_calculate_mid_points_output_lenght():
    lenght_histogram_limits = len(HistogramBinsLimits)
    lenght_centered_bins = len(HistogramCenteredBins)
    assert (lenght_histogram_limits - 1) == (lenght_centered_bins)


def test_init_GECI_Distance():
    assert distancia.n_bins == 10
    assert distancia.n_obs == 1
    assert distancia.n_total is None
    assert distancia.area is None
    assert distancia.beta is None
    assert distancia.sigma is None
    assert distancia.bins_mid_points is None
    assert distancia.detection_probability is None
    assert distancia.distances == 1
    assert distancia.length is None
    assert distancia.width is None
    assert distancia.norm_hist is None


def test_property_GECI_Distance():
    distancia.set_line_length(4)
    assert distancia.length == 4
    distancia.set_line_width(4)
    assert distancia.width == 4
    distancia.set_study_area(area=1)
    assert distancia.area == 1_000_000
    distancia.set_study_area(area=1, units="m2")
    assert distancia.area == 1


class Test_GECI_Distance:
    def setup(self):
        self.project = GECI_Distance(n_obs=[10, 12], distances=[1, 1])
        self.project.set_line_width(9)

    def test_fit_detection_function_hazard(self):
        norm_hist, bins_mid_points = self.project.calculate_histogram()
        expected_bins_mid_points = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5])
        np.testing.assert_array_equal(expected_bins_mid_points, bins_mid_points)
        sigma, beta = self.project.fit_detection_function_hazard()
        assert sigma is not None
        assert beta is not None
