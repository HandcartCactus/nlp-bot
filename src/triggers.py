"""
Intended for bot triggers and related classes
"""
import os
import time
from datetime import datetime, timedelta
from twitter import TwitterError


class MentionsIDStorage(object):
    def __init__(self, filepath):
        """
        Manages the latest mentions tweet id.
        Remember latest tweet even after shutdown, so you don't annoy everybody.

        Args:
            filepath (str): path to a file to store the id. File doesnt have to exist, but the directory it's in does.
        """
        self.filepath = filepath
        self._build_if_ne(filepath)
        
    def _build_if_ne(self, filepath):
        """Builds the file if it doesn't exist.

        Args:
            filepath (str): filepath

        Raises:
            Error: Couldn't build your file. Probably one or more directories referenced don't exist.
        """
        if not os.path.exists(filepath):
            with open(filepath, 'w') as _: 
                pass
    
    def _file_to_id(self, file):
        """Parse the file for the id and return the id

        Args:
            file : file object
        Returns:
            int: the id of the latest tweet mentioning your bot
        """
        # may need to be str
        return int(file.readlines()[0])
    
    def get_id(self):
        """Return the mentions id

        Returns:
            int: the id of the latest tweet id you collected that mentions your bot
        """
        val = None
        with open(self.filepath, 'r') as file:
            val = self._file_to_id(file)
        return val 
    
    def set_id(self, new_id):
        """set the tweet id

        Args:
            new_id (str or castable to str): the latest tweet id you collected that mentions your bot
        """
        with open(self.filepath, 'w') as file:
            new_id = str(new_id)
            file.write(new_id)


class MentionsListener(object):
    def __init__(self, api, mentions_id_fpath, ignore_all_before=False):
        """Listen for mentions

        Args:
            api (twitter.Api): The twitter api object
            mentions_id_fpath (str): where to get or store the most recent mentions id
            ignore_all_before (bool): Ignore mentions that happened since before you started running. 
        """
        self.api = api
        self.mids = MentionsIDStorage(mentions_id_fpath)
        self.ignore_all_before = ignore_all_before

    def msg(self, s, verbose=True):
        if verbose:
            print(s)

    def ignore_mentions_before_now(self):
        mentions = self.api.GetMentions()
        most_recent_id = mentions[0].id
        self.mids.set_id(most_recent_id)

    def listen(self, query_wait_s=30, cooldown_wait_m=15, expire_in=None, verbose=False):
        """
        Yield any new tweets mentioning your bot. (Runs indefinitely, if you desire.)
        Limited to 70 queries every 15m, and 100,000 every 24h.
        Args:
            query_wait_s (int, optional): How many seconds to wait between asking twitter for new mentions. Defaults to 30.
                Least you should go is 12s, any less than that and you'll get rate limited.
            cooldown_wait_m (int, optional): How many minutes to wait after you get rate limited. Defaults to 15m. 
            expire_in (timedelta, optional): How long to run before killing the listener. Example: timedelta(hours=5). Defaults to never expire.
            verbose (bool): Print messages about the status of your loop.

        Yields:
            twitter.Status: Any tweets mentioning your bot as a twitter.Status object
        """
        if self.ignore_all_before:
            self.ignore_mentions_before_now()

        will_expire = not expire_in is None
        if will_expire:
            start_at = datetime.now()

        while True:
            # exit the loop if running for longer than expire time
            if will_expire:
                elapsed_time = datetime.now() - start_at
                self.msg(f'Time Elapsed {elapsed_time}', verbose)

                if elapsed_time > expire_in:
                    self.msg('Expiring now!', verbose)
                    break

            # get the most recent mentions id
            last_id = self.mids.get_id()

            # Get mentions, no mentions by default
            mentions = []
            try:
                mentions = self.api.GetMentions(since_id=last_id)

            except TwitterError:
                # We hit the rate limit. Cool down for a while. 
                self.msg('Hit rate limit :(', verbose)
                time.sleep(60 * cooldown_wait_m)

            if len(mentions) > 0:
                self.msg('New Mentions!\n', verbose)
                # if there are new mentions, store the most recent id
                most_recent_id = sorted(mentions, key=lambda status: -status.id)[0].id
                self.mids.set_id(most_recent_id)

                for mention in mentions:
                    self.msg(f'\t{mention}', verbose)
                    yield mention

            # wait to avoid hitting the rate limit
            time.sleep(query_wait_s)