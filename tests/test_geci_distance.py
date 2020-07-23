import pytest
import numpy as np
from geci_distance import *


X: int = 10
Sigma = 2
Beta: int = 1
DistancesData: np.array = np.array([1, 2, 3, 4, 5, 1, 2, 3, 10, 50])
N_obs_data: np.array = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
HistogramData: np.array = np.array([10, 5, 10, 2, 5, 1, 10])
NormalizedHistogram: np.array = np.array([1, 0.5, 1, 0.2, 0.5, 0.1, 1])
HistogramBinsLimits: np.array = np.array([3, 5, 7, 9, 11, 13, 15, 17])
HistogramCenteredBins: np.array = np.array([4, 6, 8, 10, 12, 14, 16])


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
    obtained_histogram = normalize_histogram(HistogramData)
    np.testing.assert_array_equal(obtained_histogram, NormalizedHistogram)


def test_calculate_mid_points():
    obtained_centered_bins = calculate_mid_points(HistogramBinsLimits)
    np.testing.assert_array_equal(obtained_centered_bins, HistogramCenteredBins)


def test_calculate_mid_points_output_lenght():
    lenght_histogram_limits = len(HistogramBinsLimits)
    lenght_centered_bins = len(HistogramCenteredBins)
    assert (lenght_histogram_limits - 1) == (lenght_centered_bins)
