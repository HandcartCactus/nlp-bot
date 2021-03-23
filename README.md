# TwitterBot
Code relating to my twitter bot, which can be found [here](https://twitter.com/WhatDoITweetBot). (The bot and the template are both WIP.)

## Setup
### Fork it!
Fork it.
### API Tokens
Get your [Twitter api tokens](https://developer.twitter.com/en/support/twitter-api).
### Config File
Create a copy of `configs/template.ini` as `configs/config.ini` and store your credentials in it.
### Conda Env
In the root directory of the project, create your conda env with `conda env create -f twitterbot.yml`.

### Running The Code
```bash
conda activate twitterbot
python client.py --config configs/config.ini
```

## Development
### The Command Class
To create commands for your bot:
1. Create a `Command` subclass using the `Command` Abstract Base Class.
2. Import the command into `client.py`
3. Add the command to the `commands_dict` in `client.py` along with a string alias for twitter users.

Your `Command` subclass will recieve:
1. The Twitter API
2. The Tweet ID
3. The User ID
4. Any text following the command, for parameters.

Your subclass should implement a `reply_tweet()` method that probably calls another method to do a thing, then prepares a response and tweets it back at the user.

For Example, you might make a class like this:

```python
class MyCommand (Command):
    def _do_something(self):
        #do something
        return 100

    def _format_output(self, result):
        # string format it or whatever
        return str(result)
    
    def reply_tweet(self):
        something = self._do_something()
        text = self._format_output(something)
        self.api.PostUpdate(
            status=text, 
            in_reply_to_status_id=self.tweet_id, 
            auto_populate_reply_metadata=True
        )
```

Then you can add it to `client.py`'s `commands_dict` like this:
```python
from my_commands import MyCommand

commands_dict = {
    'my_command': MyCommand,
}

```
And you should be good to go!
## Use
Tweet at your bot using the following format: "@bot command (params)"

