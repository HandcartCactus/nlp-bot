from datetime import datetime, timedelta
import argparse
import configparser
import os
import copy

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import twitter
import numpy as np

import corpus
import commands
import utils

class TweetTimes(commands.Command):
    """
    wh: day of week / hours
    or
    pol: part of life
    """
    def __init__(self, api, tweet_id, config, user_id, options_string=None):
        self.DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        self.POL_DAYS = {'Weekends':['Sat','Sun'], 'Weekdays':['Mon','Tue','Wed','Thu','Fri']}
        self.POL_DAYS_CT = {pol:len(days) for pol,days in self.POL_DAYS.items()}
        self.DAYS_2_POL = {'Sat': 'Weekends', 'Sun': 'Weekends', 'Mon': 'Weekdays', 'Tue': 'Weekdays', 'Wed': 'Weekdays', 'Thu': 'Weekdays', 'Fri': 'Weekdays'}
        self.POL_HOURS = {'6-9am':[6,7,8,9],'10am-1pm':[10,11,12,13],'2-5pm':[14,15,16,17],'6-9pm':[18,19,20,21],'10pm-1am':[22,23,0,1],'2-5am':[2,3,4,5]}
        self.POL_HOURS_CT = {pol:len(hours) for pol,hours in self.POL_HOURS.items()}
        self.HOURS_2_POL = {6: '6-9am', 7: '6-9am', 8: '6-9am', 9: '6-9am', 10: '10am-1pm', 11: '10am-1pm', 12: '10am-1pm', 13: '10am-1pm', 14: '2-5pm', 15: '2-5pm', 16: '2-5pm', 17: '2-5pm', 18: '6-9pm', 19: '6-9pm', 20: '6-9pm', 21: '6-9pm', 22: '10pm-1am', 23: '10pm-1am', 0: '10pm-1am', 1: '10pm-1am', 2: '2-5am', 3: '2-5am', 4: '2-5am', 5: '2-5am'}
        self.tweets = None
        super(TweetTimes, self).__init__(api, tweet_id, config, user_id, options_string)

    def load_tweets(self):
        if self.tweets is None:
            self.tweets = corpus.get_max_tweets(self.api, self.user_id)
    
    def get_timestamps(self):
        self.load_tweets()
        return [self.parse_dt_str(tweet.created_at) for tweet in self.tweets]

    def parse_dt_str(self, dt_str):
        return datetime.strptime(dt_str, '%a %b %d %H:%M:%S %z %Y')

    def ts2wh(self, t):
        return t.strftime('%a'), int(t.strftime('%H'))

    def ts2pol(self, t):
        day, hour = self.ts2wh(t)
        return self.DAYS_2_POL[day], self.HOURS_2_POL[hour]

    def get_weekhrs(self):
        ts = self.get_timestamps()
        wh = [self.ts2wh(t) for t in ts]
        return wh

    def tweets_by_week_hour(self):
        x = self.get_weekhrs()

        chart = {d:[0]*24 for d in self.DAYS}
        for day, hour in x:
            chart[day][hour] += 1
        
        arr = [chart[day] for day in self.DAYS]

        return arr

    def get_pol(self):
        ts = self.get_timestamps()
        pairs = [self.ts2pol(t) for t in ts]
        return pairs

    def avg_hrly_tweets_by_pol(self):
        pol_pairs = self.get_pol()
        chart = {d:{h:0 for h in self.POL_HOURS.keys()} for d in self.POL_DAYS.keys()}
        
        for pol_d, pol_h in pol_pairs:
            days_in_pol = self.POL_DAYS_CT[pol_d]
            hours_in_pol = self.POL_HOURS_CT[pol_h]
            chart[pol_d][pol_h] += 1/(days_in_pol * hours_in_pol)
        
        arr = [[v for v in chart[pol_d].values()] for pol_d in chart.keys()]
        return arr

    def get_dir_for_img(self):
        mydir = self.config['TweetTimes_Dir']
        subdir = os.path.join(mydir, str(self.user_id))
        return subdir

    def make_filesystem(self):
        subdir = self.get_dir_for_img()
        if not os.path.exists(subdir):
            os.mkdir(subdir)

    def plot_save_ahtbp(self):
        subdir = self.get_dir_for_img()
        fname = self.config['TweetTimes_POL_fname']
        full_path = os.path.join(subdir, fname)
        self.make_filesystem()
        arr = self.avg_hrly_tweets_by_pol()

        y_axis_labels = self.POL_DAYS.keys()
        y_axis_values = list(range(len(y_axis_labels)))

        x_axis_labels = self.POL_HOURS.keys()
        x_axis_values = list(range(len(x_axis_labels))) 

        cmap = copy.copy(plt.cm.gray)
        cmap.set_under(color='black')

        plt.figure(figsize=(7,7))
        ax = plt.gca()
        im = ax.imshow(arr,cmap=cmap,vmin=0.25)
        plt.yticks(y_axis_values, y_axis_labels)
        plt.xticks(x_axis_values, x_axis_labels)
        plt.title('Hourly average tweets by pattern of life\n(Up to 200 most recent tweets)')

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.09)
        plt.colorbar(im, cax=cax)

        plt.savefig(full_path)
        
    def plot_save_wh(self):
        subdir = self.get_dir_for_img()
        fname = self.config['TweetTimes_WH_fname']
        full_path = os.path.join(subdir, fname)
        self.make_filesystem()
        arr = self.tweets_by_week_hour()

        x_axis_values = [i for i in range(0,24,3)]
        x_axis_labels = ['12 am', '3 am', '6 am', '9 am', '12 pm', '3 pm', '6 pm', '9 pm']
    
        y_axis_values = list(range(len(self.DAYS)))
        y_axis_labels = self.DAYS

        cmap = copy.copy(plt.cm.Reds_r)
        cmap.set_under(color='black')

        plt.figure()
        ax = plt.gca()
        im = ax.imshow(arr,cmap=cmap,vmin=0.5)
        plt.yticks(y_axis_values, y_axis_labels)
        plt.xticks(x_axis_values, x_axis_labels)
        plt.title('Tweets by weekday and hour\n(Up to last 200 tweets)')

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.09)
        plt.colorbar(im, cax=cax)

        plt.savefig(full_path)

    def get_statistics_s(self):
        dts = self.get_timestamps()
        time_span = np.max(dts)-np.min(dts)
        tps = len(dts)/time_span.total_seconds()
        diffs = np.diff(np.sort(dts))
        d_s = np.array([delta.total_seconds() for delta in diffs])
        std = np.std(d_s)
        mean = np.mean(d_s)
        return tps, mean, std
    
    def get_statistics(self):
        tps, mean, std = self.get_statistics_s()
        tps = find_sensible_unit(tps, multiply_mode=True)
        mean = find_sensible_unit(mean)
        std = find_sensible_unit(std)
        return tps, mean, std
    
    def describe_statistics(self, p=.95):
        """Describe tweet stats

        Args:
            p (float, optional): ratio of posts that fall within time range. 0<p<1. Defaults to .95.
        """
        p = float(p)

        tps_s, mean_s, std_s = self.get_statistics_s()
        tps, mean, std = self.get_statistics()

        tps_u, tps_v = tps
        mean_u, mean_v = mean
        std_u, std_v = std

        k = np.sqrt(1/(1 - p))

        max_e_s = mean_s + k*std_s
        next_post_by_dt = datetime.now() + timedelta(seconds=max_e_s)
        next_post_by_str = next_post_by_dt.strftime('%a %b %d %Y, %I:%M %p')
        max_e_u, max_e_v = find_sensible_unit(max_e_s)

        arr = np.array(self.avg_hrly_tweets_by_pol())
        d_idx, h_idx = np.unravel_index(arr.argmax(), arr.shape)
        pol_days = list(self.POL_DAYS.keys())[d_idx]
        pol_hours = list(self.POL_HOURS.keys())[h_idx]
        aht = arr[d_idx][h_idx]

        a = ""
        a += f"In your last 200 tweets, your most active time was {pol_days} {pol_hours}. You averaged {aht:0.1f} tweets per hour during that time period.\n"
        a += f"Generally, in your last 200 tweets, you averaged about {tps_v:0.0f} tweets per {tps_u}, with a mean wait time of {mean_v:0.1f} {mean_u}s and stdv of {std_v:0.1f} {std_u}s.\n"
        a += f"At the time of any new tweet, there is at least a {p:0.2%} chance you will tweet again within {max_e_v:0.1f} {max_e_u}s. I predict your next post will be before {next_post_by_str}.\n"
        
        return a


    def run(self):
        subdir = self.get_dir_for_img()
        wh_fname = self.config['TweetTimes_WH_fname']
        wh_full_path = os.path.join(subdir, wh_fname)
        pol_fname = self.config['TweetTimes_POL_fname']
        pol_full_path = os.path.join(subdir, pol_fname)
        desc = self.describe_statistics(self.config['TweetTimes_p'])
        
        self.plot_save_ahtbp()
        self.plot_save_wh()

        return pol_full_path, wh_full_path, desc

    def send_single_rt(self, message, tweet_id, media=None):
        a = self.api.PostUpdate(
            status=message,
            media=media,
            in_reply_to_status_id=self.tweet_id, 
            auto_populate_reply_metadata=True
        )
        return a

    def __repr__(self):
        return "TweetTimes Command"

    def reply_tweet(self):
        pol_fp, wh_fp, desc = self.run()
        tweet_id = self.tweet_id
        tweets = utils.split_string(desc)
        for idx, tweet_txt in enumerate(tweets):
            if idx==0:
                media = [pol_fp, wh_fp]
            else:
                media = None
            last_tweet = self.send_single_rt(tweet_txt, tweet_id, media=media)
            tweet_id = last_tweet.id

            

def find_sensible_unit(value, unit_scale_dict=None, multiply_mode=False):
    if unit_scale_dict is None:
        unit_scale_dict = {
            'second':1,
            'minute':60,
            'hour':60*60,
            'day':60*60*24,
            'week':60*60*24*7,
            'month':60*60*24*30.436,
            'year':60*60*24*364.75,
        }
        
    if multiply_mode:
        v_dict = {k:value*v for k,v in unit_scale_dict.items()}
    else:
        v_dict = {k:value/v for k,v in unit_scale_dict.items()}
    
    sensible_unit = None
    unit_value = np.infty
    for unit, value in v_dict.items():
        if value >= 1 and value<unit_value:
            sensible_unit = unit
            unit_value = value
            
    return sensible_unit, unit_value


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='configuration file')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    keys = config['Twitter Keys']

    api = twitter.Api(
        consumer_key=keys['API_Key'],
        consumer_secret=keys['API_Secret_Key'],
        access_token_key=keys['Access_Token'],
        access_token_secret=keys['Access_Token_Secret'],
        tweet_mode="extended",
    )

    tweet_id = 1375406548747440129
    user_id = 939091

    t = TweetTimes(api, tweet_id, config=config['Commands'], user_id=user_id)
    t.reply_tweet()