TP, FN, FP = 0, 0, 0
for k in range(len(IMAGE)):
    #create arrays for each image
    all_ground_truth = array #shape = n_groundtruth * 4
    all_predictions = array #shape = n_prediction * 4
    #all predictions are all that have score > thresh_score for this image
    if all_ground_truth.shape[0] == 0:
        tp = 0
        fn = 0
        fp = all_predictions.shape[0]
    if all_predictions.shape[0] == 0:
        tp = 0
        fn = all_ground_truth.shape[0]
        fp = 0
    else:
        fp, fn, tp = 0, 0, 0
        matrix = np.zeros([all_ground_truth.shape[0], all_predictions.shape[0]])
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if IoU(all_ground_truth[i], all_predictions[j]) > thresh_iou:
                    matrix[i, j] += 1
        sum_rows = matrix.sum(axis = 0)
        sum_cols = matrix.sum(axis = 1)
        for j in range(len(sum_cols)):
            if sum_cols[j] == 0:
                fn += 1
            if sum_cols[j] == 1:
                tp += 1
            if sum_cols[j] >= 2:
                tp += 1
                fp += sum_cols[j] - 1
        for i in range(len(sum_rows)):
            if sum_rows[i] == 0:
                fp += 1
    TP += tp
    FP += fp
    FN += fn
