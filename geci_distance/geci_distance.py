#!/usr/bin/env python

import numpy as np
from lmfit import Model
from scipy import integrate


def hazard_model(x, sigma, beta):
    return 1 - np.exp(-((x / sigma) ** (-beta)))


def initialize_hazard_model():
    model = Model(hazard_model)
    model.set_param_hint("sigma", value=1, min=0)
    model.set_param_hint("beta", value=1, min=0)
    params = model.make_params()
    return model, params


def calculate_mid_points(bins):
    return (bins[:-1] + bins[1:]) / 2


def normalize_histogram(hist):
    return hist / max(hist)


class GECI_Distance:
    def __init__(self, n_obs, distances, n_bins=10):
        self.area = None
        self.beta = None
        self.bins_mid_points = None
        self.detection_probability = None
        self.distances = distances
        self.length = None
        self.n_bins = n_bins
        self.n_obs = n_obs
        self.n_total = None
        self.norm_hist = None
        self.sigma = None
        self.width = None

    def set_line_width(self, width):
        self.width = width

    def set_line_length(self, length):
        self.length = length

    def set_study_area(self, area, units="km2"):
        if units == "km2":
            self.area = area * 1_000_000
        if units == "m2":
            self.area = area

    def fit_detection_function_hazard(self):
        model, params = initialize_hazard_model()
        result = model.fit(self.norm_hist, params, x=self.bins_mid_points, method="nelder")
        self.sigma = result.params["sigma"].value
        self.beta = result.params["beta"].value
        return self.sigma, self.beta

    def calculate_histogram(self):
        hist, bins = np.histogram(self.distances, np.linspace(0, self.width, self.n_bins))
        self.norm_hist = normalize_histogram(hist)
        self.bins_mid_points = calculate_mid_points(bins)
        return self.norm_hist, self.bins_mid_points

    def calculate_detection_probability(self):
        self.calculate_histogram()
        self.fit_detection_function_hazard()
        area, _ = integrate.quad(hazard_model, 0, self.width, args=(self.sigma, self.beta))
        self.detection_probability = area / self.width
        return self.detection_probability

    def estimate_population(self):
        self.calculate_detection_probability()
        self.n_total = np.sum(self.n_obs[self.distances < self.width])
        return (self.area * self.n_total) / (
            2 * self.width * self.length * self.detection_probability
        )
