def print_metrics(tp, tn, fp, fn):
    # 计算准确率
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    # 计算精确率
    precision = tp / (tp + fp)
    # 计算召回率
    recall = tp / (tp + fn)
    # 计算 F1 值
    f1 = 2 * precision * recall / (precision + recall)
    # 计算漏报率
    miss_rate = fn / (tp + fn)
    # 计算误报率
    fall_out_rate = fp / (tp + fp)

    print("准确率：{:.4f}".format(accuracy))
    print("精确率：{:.4f}".format(precision))
    print("召回率：{:.4f}".format(recall))
    print("F1 值：{:.4f}".format(f1))
    print("漏报率：{:.4f}".format(miss_rate))
    print("误报率：{:.4f}".format(fall_out_rate))


# 示例：
print("输入TP：")
tp = int(input())

print("输入TN：")
tn = int(input())

print("输入FP：")
fp = int(input())

print("输入FN：")
fn = int(input())

print_metrics(tp, tn, fp, fn)