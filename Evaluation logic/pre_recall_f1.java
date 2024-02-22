public class ClassificationMetrics {

    public static double[] precision_recall_fscore_support(
        int[] yTrue,
        int[] yPred,
        double beta,
        int[] labels,
        int posLabel,
        String average,
        String[] warnFor,
        double[] sampleWeight,
        String zeroDivision
    ) {
        // 初始化变量
        double zeroDivisionValue = checkZeroDivision(zeroDivision);
        labels = checkSetWiseLabels(yTrue, yPred, average, labels, posLabel);

        // 计算tp_sum, pred_sum, true_sum
        boolean samplewise = average.equals("samples");
        double[][][] MCM = multilabelConfusionMatrix(yTrue, yPred, sampleWeight, labels, samplewise);
        double[] tpSum = sumOfColumn(MCM, 1, 1);
        double[] predSum = sumColumns(MCM, 0, 1);
        double[] trueSum = sumColumns(MCM, 1, 0);

        if (average.equals("micro")) {
            double microTpSum = sumOfArray(tpSum);
            double microPredSum = sumOfArray(predSum);
            double microTrueSum = sumOfArray(trueSum);
            tpSum = new double[]{microTpSum};
            predSum = new double[]{microPredSum};
            trueSum = new double[]{microTrueSum};
        }

        // 计算precision, recall, f_score
        double beta2 = Math.pow(beta, 2);
        double[] precision = prfDivide(tpSum, predSum, "precision", "predicted", average, warnFor, zeroDivisionValue);
        double[] recall = prfDivide(tpSum, trueSum, "recall", "true", average, warnFor, zeroDivisionValue);
        double[] fScore = calculateFScore(precision, recall, beta2, zeroDivisionValue);

        // 根据average参数计算加权平均值
        if (average != null && !average.isEmpty()) {
            double[] weights = average.equals("weighted") ? trueSum : sampleWeight;
            precision = nanaverage(precision, weights);
            recall = nanaverage(recall, weights);
            fScore = nanaverage(fScore, weights);
        }

        return new double[]{precision[0], recall[0], fScore[0]};
    }

    // 以下是需要实现的辅助方法：
    // checkZeroDivision, checkSetWiseLabels, multilabelConfusionMatrix,
    // sumOfColumn, sumColumns, sumOfArray, prfDivide, calculateFScore, nanaverage

    // ...（这里省略了辅助方法的实现）
}
