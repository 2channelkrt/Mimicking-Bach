# Mimicking-Bach
creating melody based on Bach's keyboard scores, using Tensorflow.
## How It's Done

1. retrieve midi data from [musedata](http://www.musedata.org/)
2. Using [csvmidi](http://www.fourmilab.ch/webtools/midicsv/), convert midi data to csv data
3. Load & prune data
4. Train Model ([LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory))
5. Using trained model, create melody in csv format
6. using [csvmidi](http://www.fourmilab.ch/webtools/midicsv/), convert created csv format melody to audiable midi format.
## Created Examples
try listening at [soundcloud](https://soundcloud.com/2channelkrt/sets/mimicking-bach-examples)

## Articles
- [Github](Article.md)
- [Blog](https://2channelkrt.github.io/regular_post/2019/06/17/Mimicking-Bach-Melody-with-LSTM.html)
