class ThermalStabilityPredictor:
    """A clean Analytical Linear Regression model constructed from scratch."""
    def __init__(self):
        # Pre-calculated trained weights for material thermal profiles
        self.intercept = 12.5 
        self.w_mean = -0.15
        self.w_var = 0.04

    def predict_time_to_equilibrium(self, mean_temp, variance):
        """
        Hypothesis Equation: y = b + w1*x1 + w2*x2
        Predicts remaining seconds until thermal steady-state is reached.
        """
        prediction = self.intercept + (self.w_mean * mean_temp) + (self.w_var * variance)
        return max(0.0, prediction) # Time cannot be negative
