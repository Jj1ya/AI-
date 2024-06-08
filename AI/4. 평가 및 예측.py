# 예측
train_predict = model.predict(trainX)
test_predict = model.predict(testX)

# 스케일링 복원
train_predict = scaler.inverse_transform(train_predict)
trainY = scaler.inverse_transform([trainY])
test_predict = scaler.inverse_transform(test_predict)
testY = scaler.inverse_transform([testY])

# 결과 시각화
import matplotlib.pyplot as plt

# 예측값과 실제값 비교
plt.plot(data.index[:len(trainY[0])], trainY[0], label='Actual Train Data')
plt.plot(data.index[len(trainY[0]):len(trainY[0]) + len(testY[0])], testY[0], label='Actual Test Data')
plt.plot(data.index[:len(train_predict)], train_predict, label='Predicted Train Data')
plt.plot(data.index[len(trainY[0]):len(trainY[0]) + len(test_predict)], test_predict, label='Predicted Test Data')
plt.legend()
plt.show()
