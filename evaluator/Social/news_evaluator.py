from random import randint

from config.cst import *
from evaluator.Dispatchers.TwitterDispatcher import TwitterDispatcher
from evaluator.Social.social_evaluator import NewsSocialEvaluator
from evaluator.evaluator_dispatcher import *


class TwitterNewsEvaluator(NewsSocialEvaluator, EvaluatorDispatcherClient):
    def __init__(self):
        NewsSocialEvaluator.__init__(self)
        EvaluatorDispatcherClient.__init__(self)
        self.enabled = True
        self.is_threaded = False
        self.count = 0
        self.symbol = ""

    def set_dispatcher(self, dispatcher):
        super().set_dispatcher(dispatcher)
        self.dispatcher.update_social_config(self.social_config)

    def get_data(self):
        pass

    @staticmethod
    def get_dispatcher_class():
        return TwitterDispatcher

    def get_twitter_service(self):
        return self.config[CONFIG_CATEGORY_SERVICES][CONFIG_TWITTER][CONFIG_SERVICE_INSTANCE]

    def print_tweet(self, tweet, count):
        self.logger.debug(str(count) + " : " + str(self.symbol) + " : " + tweet)

    def receive_notification_data(self, data):
        self.count += 1
        self.print_tweet(data[CONFIG_TWEET_DESCRIPTION], self.count)

    def eval_impl(self):
        # self.notify_evaluator_threads(self.__class__.__name__)
        pass

    def run(self):
        pass

    def is_interested_by_this_notification(self, notification_description):
        # true if in twitter accounts
        for account in self.social_config[CONFIG_TWITTERS_ACCOUNTS][self.symbol]:
            if account.lower() in notification_description:
                return True

        if notification_description.startswith("rt"):
            return False

        # true if contains symbol
        if self.symbol.lower() in notification_description:
            return True

        # true if in hashtags
        for hashtags in self.social_config[CONFIG_TWITTERS_HASHTAGS][self.symbol]:
            if hashtags.lower() in notification_description:
                return True
        return False

    def purify_config(self):
        # remove other symbols data to avoid unnecessary tweets
        if self.symbol in self.social_config[CONFIG_TWITTERS_ACCOUNTS]:
            self.social_config[CONFIG_TWITTERS_ACCOUNTS] = \
                {self.symbol: self.social_config[CONFIG_TWITTERS_ACCOUNTS][self.symbol]}
        else:
            self.social_config[CONFIG_TWITTERS_ACCOUNTS] = {}
        if self.symbol in self.social_config[CONFIG_TWITTERS_HASHTAGS]:
            self.social_config[CONFIG_TWITTERS_HASHTAGS] = \
                {self.symbol: self.social_config[CONFIG_TWITTERS_HASHTAGS][self.symbol]}
        else:
            self.social_config[CONFIG_TWITTERS_HASHTAGS] = {}

    def prepare(self):
        self.purify_config()


class MediumNewsEvaluator(NewsSocialEvaluator):
    def __init__(self):
        super().__init__()
        self.enabled = False
        self.is_threaded = False

    def get_data(self):
        pass

    def eval_impl(self):
        self.notify_evaluator_threads(self.__class__.__name__)

    def run(self):
        pass

    def set_default_config(self):
        self.social_config = {
            CONFIG_REFRESH_RATE: 2
        }
