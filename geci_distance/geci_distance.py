#!/usr/bin/env python

import pandas as pd
import numpy as np
from lmfit import Model
from scipy import integrate

def hazard_model(x,sigma,beta):
    return (1 - np.exp(-(x/sigma)**(-beta)))

class GECI_Distance():
    
    def __init__(self, n_obs, distances, n_bins=10):
        self.distances = distances
        self.n_bins = n_bins
        self.n_obs = n_obs
    
    def set_line_width(self, width):
        self.width = width
        
    def set_line_length(self,length):
        self.length = length
    
    def set_study_area(self, area, units='km2'):
        if units == 'km2':
            self.area = area*1_000_000
        if units == 'm2':
            self.area = area    

    def initialize_hazard_model(self):
        model = Model(hazard_model)
        model.set_param_hint('sigma', value= 1, min=0)
        model.set_param_hint('beta', value= 1, min=0)
        params = model.make_params()
        return model, params

    def calculate_mid_points(self, bins):
        return (bins[:-1]+bins[1:])/2

    def normalize_pdf(self, pdf):
        return pdf/pdf[0]

    def fit_detection_function(self, model='hazard'):
        if model == 'hazard':
            model, params = self.initialize_hazard_model()
            result = model.fit(self.norm_hist, params, x=self.bins_mid_points, method='nelder')
            self.sigma = result.params['sigma'].value
            self.beta = result.params['beta'].value
            return self.sigma, self.beta

    def calculate_histogram(self):
        hist, bins = np.histogram(self.distances, np.linspace(0, self.width, self.n_bins))
        self.norm_hist = self.normalize_pdf(hist)
        self.bins_mid_points = self.calculate_mid_points(bins)
        return self.norm_hist, self.bins_mid_points

    def calculate_detection_probability(self):
        self.calculate_histogram()
        self.fit_detection_function()
        area, error = integrate.quad(hazard_model, 0, self.width,args=(self.sigma,self.beta))
        self.detection_probability = area/self.width
        return self.detection_probability
    
    def estimate_population(self):
        self.calculate_detection_probability()
        self.n_total = np.sum(self.n_obs[self.distances < self.width])
        return (self.area*self.n_total)/(2*self.width*self.length*self.detection_probability)