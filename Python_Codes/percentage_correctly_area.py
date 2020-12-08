def get_pca(a, b):

    # a: ground_truth ; b: predicted
    # COORDINATES OF THE INTERSECTION BOX / Order: [xmin, ymin, xmax, ymax]
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height

    area_a = (a[2] - a[0]) * (a[3] - a[1])

    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    pca = area_overlap / area_a
    return pca

resultado = get_pca([339, 185, 402, 255], [333, 186, 398, 246])
print(resultado)
