# 모델 평가
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# 모델 저장
model.save('export_market_recommendation_model.h5')
