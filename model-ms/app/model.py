def getLinearPredictions(df):
    ''' Outputs the predictions of an ordinary least squares linear regression
        for the close price of given stocks.
    '''

    # Set up features and response tables.
    X = df['High', 'Low', 'Open', 'Volume']
    y = df['Close']

    # Train/Test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size-0.2, random_state=42)

    # Create and train model
    from sklearn.linear_model import LinearRegression
    lm = LinearRegression()
    lm.fit(X_train, y_train)

    # Print model information
    print("linear model intercept: " + lm.intercept_) # Intercept
    coeff_df = pd.DataFrame(lm.coef_, X.columns, columns = ['Coefficient']) # Coefficients (gradients)

    # Predictions
    predictions = lm.predict(X_test)

    # Metrics
    from sklearn import metrics
    print('MAE:', metrics.mean_absolute_error(y_test, predictions))
    print('MSE:', metrics.mean_squared_error(y_test, predictions))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

if __name__ = '__main__':
    BASE_PATH = '' # Add path of data here
    Stocks_df = pd.read_csv(BASE_PATH))
    getLinearPredictions(Stocks_df)
