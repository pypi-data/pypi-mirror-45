import numpy as np


class LdaCollapsedGibbs:
    def __init__(self, K=25, alpha=0.5, beta=0.5, docs=None, V=None):
        """
        Create the model with given parameters
        :param K: num of topics
        :param alpha: Dirichlet hyper-parameter
        :param beta: Dirichlet hyper-parameter
        :param docs:
        :param V:
        """



        """
        
        K : , integer
        alpha: , if None set it to 1/K
        beta:  if None set it to 1/K
        docs: document in the format of lists of integers: [[1,2,3,4,5,1,2], [2,4,5,1]] is two documents with 7 and 4 words respectively.
        V: vocabulary length
        The goal of the function is to initialize the internal variables of the class that are those provided and the counter variables described in the pseudocode.
        """

        self.K = K
        self.alpha = alpha  # parameter of topics prior
        self.beta = beta  # parameter of words prior
        self.docs = docs  # a list of lists, each inner list contains the indexes of the words in a doc, e.g.: [[1,2,3],[2,3,5,8,7],[1, 5, 9, 10 ,2, 5]]
        self.V = V  # how many different words in the vocabulary i.e., the number of the features of the corpus
        # Definition of the counters
        self.z_m_n = []  # topic assignements for each of the N words in the corpus. N: total number od words in the corpus (not the vocabulary size).
        self.n_m_z = np.zeros(
            (len(self.docs), K)) + alpha  # |docs|xK topics: number of words assigned to topic z in document m
        self.n_z_t = np.zeros((K, V)) + beta  # (K topics) x |V| : number of times a word v is assigned to a topic z
        self.n_z = np.zeros(K) + V * beta  # (K,) : overal number of words assigned to a topic z

        self.N = 0
        for m, doc in enumerate(docs):  # Initialization of the data structures I need.
            self.N += len(doc)  # to find the size of the corpus
            z_n = []
            for t in doc:
                z = np.random.randint(0,
                                      K)  # Randomly assign a topic to a word. Recall, topics have ids 0 ... K-1. randint: returns integers to [0,K[
                z_n.append(z)  # Keep track of the topic assigned
                self.n_m_z[m, z] += 1  # increase the number of words assigned to topic z in the m doc.
                self.n_z_t[z, t] += 1  # .... number of times a word is assigned to this particular topic
                self.n_z[z] += 1  # increase the counter of words assigned to z topic
            self.z_m_n.append(np.array(
                z_n))  # update the array that keeps track of the topic assignements in the words of the corpus.

    def fit(self, iters=10):
        """
        :param iters: number of times to run the sampling procedure
        """
        for _ in range(iters):
            self._inference()

    def _inference(self):
        """    The learning process. Code only one iteration over the data.
               In the main function a loop will be calling this function.
        """
        for m, doc in enumerate(self.docs):
            z_n, n_m_z = self.z_m_n[m], self.n_m_z[m]
            for n, t in enumerate(doc):
                z = z_n[n]
                n_m_z[z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1
                # sampling topic new_z for t
                p_z = (self.n_z_t[:, t] + self.beta) * (n_m_z + self.alpha) / (
                        self.n_z + self.V * self.beta)  # A list of len() = # of topic
                new_z = np.random.multinomial(1,
                                              p_z / p_z.sum()).argmax()  # One multinomial draw, for a distribution over topics, with probabilities summing to 1, return the index of the topic selected.
                # set z the new topic and increment counters
                z_n[n] = new_z
                n_m_z[new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def get_params(self):
        """
        :return: document-topic distribution (D, K), topic-word distribution (K, V)
        """
        dt_dist = self.n_m_z / self.n_m_z.sum(axis=1)[:, np.newaxis]
        tw_dist = self.n_z_t / self.n_z[:, np.newaxis]
        return dt_dist, tw_dist

    def perplexity(self):
        """
        Model perplexity given test set
        https://github.com/JerryZhong/LDA/blob/master/src/model.cpp#L1125
        """
        pass
