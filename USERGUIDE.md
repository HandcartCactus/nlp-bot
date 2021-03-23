# What Do I Tweet Bot's User Guide

[TOC]

## Commands

### Quick List

1.  Topic Modeling: `@WhatDoITweetBot topics`
2.  Help: `@WhatDoITweetBot ` with any malformed command will send you a link to this document.

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

The topic model was tricky to implement satisfactorily. NMF and LDA just weren't cuting it. I ended up implementing a new model called CorEx Topic, Which was based on this paper:

```quote
Gallagher, R. J., Reing, K., Kale, D., and Ver Steeg, G. "Anchored Correlation Explanation: Topic Modeling with Minimal Domain Knowledge." Transactions of the Association for Computational Linguistics (TACL), 2017.
```

The code for CorExTopic can be found on github at https://github.com/gregversteeg/corex_topic.

## General Guidance

### Make My Own

You can make your own bot based on this one. There is a generic [command bot template](https://github.com/Ejjaffe/twitter-command-bot) on my github for convenience. Be sure to link to our bot in your documentation too!