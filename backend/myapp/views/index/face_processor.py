import numpy as np
import cv2
import dlib
import math

class FaceProcessor:
    def __init__(self, predictor_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    @staticmethod
    def sharpen_image(src):
        blur_img = cv2.GaussianBlur(src, (0, 0), 5)
        usm = cv2.addWeighted(src, 1.5, blur_img, -0.5, 0)
        return usm

    @staticmethod
    def bilinear_insert(src, ux, uy):
        # 双线性插值法
        w, h, c = src.shape
        if c == 3:
            x1 = int(ux)
            x2 = x1 + 1
            y1 = int(uy)
            y2 = y1 + 1

            part1 = src[y1, x1].astype(np.float32) * (float(x2) - ux) * (float(y2) - uy)
            part2 = src[y1, x2].astype(np.float32) * (ux - float(x1)) * (float(y2) - uy)
            part3 = src[y2, x1].astype(np.float32) * (float(x2) - ux) * (uy - float(y1))
            part4 = src[y2, x2].astype(np.float32) * (ux - float(x1)) * (uy - float(y1))

            insert_value = part1 + part2 + part3 + part4
            return insert_value.astype(np.int8)

    def local_translation_warp(self, src_img, start_x, start_y, end_x, end_y, radius):
        ddradius = float(radius * radius)
        copy_img = np.zeros(src_img.shape, np.uint8)
        copy_img = src_img.copy()

        # 计算公式中的 |m-c|^2
        ddmc = (end_x - start_x) * (end_x - start_x) + (end_y - start_y) * (end_y - start_y)
        h, w, c = src_img.shape
        for i in range(w):
            for j in range(h):
                # 计算该点是否在形变圆的范围之内
                if math.fabs(i - start_x) > radius and math.fabs(j - start_y) > radius:
                    continue

                distance = (i - start_x) * (i - start_x) + (j - start_y) * (j - start_y)
                if distance < ddradius:
                    # 计算出（i,j）坐标的原坐标
                    ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                    ratio = ratio * ratio

                    # 映射原位置
                    ux = i - ratio * (end_x - start_x)
                    uy = j - ratio * (end_y - start_y)

                    # 根据双线性插值法得到 UX, UY 的值
                    value = self.bilinear_insert(src_img, ux, uy)
                    # 改变当前 i, j 的值
                    copy_img[j, i] = value

        return copy_img

    def landmark_dec_dlib_fun(self, img_src):
        img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
        land_marks = []
        rects = self.detector(img_gray, 0)
        for i in range(len(rects)):
            land_marks_node = np.matrix([[p.x, p.y] for p in self.predictor(img_gray, rects[i]).parts()])
            land_marks.append(land_marks_node)
        return land_marks

    def face_thin_auto(self, src):
        landmarks = self.landmark_dec_dlib_fun(src)
        if len(landmarks) == 0:
            return src

        for landmarks_node in landmarks:
            left_landmark = landmarks_node[3]
            left_landmark_down = landmarks_node[5]
            right_landmark = landmarks_node[13]
            right_landmark_down = landmarks_node[15]
            end_pt = landmarks_node[30]

            # 瘦左边脸
            thin_image = self.local_translation_warp(src, left_landmark[0, 0], left_landmark[0, 1], end_pt[0, 0], end_pt[0, 1], 70)
            # 瘦右边脸
            thin_image = self.local_translation_warp(thin_image, right_landmark[0, 0], right_landmark[0, 1], end_pt[0, 0], end_pt[0, 1], 70)
            return thin_image

    def face_thin(self, image):
        return self.face_thin_auto(image)

    def getEllipseCross(self,p1x, p1y, p2x, p2y, a, b, centerX, centerY):
        resx = 0
        resy = 0
        k = (p1y - p2y) / (p1x - p2x)
        m = p1y - k * p1x
        A = (b * b + (a * a * k * k))
        B = 2 * a * a * k * m
        C = a * a * (m * m - b * b)

        X1 = (-B + math.sqrt(B * B - (4 * A * C))) / (2 * A)
        X2 = (-B - math.sqrt(B * B - (4 * A * C))) / (2 * A)

        Y1 = k * X1 + m
        Y2 = k * X2 + m

        if self.getDis(p2x, p2y, X1, Y1) < self.getDis(p2x, p2y, X2, Y2):
            resx = X1
            resy = Y1
        else:
            resx = X2
            resy = Y2

        return [resx + centerX, resy + centerY]
    
    @staticmethod
    def getLinearEquation(p1x, p1y, p2x, p2y):
        sign = 1
        a = p2y - p1y
        if a < 0:
            sign = -1
            a = sign * a
        b = sign * (p1x - p2x)
        c = sign * (p1y * p2x - p1x * p2y)
        return [a, b, c]

    @staticmethod
    def getDis(p1x, p1y, p2x, p2y):
        return math.sqrt((p1x - p2x) * (p1x - p2x) + (p1y - p2y) * (p1y - p2y))

    @staticmethod
    def get_line_cross_point(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
        a0, b0, c0 = FaceProcessor.getLinearEquation(p1x, p1y, p2x, p2y)
        a1, b1, c1 = FaceProcessor.getLinearEquation(p3x, p3y, p4x, p4y)

        D = a0 * b1 - a1 * b0
        if D == 0:
            return None
        x = (b0 * c1 - b1 * c0) / D
        y = (a1 * c0 - a0 * c1) / D
        return x, y
    
    def localTranslationWarp(self, srcImg, startIndex, endIndex, Strength, landmarks_node):
        midIndex = (startIndex + endIndex + 1) >> 1

        startDot = landmarks_node[startIndex]
        endDot = landmarks_node[endIndex]
        midDot = landmarks_node[midIndex]

        Eye = []
        for i in range(startIndex, endIndex + 1):
            Eye.append([landmarks_node[i][0, 0], landmarks_node[i][0, 1]])
        ellipseEye = cv2.fitEllipse(np.array(Eye))

        radius = math.sqrt(
            (startDot[0, 0] - midDot[0, 0]) * (startDot[0, 0] - midDot[0, 0]) -
            (startDot[0, 1] - midDot[0, 1]) * (startDot[0, 1] - midDot[0, 1])
        ) / 2
        points_list = []

        for i in range(0, 3):
            tmplist = self.get_line_cross_point(
                landmarks_node[startIndex + i][0, 0], landmarks_node[startIndex + i][0, 1],
                landmarks_node[midIndex + i][0, 0], landmarks_node[midIndex + i][0, 1],
                landmarks_node[startIndex + ((i + 1) % 3)][0, 0], landmarks_node[startIndex + ((i + 1) % 3)][0, 1],
                landmarks_node[midIndex + ((i + 1) % 3)][0, 0], landmarks_node[midIndex + ((i + 1) % 3)][0, 1]
            )
            points_list.append(tmplist)

        a = self.getDis(points_list[0][0], points_list[0][1], points_list[1][0], points_list[1][1])
        b = self.getDis(points_list[1][0], points_list[1][1], points_list[2][0], points_list[2][1])
        c = self.getDis(points_list[2][0], points_list[2][1], points_list[0][0], points_list[0][1])

        centerX = (a * points_list[0][0] + b * points_list[1][0] + c * points_list[2][0]) / (a + b + c)
        centerY = (a * points_list[0][1] + b * points_list[1][1] + c * points_list[2][1]) / (a + b + c)

        width, height, _ = srcImg.shape
        Intensity = 15 * 512 * 512 / (width * height)

        ddradius = float(radius * radius)
        copyImg = np.zeros(srcImg.shape, np.uint8)
        copyImg = srcImg.copy()

        K0 = Strength / 100.0

        eyeWidth = radius
        eyeHeight = self.getDis(
            (landmarks_node[startIndex + 1][0, 0] + landmarks_node[startIndex + 2][0, 0]) / 2,
            (landmarks_node[startIndex + 1][0, 1] + landmarks_node[startIndex + 2][0, 1]) / 2,
            (landmarks_node[midIndex + 1][0, 0] + landmarks_node[midIndex + 2][0, 0]) / 2,
            (landmarks_node[midIndex + 1][0, 1] + landmarks_node[midIndex + 2][0, 1]) / 2
        )
        centerX = ellipseEye[0][0]
        centerY = ellipseEye[0][1]
        ellipseA = ellipseEye[1][1]
        ellipseB = ellipseEye[1][0]
        ellipseC = math.sqrt(ellipseA * ellipseA - ellipseB * ellipseB)

        for i in range(width):
            for j in range(height):
                if self.getDis(i, j, centerX - ellipseC, centerY) + self.getDis(i, j, centerX + ellipseC, centerY) > 2 * ellipseA:
                    continue

                [crossX, crossY] = self.getEllipseCross(0, 0, i - ellipseEye[0][0], j - ellipseEye[0][1], ellipseEye[1][1],
                                                        ellipseEye[1][0], ellipseEye[0][0], ellipseEye[0][1])

                radius = self.getDis(centerX, centerY, crossX, crossY)
                ddradius = radius * radius
                distance = (i - centerX) * (i - centerX) + (j - centerY) * (j - centerY)
                K1 = 1.0 - (1.0 - distance / ddradius) * K0

                UX = (i - centerX) * K1 + centerX
                UY = (j - centerY) * K1 + centerY

                value = self.bilinear_insert(srcImg, UX, UY)
                copyImg[j, i] = value

        return copyImg
    
    def face_whiten(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            face_region = image[y:y+h, x:x+w]

            lower_reso = face_region.copy()
            for i in range(1):
                lower_reso = cv2.pyrDown(lower_reso)

            higher_reso = lower_reso.copy()
            for i in range(1):
                higher_reso = cv2.pyrUp(higher_reso)

            higher_reso = cv2.resize(higher_reso, (face_region.shape[1], face_region.shape[0]))
            laplacian = cv2.subtract(face_region, higher_reso)
            laplacian = cv2.convertScaleAbs(laplacian, alpha=1.5)

            contrasted_face = cv2.add(face_region, laplacian)
            image[y:y+h, x:x+w] = contrasted_face

        return image
    
    def face_bigeye(self, src, LStrength=20, RStrength = 25):
        landmarks = self.landmark_dec_dlib_fun(src)

        # 如果未检测到人脸关键点，就不进行瘦脸
        if len(landmarks) == 0:
            return

        for landmarks_node in landmarks:
            # print(landmarks_node)
            bigEyeImage = self.localTranslationWarp(src,36,41,LStrength,landmarks_node)
            bigEyeImage = self.localTranslationWarp(bigEyeImage,42,47,RStrength,landmarks_node)

        return bigEyeImage

    def face_smooth(self,image):
        if image is None:
            print("图像读取失败，请检查路径和文件名")
            return None

        dst = np.zeros_like(image)
        dx = 7 * 5  # 双边滤波的直径
        fc = 7 * 12.5  # 双边滤波的颜色和空间标准差
        p = 0.1  # 原图与处理图的权重比

        # 双边滤波用于平滑图像同时保持边缘清晰
        temp1 = cv2.bilateralFilter(image, dx, fc, fc)
        # 通过与原图相减获取高频部分，然后加上一个偏移增强边缘
        temp2 = cv2.subtract(temp1, image)
        temp2 = cv2.add(temp2, (10, 10, 10, 128))
        # 对高频部分使用高斯模糊
        temp3 = cv2.GaussianBlur(temp2, (2 * 4 - 1, 2 * 4 - 1), 0)
        # 将模糊后的高频部分叠加回原图
        temp4 = cv2.add(image, temp3)
        # 结合原图和处理后的图像，使用权重 p 和 1-p
        dst1 = cv2.addWeighted(image, p, temp4, 1 - p, 0.0)
        dst = cv2.add(dst1, (10, 10, 10, 255))
        return dst