Description:
Bitcoin Price Prediction Using Chainlet Data and Historical Trends

This project focuses on predicting Bitcoin prices using a combination of chainlet data and historical price trends, while ensuring no data leakage and adhering to constraints such as avoiding direct price features. The approach involved feature engineering, creating metrics like moving averages, momentum, and standard deviation to capture price behavior.

The model selection process compared neural networks and linear regression techniques. Neural networks performed poorly due to the dataset’s size, while Ordinary Least Squares (OLS) and Elastic Net emerged as the best-performing models, achieving an RMSE of ~1,039. The data was split using TimeSeriesSplit to maintain chronological integrity and prevent future data leakage.

Key challenges included limited predictive power from chainlet data, high collinearity in financial datasets, and constraints on feature selection. The project highlights the strengths of linear regression in constrained environments and reinforces the importance of robust feature engineering in financial modeling.