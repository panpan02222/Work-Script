import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.metrics import confusion_matrix

def calculate_iou(box1, box2):
    # 计算IoU值
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1+w1, x2+w2)
    yi2 = min(y1+h1, y2+h2)
    inter_area = max(xi2-xi1, 0) * max(yi2-yi1, 0)
    box1_area = w1*h1
    box2_area = w2*h2
    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area
    return iou

def plot_boxes(boxes):
    # 绘制矩形框
    fig, ax = plt.subplots(1)
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    colors = ['r', 'b', 'g', 'y', 'c', 'm']
    for i, box in enumerate(boxes):
        rect = patches.Rectangle((box[0], box[1]), box[2], box[3], linewidth=1, edgecolor=colors[i%len(colors)], facecolor='none')
        ax.add_patch(rect)
    plt.show()

def calculate_confusion_matrix(iou):
    # 计算混淆矩阵
    threshold = 0.5
    if iou > threshold:
        tp = 1
        fp = 0
    else:
        tp = 0
        fp = 1
    cm = confusion_matrix([1], [1 if iou > threshold else 0])
    print('Confusion Matrix : \n', cm)
    print('TP: ', tp)
    print('FP: ', fp)

def main():
    # 获取用户输入的矩形框数量
    x = int(input("请输入矩形框的数量："))
    boxes = []
    for i in range(x):
        # 获取用户输入的矩形框信息
        box = list(map(int, input(f"请输入第{i+1}个矩形框的信息（格式：x y w h）：").split()))
        boxes.append(box)
    tp = 0
    fp = 0
    for i in range(1, len(boxes)):
        iou = calculate_iou(boxes[0], boxes[i])
        print(f'IoU between box 1 and box {i+1}: ', iou)
        if iou > 0.5:
            tp += 1
        else:
            fp += 1
    fn = x - 1 - tp
    print('TP: ', tp)
    print('FP: ', fp)
    print('FN: ', fn)
    plot_boxes(boxes)

# 运行主函数
main()
