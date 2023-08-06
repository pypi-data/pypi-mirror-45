# AmarettoPy

Python library to control Buildit servo actuators (only for python3)


## Install

### Windows

```
$ pip3 install amarettopy
```

### Ubuntu

```
$ sudo apt-get -y install python3-tk
$ pip3 install amarettopy
```

## Usage

### amarettopy library


* 速度制御と位置制御の方法
```
>>> import amarettopy
>>> amaretto = AmarettoPy(port="/dev/ttyUSB0", timeout_ms=3000) #for Linux
>>> amaretto = AmarettoPy(port="COM8", timeout_ms=3000) #for Win
>>> deviceId = 1
>>> state2str(amaretto.state())
>>> amaretto.ready(deviceId)
>>> amaretto.set_ref_velocity(deviceId, fromRPM(40))
>>> amaretto.set_ref_position(deviceId, fromDegree(180))
```

* 現在の位置や速度といった情報の取得
```
>>> (pos, vel, cur, ref, temp, faults) = amaretto.query_servo_status(deviceId)
```

* ライブラリについてのドキュメント
    * https://smartrobotics.github.io/AmarettoPy-doc/amarettopy.html


### amrtctl

amrtctl は AmarettoPy の各メソッドをコマンドラインから呼び出す為のツールです。
アクチュエーターの状態を確認する場合は以下のように実行します。

```
$ amrtctl query-servo-status -d 1 -p /dev/ttyUSB0
state: STATE_HOLD
pos: -51636
vel: 0
cur: 0
ref: 0
temp: 26
faults: NO_FAULTS
```

速度制御を行う場合は以下のように実行します。

```
$ amrtctl ready -d 1 -p /dev/ttyUSB0

$ amrtctl set-ref-velocity 2500 -d 1 -p /dev/ttyUSB0 # 指定速度の単位は [rpm/100]
0
```

位置制御を行う場合は以下のように実行します。

```
$ amrtctl stop -d 1 -p /dev/ttyUSB0

$ amrtctl set-ref-position 2500 -d 1 -p /dev/ttyUSB0 # 指定位置の単位は [360/65536 度]
-39775
```


### amrtct-gui

amrtctl は AmarettoPy の各メソッドをコマンドラインから呼び出す為のツールです。

```
$ amrtctl-gui
```

ポートを選択し、Connectボタンを押した後、各種ボタンを使ってデバイスを操作することが出来ます。





