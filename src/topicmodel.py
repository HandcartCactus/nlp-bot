from corextopic import corextopic as ct
import corextopic.vis_topic as vt
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from commands import Command
import corpus

class TopicModelCorEx(Command):
    n_features=20000
    n_topics = 3

    def parse_options(self):
        if not self.options_string is None:
            opts = self.options_string.split(' ')
            print(opts)
            if 'n_topics' in opts:
                print('topics!')
                idx = opts.index('n_topics')
                print(idx)
                try:
                    self.n_topics = int(opts[idx+1])
                    print(opts[idx+1])
                except:
                    pass

            if 'n_features' in opts:
                idx = opts.index('n_features')
                try:
                    self.n_features = int(opts[idx+1])
                except:
                    pass

    def get_tweets(self):
        return corpus.tweet_corpus(self.api, self.user_id)

    def set_word_doc_model(self):
        self.docs = self.get_tweets()
        self.tf_vectorizer = CountVectorizer(
            max_df=0.95, 
            min_df=2, 
            max_features=self.n_features, 
            stop_words='english'
        )
        self.tf = self.tf_vectorizer.fit_transform(self.docs)
        self.tf_feature_names = self.tf_vectorizer.get_feature_names()
        self.words = list(np.asarray(self.tf_feature_names))

    def set_topic_model(self):
        self.set_word_doc_model()
        self.topic_model = ct.Corex(
            n_hidden=self.n_topics, 
            words=self.words, 
            max_iter=200, 
            verbose=False
        )
        self.topic_model.fit(self.tf, words=self.words)

    def get_words(self, topic_no, n_words=15, trim=True):
        t = self.topic_model.get_topics(topic=topic_no, n_words=n_words)
        w = " ".join([w[0] for w in t])
        w = f"Topic {topic_no}: {w}"
        if trim:
            w = w[:139]
        return w+"\n"

    def send_single_rt(self, message, tweet_id):
        a = self.api.PostUpdate(
            status=message, 
            in_reply_to_status_id=self.tweet_id, 
            auto_populate_reply_metadata=True
        )
        return a

    def reply_tweet(self):
        self.parse_options()
        self.set_topic_model()
        tweet_id = self.tweet_id
        for i in range(self.n_topics):
            m = self.get_words(i)
            my_tweet = self.send_single_rt(m, tweet_id)
            tweet_id = my_tweet.id
    
    def __repr__(self):
        return "TopicModelCorEx Command"