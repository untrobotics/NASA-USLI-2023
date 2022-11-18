# About

This is sourced from [Trackuino](https://github.com/trackuino/trackuino). The main difference is that it functions without a GPS connection to the Arduino. See the [Differences](/README.md#Differences) for more details.

# Important notices

**Add your callsign to the config.h file. This is a legal requirement.** ^(at least in the US)

**Do not run this while connected to the transmitter chip without the antenna. The chip can be damaged without it.**
- I recommend soldering the antenna and chip in a way so that the antenna doesn't get removed unexpectedly.

# Hardware

Required Components:

* An Arduino
  * This was tested with a [SparkFun RedBoard](https://www.sparkfun.com/products/13975). Most likely any Arduino will work.
  * You'll need something to power the Arduino. The RedBoard can be powered and programmed via the USB port, so that will not need a DC power supply.
* An [HX1 Transmitter](http://www.radiometrix.com/content/hx1)
  * HX1s can come in 144.390MHz (United States of America), 144.800MHz (Europe), and 145.175MHz (Australia). Most retailers will only let you purchase the proper chip.
* Some wires to connect everything
* An antenna.
  * It must be able to transmit the frequency associated with the transmitter chip.
    * Most antennas have a range and should be able to transmit all 3 frequencies.
    * If you want to build your own antenna then use [this calculator](https://m0ukd.com/calculators/quarter-wave-ground-plane-antenna-calculator/) to figure out your antenna sizes. Velocity factor should be fine at 0.95, but the frequency needs to be put at whatever the transmitter chip uses.
  * Some kind of connector to connect the chip and antenna ([example](https://www.adafruit.com/product/4642)). Or you could use a wire and risk extra noise in the transmission.

Optional:

* A breadboard or protoboard to help connect the chip, antenna, and Arduino.
* Soldering equipment (to solder antenna/chip to the protoboard)
* GPS receiver, temperature sensor, buzzer, or any other sensor.
* A radio or some way to decode APRS (so you can make sure that you are transmitting properly).
* A potato (to eat).

Here is an image of how it is connected (compared to [SparkFun's wiring](https://learn.sparkfun.com/tutorials/hx1-aprs-transmitter-hookup-guide#connecting-to-trackuino) as that one has other components such as a buzzer and GPS):

![Wiring Image. Why yes I did get a higher quality image of the RedBoard than what is posted on SparkFun's guide, how could you tell?](/Images/Diagram.png)

Picture of an example setup:

![Example of setup](/Images/Setup.png)

# Building (copied from ``Trackuino-master``)

If you are building for the Arduino platform you need Arduino IDE version 0023 or higher (tested with versions 2.0.0). Get it from the [Arduino web site](http://arduino.cc/).

Unzip the Code folder in your sketches directory and load it up by double-clicking on trackuino.ino.

The single most important configuration file is [config.h](/Code/config.h). The file is self-documented. Here is where you set up your callsign, among other things.

# Using Trackuino

Change ``aprs_send()`` (located in [aprs.cpp](/Code/aprs.cpp)) to send what packets you want. Right now it sends a message that says "Test message" (defined by the macro `APRS_MESSAGE` from the config file). Commented code is examples from the SparkFun fork of Trackuino.

Add your callsign to the config file. Use the macro `S_CALLSIGN`.

Upload the code to the Arduino to run.

Currently the time between transmissions is 60 seconds, defined by a macro in [config.h](/Code/config.h) called `APRS_PERIOD`. Change it if you want a shorter time between transmissions (don't make it too short [duh]).

# Differences

2 main things were commented out:
1. Line 88-92, 151-156 for [trackuino.ino](/Code/trackuino.ino)
2. Line 55-79 (explained below)

``aprs_send()`` comments out most of the packets and only sends the message. 
