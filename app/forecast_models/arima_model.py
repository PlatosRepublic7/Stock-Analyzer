from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

class ARIMAModel:
    def __init__(self, order=(1, 1, 1)):
        self.order = order
        self.model_fit = None
        self.data = None

    
    def train(self, data: pd.Series):
        '''
        Train or update the ARIMA model on new data
        '''
        self.data = data
        model = ARIMA(data, order=self.order)
        self.model_fit = model.fit()


    def predict(self, steps: int = 1):
        '''
        Predict future values using the ARIMA model
        '''
        if self.model_fit is None:
            raise ValueError("Model has not been trained.")
        return self.model_fit.forecast(steps=steps).tolist()
    

    def update(self, data: pd.Series):
        '''
        A simple update mechanism. We might want to change this later to retrain the model periodically.
        '''
        self.train(data)
