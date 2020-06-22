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
        self.DistancesData: np.array = np.array([1,2,3,4,5,1,2,3,10,50])
        self.N_obs_data: np.array = np.array([1,1,1,1,1,1,1,1,1,1])

    def test_hazard_model(self):
        output = hazard_model(self.X, self.Sigma, self.Beta)
        self.assertAlmostEqual(output, 0.18126924)

if __name__ == "__main__":
    unittest.main()
