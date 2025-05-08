import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

# ages
X = np.array([5, 6, 7, 8, 9, 10], dtype=float)

# heights
Y = np.array([110, 116, 123, 130, 136, 142], dtype=float)

# Verileri ölçeklendirelim
scaler_X = StandardScaler()
scaler_Y = StandardScaler()

X_scaled = scaler_X.fit_transform(X.reshape(-1, 1))
Y_scaled = scaler_Y.fit_transform(Y.reshape(-1, 1))

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=10, activation="relu", input_shape=[1]),
    tf.keras.layers.Dense(units=1)
])

model.compile(optimizer="adam", loss="mean_squared_error")

model.fit(X_scaled, Y_scaled, epochs=500, verbose=0)

# Test tahmini
test_age = 7.5
test_age_scaled = scaler_X.transform(np.array([[test_age]]))  # Test verisini ölçeklendir
predicted_height_scaled = model.predict(test_age_scaled)

# Ölçekli sonucu geri dönüştür
predicted_height = scaler_Y.inverse_transform(predicted_height_scaled)
print(f"{test_age} için boy tahmini = {predicted_height[0][0]}")