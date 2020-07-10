import unittest
import numpy as np
from geci_distance import *


class Test_geci_distance(unittest.TestCase):
    def setUp(self):
        """
        Crea variables que se usarán en las pruebas
        """
        self.X: int = 10
        self.Sigma = 2
        self.Beta: int = 1
        self.DistancesData: np.array = np.array([1, 2, 3, 4, 5, 1, 2, 3, 10, 50])
        self.N_obs_data: np.array = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.HistogramData: np.array = np.array([10,5,10,2,5,1,10])
        self.NormalizedHistogram: np.array = np.array([1, 0.5,1,0.2,0.5,0.1,1])
        self.HistogramBinsLimits: np.array = np.array([3,5,7,9,11,13,15,17])
        self.HistogramCenteredBins: np.array = np.array([4,6,8,10,12,14,16])

    def test_hazard_model(self):
        output = hazard_model(self.X, self.Sigma, self.Beta)
        self.assertAlmostEqual(output, 0.18126924)

    def test_normalize_histogram(self):
        obtained_histogram = normalize_histogram(self.HistogramData)
        np.testing.assert_array_equal(obtained_histogram,self.NormalizedHistogram)

    def test_calculate_mid_points(self):
        obtained_centered_bins = calculate_mid_points(self.HistogramBinsLimits)
        np.testing.assert_array_equal(obtained_centered_bins,self.HistogramCenteredBins)
        
    def test_calculate_mid_points_output_lenght(self):
        lenght_histogram_limits = len(self.HistogramBinsLimits)
        lenght_centered_bins = len(self.HistogramCenteredBins)
        assert (lenght_histogram_limits-1) == (lenght_centered_bins)

if __name__ == "__main__":
    unittest.main()
