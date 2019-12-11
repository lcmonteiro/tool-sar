# -*- coding: utf-8 -*-

import operator as op
import numpy as nm


class Math:

    def __init__(self):
        pass

#static
    @staticmethod
    def Max(data):
        maximumV = 0.0
        maximumI = 0
        maximumJ = 0
        for i in xrange(len(data)):
            for j in xrange(len(data[i])):
                if maximumV < data[i][j]:
                    maximumV = data[i][j]
                    maximumI = i
                    maximumJ = j
        return [maximumV, (maximumI, maximumJ)]

    @staticmethod
    def Rotate(data):
        return map(list, zip(*data))

    @staticmethod
    def Derive(data):
        return map(op.sub, data[1:] + data[-1:], data)

    @staticmethod
    def Integral(data):
        out = []
        acc = 0
        for d in data:
            acc += d
            out.append(acc)
        return out

    @staticmethod
    def Integral2(data, func=lambda x: 100 / x if x != 0 else 0):
        out = []
        acc = 0
        for d in data:
            acc += (d - func(acc))
            out.append(acc)
        return out

    @staticmethod
    def Integral3(data, factor):
        out = []
        acc = 0
        for d, f in zip(data, factor):
            acc += d
            if acc < 0:
                acc += f
                out.append(acc if acc < 0 else 0)

            else:
                acc -= f
                out.append(acc if acc > 0 else 0)
        return out

    @staticmethod
    def Smooth(data, factor):
        out = []
        acc = nm.mean(data[:10])
        for d in data:
            acc = (acc * factor) + (d * (1 - factor))
            out.append(acc)
        return out

    @staticmethod
    def Smooth2(data, factor):
        out = []
        acc = 0
        for d in data:
            if d < acc:
                acc = (acc * factor) + (d * (1 - factor))
            else:
                acc = d
            out.append(acc)
        return out

    @staticmethod
    def Smooth3(data, mag, size, order):
        out = []
        count = 0
        for d in data:
            if d:
                count = 0
            v = mag - ((float(mag) / pow(size, order)) * pow(count, order))
            out.append(v if v > 0 else 0)
            count += 1
        return out

    @staticmethod
    def Smooth4(data, mag, size, order):
        out = []
        count = 0
        for d in data:
            if d:
                count = 0
            out.append((float(mag) / pow(size, order)) * pow(count, order))
            count += 1
        return out

    @staticmethod
    def Filter(data, factor1=0.99, factor2=0.9):
        return map(
            op.sub,
            Math.Smooth(data, factor2),
            Math.Smooth(data, factor1)
        )

    @staticmethod
    def Reduce(data, setp, window):
        return [
            sum(data[i:i + window]) / window
            for i in range(0, len(data) - window, setp)
        ]

    @staticmethod
    def Reduce2(data, setp, window):
        return [
            nm.mean(data[:((i * 2) + 1)])
            for i in range(0, window / 2, setp)
        ] + [
            nm.mean(data[i:i + window])
            for i in range(setp, len(data) - window, setp)
        ] + [
            nm.mean(data[((i * 2) + 1):])
            for i in range(-window / 2, 0, setp)
        ]

    @staticmethod
    def CutCoFloat(data):
        out = []
        for a in data:
            m = min(map(abs, a))
            out.append(map(lambda x: x + m if x < 0 else x - m, a))
        return out

    @staticmethod
    def CoFloat(data, factor):
        out = []
        acc = list(data[0])
        acc_p = nm.prod(data[0])

        for a in data:
            acc_p = (acc_p * factor) + (nm.prod(a) * (1 - factor))

            for i in range(len(a)):
                acc[i] = (acc[i] * factor) + (a[i] * (1 - factor))
            out.append(acc_p - nm.prod(acc))
        return out

    @staticmethod
    def  WaveletT(data):
        out = []
        count = 1

        while len(data):
            count <<= 1
            diff = []
            mean = []
            for i, j in zip(range(0, len(data), 2), range(1, len(data), 2)):
                diff.append((data[i] - data[j]) / 2)
                mean.append((data[i] + data[j]) / 2)
            tmp = []
            for d in diff:
                for i in range(count):
                    tmp.append(d)
            out.append(tmp)
            data = mean
        return out

    @staticmethod
    def WaveletT2(data):
        out = []
        count = 1
        buff = data
        while len(buff):
            diff = []
            mean = []
            for i, j in zip(range(0, len(buff), 2), range(1, len(buff), 2)):
                d = (buff[i] - buff[j]) / 2
                for c in range(count):
                    diff.append(d)
                for c in range(count):
                    diff.append(-d)
                mean.append((buff[i] + buff[j]) / 2)
            if len(diff) == 0:
                for c in range(count):
                    diff.append(buff[0])
            for c in range(len(data) - len(diff)):
                diff.append(0)
            out.append(diff)
            buff = mean
            count <<= 1
        return out

    @staticmethod
    def Cov(d):
        return nm.mean(map(nm.prod, Math.Rotate(d))) - nm.prod(map(nm.mean, d))

    @staticmethod
    def CorrCoef(d1):
        return nm.corrcoef(d1)

    @staticmethod
    def Corr(data):
        try:
            diff = [
                [s - m for s in d] for d, m in zip(data, [nm.mean(d) for d in data])
            ]
            return sum(
                map(nm.prod, Math.Rotate(diff))
            ) / nm.sqrt(nm.prod(
                map(sum, map(lambda x: map(lambda y: pow(y, 2), x), diff))
            ))
        except:
            return 0

    @staticmethod
    def MatrixCorr(data1, data2):
        cm = []
        for d1 in data1:
            r = []
            for d2 in data2:
                c = Math.Corr([d1, d2])
                if nm.isnan(c):
                    r += [0.0]
                else:
                    r += [c]
            cm += [r]
        return cm

    @staticmethod
    def Corr2(d):
        return Math.Cov(d) / nm.prod(
            map(lambda x: pow(Math.Cov([x, x]), 0.5), d)
        )

    @staticmethod
    def RMS(d):
        return nm.sqrt(nm.mean(nm.array(d) ** 2))

    @staticmethod
    def Regression(y, x):
        x += [[1 for i in xrange(len(y))]]
        A = nm.array(x)
        Y = nm.array(y)
        w = nm.linalg.lstsq(A.T, Y)
        return list(w[0])

    @staticmethod
    def Weights(y):
        s = sum(y)
        return [float(v) / s for v in y]

    @staticmethod
    def Weights2(y):
        m = min(y)
        return Math.Weights([v - m for v in y])

    @staticmethod
    def Gravity(pos, weights, ignor=0, alpha=0.1):
        pos_next = pos[0:ignor]
        for p_w, p_ref in zip(weights[ignor:], pos[ignor:]):
            p_tmp = [0.0, 0.0]
            for w, p in zip(p_w, pos):
                p_tmp[0] += w * p[0]
                p_tmp[1] += w * p[1]
            p_tmp[0] = p_ref[0] + alpha * ((p_tmp[0] - p_ref[0]))
            p_tmp[1] = p_ref[1] + alpha * ((p_tmp[1] - p_ref[1]))
            pos_next += [p_tmp]
        return pos_next

    @staticmethod
    def Gravity2(pos, weights, ignor=0, alpha=1.0):
        pos_next = pos[0:ignor]
        for p_w, p_ref in zip(weights[ignor:], pos[ignor:]):
            p_tmp = [0.0 for i in xrange(len(p_ref))]
            for w, p in zip(p_w, pos):
                for i in xrange(len(p_ref)):
                    p_tmp[i] += w * p[i]
            diff = [t - r for t, r in zip(p_tmp, p_ref)]
            beta = pow(sum([pow(d, 2) for d in diff]), 0.5)
            pos_next += [[r + alpha * beta * d for r, d in zip(p_ref, diff)]]
        return pos_next

    @staticmethod
    def Gravity3(pos, weights, ignor=0, alpha=1.0):
        pos_next = pos[0:ignor]
        for p_w, p_ref in zip(weights[ignor:], pos[ignor:]):
            p_tmp = [0.0 for i in xrange(len(p_ref))]
            for w, p in zip(p_w, pos):
                for i in xrange(len(p_ref)):
                    p_tmp[i] += w * p[i]
            diff = [t - r for t, r in zip(p_tmp, p_ref)]
            beta = sum([pow(d, 2) for d in diff])
            pos_next += [[r + alpha * beta * d for r, d in zip(p_ref, diff)]]
        return pos_next

    @staticmethod
    def Entropy(var, factor=1.0):
        hist = {}
        for i in [int(v * factor) for v in var]:
            if i in hist:
                hist[i] += 1.0
            else:
                hist[i] = 1.0
        entropy = 0.0
        for p in [hist[k] / len(var) for k in hist]:
            entropy += p * nm.log(p)
        return -entropy

    @staticmethod
    def Basis(var, keep=0.9):
        svd = nm.linalg.svd(nm.cov(nm.matrix(var).transpose()))
        Sref = sum(svd[1]) * keep
        Si = 0.0
        i = 0
        for s in svd[1]:
            Si += s
            i += 1
            if Si >= Sref:
                return svd[0].transpose()[:i].transpose()
        return svd[0]


if __name__ == '__main__':
    def test1():
        a = [
            [
                1, 2, -30, 4
            ] * 1,
            [
                5, 6, 90, 8
            ] * 1,
            [
                5, 6, 90, 8
            ] * 1
        ]
        print(Math.Corr(a))
        print(Math.Corr2(a))

    def test2():
        a = [
            [
                -1, -2, -3, -4
            ] * 10,
            [
                1, 2, 3, 4
            ] * 5,
        ]
        print(Math.Corr(a))
        print(Math.Corr2(a))

    def test3():
        a = nm.matrix([
            [1, 1],
            [2, 2],
            [3, 3]
        ])
        print(a)
        print(a * Math.Basis(a))
        print(a * Math.Basis(a) * Math.Basis(a).transpose())
# execute
    test3()