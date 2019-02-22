# Mimicking-Bach
creating melody based on Bach's keyboard scores, using Tensorflow.
* * *
## How It's Done

1. retrieve midi data from <a href="http://www.musedata.org/" target="_blank">musedata</a>
2. Using [csvmidi](http://www.fourmilab.ch/webtools/midicsv/){:target="_blank"}, convert midi data to csv data
3. Load & optimize data
4. Train Model
5. Using trained model, create melody in csv format
6. using [csvmidi](http://www.fourmilab.ch/webtools/midicsv/){:target="_blank"}, convert created csv format melody to audiable midi format.
* * *
## Created Examples