# What Do I Tweet Bot's User Guide

[TOC]

## Commands

### Quick List

1.  Topic Modeling: `@WhatDoITweetBot topics`
2.  Tweet Time Analysis: `@WhatDoITweetBot when`
3.  Help: `@WhatDoITweetBot ` with any malformed command will send you a link to this document.

### Command Format

All commands to the bot start with an `@WhatDoITweetBot`, followed by a space character, and then a command name.

```
@WhatDoITweetBot commandName
```

Sometimes, commands come with options. The format for that is:

```
@WhatDoITweetBot commandName optionName optionValue
```

Multiple options can be configured like this:

```
@WhatDoITweetBot commandName optionName1 optionValue1 optionName2 optionValue2
```

### Topic Modeling

#### Use

The bot can run state of the art topic modeling code on your 200 most recent tweets. It will return lists of words that you have tweeted about that it believes belong to unique topics. To try it out, run:

```
@WhatDoITweetBot topics
```

The bot defaults to 3 topics, but you can ask it to try to find more. To find 6 topics, use the option `n_topics` followed by an integer.

```
@WhatDoITweetBot topics n_topics 6
```

Are you very verbose? The bot defaults to 20000 unique words, but can also be configured to inorporate more or less words with the `n_features` option.

```
@WhatDoITweetBot topics n_topics 6 n_features 300
```

```
@WhatDoITweetBot topics n_features 10000
```

#### Notes

The topic model was tricky to implement satisfactorily. NMF and LDA just weren't cutting it. I ended up implementing a new model called CorEx Topic, Which was based on this paper:

```quote
Gallagher, R. J., Reing, K., Kale, D., and Ver Steeg, G. "Anchored Correlation Explanation: Topic Modeling with Minimal Domain Knowledge." Transactions of the Association for Computational Linguistics (TACL), 2017.
```

The code for CorExTopic can be found on github at https://github.com/gregversteeg/corex_topic.

### Tweet Time Analysis

#### Use

The bot can run interesting analytics on when you tend to tweet. To try it out, run:

```
@WhatDoITweetBot when
```

The bot will respond with two plots describing when you tend to tweet, and a textual description of your tweeting habits. The first plot, the "pattern of life" plot, describes your average hourly tweets across weekdays and weekends, broken up by morning, noon-ish, afternoon, evening, and night time segments. The second plot is a breakdown of number of tweets by hour and day of the week. The description includes your most active time by pattern of life, along with basic statistics, and a naive estimate of the latest timestamp on your next tweet.

#### Notes

To generate a prediction of the latest timestamp of your next tweet, the bot uses [Chebyshev's inequality](https://en.wikipedia.org/wiki/Chebyshev%27s_inequality) with a 95% confidence, using the average time between consecutive tweets, and their standard deviation from the mean.

Unfortunately, the bot is limited to your last 200 tweets, so if you are a prolific tweeter, the bot's data may be limited to the last few days, making it incapable of an accurate pattern-of-life analysis.
## General Guidance

### Make Your Own

You can make your own bot based on this one. There is a generic [command bot template](https://github.com/Ejjaffe/twitter-command-bot) on my github for convenience. Be sure to link to our bot in your documentation too!
