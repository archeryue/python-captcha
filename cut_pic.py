 #图片x轴的投影，如果有数据（黑色像素点）值为1否则为0
def get_projection_x(image):
    p_x = [0 for x in xrange(image.size[0])]
    for w in xrange(image.size[1]):
        for h in xrange(image.size[0]):
            if image.getpixel((h,w)) == 0:
                p_x[h] = 1
    return p_x

#获取分割后的x轴坐标点
#返回值为[起始位置, 长度] 的列表
def get_split_seq(projection_x):
    res = []
    for idx in xrange(len(projection_x) - 1):
        p1 = projection_x[idx]
        p2 = projection_x[idx + 1]
        if p1 == 1 and idx == 0:
            res.append([idx, 1])
        elif p1 == 0 and p2 == 0:
            continue
        elif p1 == 1 and p2 == 1:
            res[-1][1] += 1
        elif p1 == 0 and p2 == 1:
            res.append([idx + 1, 1])
        elif p1 == 1 and p2 == 0:
            continue
    return res

#分割后的图片，x轴分割后，同时去掉y轴上线多余的空白
def split_image(image, split_seq=None):
    if split_seq is None:
        split_seq = get_split_seq(get_projection_x(image))
    length = len(split_seq)
    imgs = [[] for i in xrange(length)]
    res = []
    for w in xrange(image.size[1]):
        line = [image.getpixel((h,w)) for h in xrange(image.size[0])]
        for idx in xrange(length):
            pos = split_seq[idx][0]
            llen = split_seq[idx][1]
            l = line[pos:pos+llen]
            imgs[idx].append(l)
    for idx in xrange(length):
        datas = []
        height = 0
        for data in imgs[idx]:
            flag = False
            for d in data:
                if d == 0:
                    flag = True
            if flag == True:
                height += 1
                datas += data
        child_img = Image.new('L',(split_seq[idx][1], height))
        child_img.putdata(datas)
        res.append(child_img)
    return res
