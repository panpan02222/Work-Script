from sklearn.metrics import precision_recall_fscore_support

y_true = [...]  # 真实标签
y_pred = [...]  # 预测结果

precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
