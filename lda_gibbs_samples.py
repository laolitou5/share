#-*- coding: utf-8 -*-

import random
import time


class LdaGibbsSampler:
    def __init__(self, Data, K=20):
        self.D = Data  # 输入数据
        self.K = K
        self.V = 0
        self.M = len(self.D)
        self.alpha = 2
        self.beta = 0.5
        self.maxIter = 1000
        self.burnIn = 100
        self.sampleLag = 20
        self.ndsum = {}  # total number of words in document i
        self.nw = {}  # number of instances of word i (term?) assigned to topic j
        self.nd = {}  # number of words in document i assigned to topic j
        self.nwsum = {}  # total number of words assigned to topic j
        self.z = {}  # topic assignments for each word
        self.phisum = {}
        self.numstats = 0.0
        self.thetasum = {}
        self.run()

    def run(self):
        self.set_V() \
            .set_ND() \
            .set_NW() \
            .set_NWSUM() \
            .set_NDSUM()

    def set_NDSUM(self):
        for i in range(self.M):
            self.ndsum[i] = 0.0
        return self

    def set_NWSUM(self):
        for j in range(self.K):
            self.nwsum[j] = 0.0
        return self

    def set_NW(self):
        for i in range(self.V):
            self.nw[i] = {}
            for j in range(self.K):
                self.nw[i][j] = 0.0
        return self

    def set_ND(self):
        for i in range(self.M):
            self.nd[i] = {}
            for j in range(self.K):
                self.nd[i][j] = 0.0
        return self

    def set_M(self, value=0):
        self.M = value
        return self

    def set_V(self):
        Set = set()
        for s in self.D:
            Set = Set | set(s)
        self.V = len(Set)
        print("self.V =", self.V)
        return self

    def set_K(self, value):
        self.K = value
        return self

    def set_alpha(self, value):
        self.alpha = value
        return self

    def set_beta(self, value):
        self.beta = value
        return self

    def configure(self, iterations, burnIn, sampleLag):
        self.maxIter = iterations
        self.burnIn = burnIn
        self.sampleLag = sampleLag

    def set_thetasum(self):
        for m in range(self.M):
            self.thetasum[m] = {}
            for j in range(self.K):
                self.thetasum[m][j] = 0.0
        return self

    def set_phisum(self):
        for k in range(self.K):
            self.phisum[k] = {}
            for v in range(self.V):
                self.thetasum[k][v] = 0.0
                self.phisum[k][v] = 0.0  #修改后，添加
        return self

    def gibbs(self, alpha=2, beta=0.5):
        self.alpha = alpha
        self.beta = beta
        if self.sampleLag > 0:
            self.set_thetasum() \
                .set_phisum()
            self.numstats = 0.0
        self.initial_state()
        for i in range(self.maxIter):
            if i % 1000 == 0:
                print ("iteration", i, time.ctime())
            for m in range(len(self.z)):
                for n in range(len(self.z[m])):
                    print('前')
                    print(self.z[m][n])
                    print('后')
                    '''
                        self.z[m][n] 这里更新了文档m中第n个词的主题分布
                    '''
                    self.z[m][n] = self.sample_full_conditional(m, n)
                    print(self.z[m][n])
            '''
                self.burnIn 是指这个阶段的采样过程忽略不计
                It is common to ignore some number of samples at the beginning (the so-called burn-in period)
                self.sampleLag 这里的作用主要是用来控制更新的频率，并不是每次采样都进行参数的更新，而是隔一定的采样窗口之后 。
            '''
            if i > self.burnIn and self.sampleLag > 0 and i % self.sampleLag == 0:
                self.update_params()

    def sample_full_conditional(self, m, n):
        '''
            m                 文档编号
            n                 文档位置
            self.D[m][n]      对应相应的词编号
        '''
        topic = self.z[m][n]

        '''
            -1 这四个-1的作用是采样过程中去除本身词的影响
        '''
        self.nw[self.D[m][n]][topic] -= 1
        self.nd[m][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[m] -= 1

        '''
            p 这个字典产生的是当前这个位置(m,n)的主题分布，贝叶斯估计，假设对应的词是T
            p(k|T) =     ((T在主题k中的次数 + beta) / (主题k中的总词数 + V * beta))     --->p(T|k)
                       * ((文章中的主题k的次数 + alpha) / (文章总主题数(也是文章的总词数) + K * alpha))   --->p(k|d)
        '''
        p = {}
        for k in range(self.K):
            p[k] = (self.nw[self.D[m][n]][k] + self.beta) / (self.nwsum[k] + self.V * self.beta) * (
                        self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha)

        for k in range(1, len(p)): p[k] += p[k - 1]
        '''
            u 这里是按照概率分布来为第m个文章中的第n个词选择主题。
        '''
        u = random.random() * p[self.K - 1]
        for topic in range(len(p)):
            if u < p[topic]: break
        self.nw[self.D[m][n]][topic] += 1
        self.nd[m][topic] += 1
        self.nwsum[topic] += 1
        self.ndsum[m] += 1
        return topic

    def update_params(self):
        for m in range(len(self.D)):
            for k in range(self.K):
                '''
                    self.thetasum[m][k] 是文档m的主题k的概率累加值。
                                        = 文档的主题k的次数 / 文档的总主题数
                '''
                self.thetasum[m][k] += (self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha)
        for k in range(self.K):
            for w in range(self.V):
                '''
                    self.phisum[k][w] 是主题k-词组w的概率累加值 
                                      = 被分配为主题k的单词的次数 / 主题k包含的单词总数
                '''
                self.phisum[k][w] += (self.nw[w][k] + self.beta) / (self.nwsum[k] + self.V * self.beta)
        '''
            self.numstats 对于累加计算次数的统计
        '''
        self.numstats += 1

    def initial_state(self):
        for m in range(self.M):
            '''
                N代表当前文档的总词数
            '''
            N = len(self.D[m])
            self.z[m] = []
            for n in range(N):
                topic = int(random.random() * self.K)
                '''
                    self.z 记录了每个文档的主题分布，初始时为文本中的每个单词随机的分配主题
                '''
                self.z[m].append(topic)

                '''
                    self.nw 是对应的词组-主题矩阵， 不过这里记录的是每个词组在主题中出现的次数
                '''
                self.nw[self.D[m][n]][topic] = self.nw[self.D[m][n]].get(topic, 0) + 1

                '''
                    self.nd 是对应的文档-主题矩阵，这里也是文档的主题出现的次数
                '''
                self.nd[m][topic] = self.nd[m].get(topic, 0) + 1

                '''
                    self.nwsum  是每个topic下的总词数
                '''
                self.nwsum[topic] = self.nwsum.get(topic, 0) + 1

                n += 1
            '''
                self.ndsum 每个文档对应的总词数
            '''
            self.ndsum[m] = N

            m += 1

    def get_theta(self):
        '''
            theta 对应于文档-主题分布矩阵
        '''
        theta = {}
        for m in range(self.M):
            theta[m] = {}
            for k in range(self.K):
                theta[m][k] = 0
        if self.sampleLag > 0:
            for m in range(self.M):
                for k in range(self.K):
                    theta[m][k] = self.thetasum[m][k] / self.numstats
        else:
            for m in range(self.M):
                for k in range(self.K):
                    theta[m][k] = (self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha);
        return theta

    def get_phi(self):
        '''
            phi 对应于主题-词组分布矩阵
        '''
        phi = {}
        for k in range(self.K):
            phi[k] = {}
            for v in range(self.V):
                phi[k][v] = 0
        if self.sampleLag > 0:
            for k in range(self.K):
                for v in range(self.V):
                    phi[k][v] = self.phisum[k][v] / self.numstats
        else:
            for k in range(self.K):
                for v in range(self.V):
                    phi[k][v] = (self.nw[k][v] + self.alpha) / (self.nwsum[k] + self.K * self.alpha);
        return phi


if __name__ == '__main__':
    documents = [
        [1, 4, 3, 2, 3, 1, 4, 3, 2, 3, 1, 4, 3, 2, 3, 6],
        [2, 2, 4, 2, 4, 2, 2, 2, 2, 4, 2, 2],
        [1, 6, 5, 6, 0, 1, 6, 5, 6, 0, 1, 6, 5, 6, 0, 0],
        [5, 6, 6, 2, 3, 3, 6, 5, 6, 2, 2, 6, 5, 6, 6, 6, 0],
        [2, 2, 4, 4, 4, 4, 1, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 0],
        [5, 4, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2]
    ]
    lda = LdaGibbsSampler(documents, 5)
    lda.configure(10000, 2000, 10)
    lda.gibbs()
    theta = lda.get_theta()
    print(theta)