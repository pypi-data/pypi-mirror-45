This is a simple general purpose display server - it takes values from
mqtt and publishes the resulting image to mqtt.

.. figure:: img/example.png
   :alt: Example

   Example

Based on the received values a black/white 8bit image is generated
(optionaly, the background color can be set to transparent). The image
can be generated from the following elements:

-  ``Bar`` - Subscribes to a topic and draws a solid bar.
-  ``CircularChart`` - A circular chart with a static time axis (e.g
   00:00-23:59).
-  ``DigitalClock`` - Writes the current time.
-  ``ImageList`` - Image list preloads a set of images and displays one
   based on received mqtt-messages.
-  ``MQTTImage`` - Displays images that are received via mqtt messages.
-  ``SequentialChart`` - Regular chart with the latest values added at
   the right and the oldest values on the left.
-  ``StaticImage`` - Displays a static image.
-  ``StaticText`` - Writes the provided text.

Each element can be used multiple times.

The name
`Nikippe <https://de.wikipedia.org/wiki/Nikippe_(Tochter_des_Pelops)>`__
(Νiκίππη) is taken from the children of Pelops.

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Nikippe`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

For Users
=========

Installation
------------

Prerequisites for the core functionality are:

::

    sudo apt install python3 python3-pip python-pil
    sudo pip3 install pelops

Install via pip:

::

    sudo pip3 install nikippe

To update to the latest version add ``--upgrade`` as suffix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/nikippe.git
    cd nikippe
    sudo python3 setup.py install

This will install the following shell script: \* ``nikippe`` - the
display server as a registered shell script.

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '-v' - verbose output (optional) \* '--version' - show
the version number and exit

YAML-Config Example
-------------------

A yaml file must contain two root blocks: \* mqtt - mqtt-address,
mqtt-port, and path to credentials file credentials-file (a file
consisting of two entries: mqtt-user, mqtt-password) \* display-server -
topics that nikippe should publish the resulting image to and the update
behavior. \* renderer - configuration for the render engine and the
elements that should be displayed.

| Each element must have at least the following parameters: \*
  ``name: humidity-chart`` - free choose able name - not used internally
  \* ``type: chart`` - element type. must be [bar, circularchart,
  digitalclock, imagelist, mqttimage, mqtttext, sequentialchart,
  staticimage, statictext] \* ``x: 30`` - position in rendered image
  (top/left) \* ``y: 5`` - position in rendered image (top/left) \*
  ``width: 256`` - size of the element \* ``height: 60`` - size of the
  element \* ``foreground-color: 0`` - between 0 (black) and 255
  (white). \* ``background-color: 255`` - between 0 (black) and 255
  (white).
| \* ``active: True`` - if set to false, this entry will be ignored.

Optional parameters for all elements are: \*
``ignore-update-available: False`` - if present and set to True, this
element will not trigger an update. For example you have a clock-element
that updates every minute and you want to display the latest received
temperature value, you set this parameter to True for mqtttext element.

config.yaml
~~~~~~~~~~~

The config file consists of three root nodes: mqtt, display-driver, and
renderer. #### mqtt

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml

display-server
^^^^^^^^^^^^^^

::

    display-server:
        topics-pub-image: /test/image  # send image to the display driver
        send-on-change: True  # send new image to epaper if any element reports that it received an update
        send-interval: 60  # seconds. if 0 interval is disabled.

The first two entries are the topics the epaper device driver (see
`copreus <https://gitlab.com/pelops/copreus>`__) listens to.
``send-on-change`` and ``send-interval`` define the update behavior.

Renderer
''''''''

::

        renderer:
            width: 250
            height: 122
            background: ../resources/gui_background_2.13.png  # optional
            background-color: 255  # from 0 to 255.
            elements:

Common properties for all elments:

::

              - name: [name]
                type: [element type]
                x: 0  # x position in image
                y: 10  # y position in image
                width: 242  # width of element
                height: 77  # height of element
                foreground-color: 0  # gray value - 0 is black, 255 is white
                background-color: 255  # gray value - 0 is black, 255 is white
                transparent-background: True  # boolean / optional. If True, background-color will be treated as transparent
                active: False  # if False, entry will be ignored

Bar
   

.. figure:: img/example_bar.png
   :alt: Example Bar

   Example Bar

::

              - name: current-humidity
                type: bar
                x: 5
                y: 5
                width: 20
                height: 60
                foreground-color: 0 
                background-color: 255 
                active: True
                border: True  # if true, the whole bar will be surrounded by a single line in foreground-color.
                orientation: up  # up, down, left, right
                topic-sub: /test/humidity  # input value
                min-value: 5  # displayed bar % = (max(max-value, input) - min-value) / (max-value - min-value)
                max-value: 23  #

CircularChart
             

.. figure:: img/example_circularchart.png
   :alt: Example Circular Chart

   Example Circular Chart

::

              - name: time-chart
                type: circularchart
                active: False
                topic-sub: /test/humidity
                width: 210
                height: 60
                x: 30
                y: 5
                foreground-color: 0  # from 0 to 255.
                background-color: 255  # from 0 to 255.
                border-top: False
                border-bottom: True
                border-left: True
                border-right: False
                connect-values: True  # if true - values are connected with lines, other wise they are independent dots
                pixel-per-value: 2  # a new value/dot is drawn every n-th pixel on the x-axis. must be > 0.
                draw-cursor: True  # draw a cursor at the current time slot
                time-span: Day  # Week, Day, Hour, Minute
                history-service:
                    group-by: 300  # in seconds. 0==no grouping
                    aggregator: avg  # aggregator for group-by. valid values: avg, min, max, median. can be omitted if group-by=0.
                    use-dataservice: True  # use the dataservice archippe to fill the chart with persisted data
                    dataservice-request-topic-prefix: /dataservice/request
                    dataservice-response-topic-prefix: /dataservice/response

DigitalClock
            

.. figure:: img/example_digitalclock.png
   :alt: Example Digital Clock

   Example Digital Clock

::

              - name: digital-clock
                type: digitalclock
                x: 0  
                y: 10 
                width: 242
                height: 77
                foreground-color: 0 
                background-color: 255  
                active: False
                font: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
                size: 20  # font-size

ImageList
         

|Example ImageList Clock| |Example ImageList Day| |Example ImageList
Morning|

::

              - name: dynamicicons
                type: imagelist
                active: False
                x: 50
                y: 50
                width: 50
                height: 50
                foreground-color: 0  # from 0 to 255.
                background-color: 205  # from 0 to 255.
                default-image: clock
                topic-sub: /test/imagelist
                images:
                  - name: clock
                    image: ../resources/icon_clock.png
                    offset_x: 5
                    offset_y: 5
                  - name: day
                    image: ../resources/icon_day.png
                  - name: morning
                    image: ../resources/icon_morning.png
                    offset_y: 5

MQTTImage
         

.. figure:: img/example_mqttimage.png
   :alt: Example MQTTImage

   Example MQTTImage

::

              - name: icon
                type: mqttimage
                active: False
                x: 10
                y: 10
                width: 50
                height: 50
                foreground-color: 0  # from 0 to 255.
                background-color: 205  # from 0 to 255.
                topic-sub: /test/image
                offset_x: 5
                offset_y: 5

MQTTText
        

.. figure:: img/example_mqtttext.png
   :alt: Example MQTTText

   Example MQTTText

::

              - name: humidity-value
                type: mqtttext
                x: 5  
                y: 70 
                width: 70
                height: 25
                foreground-color: 0 
                background-color: 255
                active: True
                font: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
                size: 20  # font-size
                string: "{0:.1f}%"  # format string
                topic-sub: /test/humidity  # input value

SequentialChart
               

.. figure:: img/example_sequentialchart.png
   :alt: Example Sequential Chart

   Example Sequential Chart

::

              - name: humidity-chart
                type: sequentialchart
                active: True
                topic-sub: /test/humidity
                width: 210
                height: 60
                x: 30
                y: 5
                foreground-color: 0  # from 0 to 255.
                background-color: 255  # from 0 to 255.
                border-top: False
                border-bottom: True
                border-left: True
                border-right: False
                connect-values: True  # if true - values are connected with lines, other wise they are independent dots
                pixel-per-value: 2  # a new value/dot is drawn every n-th pixel on the x-axis. must be > 0.
                range-minimum: 10  # if set, chart minimum value is set to this value. otherwise auto range  (optional)
                range-maximum: 20  # if set, chart maximum value is set to this value. otherwise auto range  (optional)
                history-service:
                    group-by: 300  # in seconds. 0==no grouping
                    aggregator: avg  # aggregator for group-by. valid values: avg, min, max, median. can be omitted if group-by=0.
                    # use-dataservice: True  # use the dataservice archippe to fill the chart with persisted data
                    # dataservice-request-topic-prefix: /dataservice/request
                    # dataservice-response-topic-prefix: /dataservice/response

StaticImage
           

.. figure:: img/example_staticimage.png
   :alt: Example Static Image

   Example Static Image

::

              - name: clock
                type: staticimage
                active: False
                x: 10
                y: 10
                width: 50
                height: 50
                foreground-color: 0  # from 0 to 255.
                background-color: 205  # from 0 to 255.
                image: ../resources/icon_clock.png
                offset_x: 5
                offset_y: 5

StaticText
          

.. figure:: img/example_statictext.png
   :alt: Example Static Text

   Example Static Text

::

              - name: design
                type: statictext
                x: 124  
                y: 103  
                width: 76
                height: 10
                foreground-color: 0  
                background-color: 255
                active: True        
                font: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
                size: 8  # font-size
                string: "design by tgd1975"  # text to be displayed     

credentials.yaml
~~~~~~~~~~~~~~~~

::

    mqtt:
        mqtt-user: user
        mqtt-password: password

run Nikippe
-----------

using ``screen``
~~~~~~~~~~~~~~~~

``screen -d -m -S nikippe bash -c 'nikippe -c config_nikippe.yaml'`` ###
using ``systemd`` - add systemd example.

For Developers
==============

Getting Started
---------------

Nikippe consists of three elements: ``DisplayServer``, ``Renderer`` and
the render elements. The ``DisplayServer`` instantiates the render
engine and sends the publishes the updated image. This is done either
with a time interval and/or upon reception of new values. The
``Renderer`` is controlling the render elements and integrates them into
a single image.

Render elements are either specialications of ``AElement``,
``AElementMQTT`` or ``AElementHistory``. If you write a new element you
must also add it to the ``ElementFactory`` and write a schema extension.
\* ``AElement`` - Static element. to be used for elements that do not
change over the time (e.g. ``StaticText``) \* ``AElementMQTT`` - Element
that reacts to MQTT Messages (e.g. ``MQTTText``) \* ``AElementHistory``
- Something that needs not only the last MQTT Message but a history
(e.g. ``SequentialChart``)

Additional Dependencies
-----------------------

Next to the dependencies listed above, you need to install the
following:

::

    sudo apt install pandoc
    sudo pip3 install pypandoc

Todos
-----

-  ...

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/nikippe/merge_requests>`__ /
`bug reports <https://gitlab.com/pelops/nikippe/issues>`__ are always
welcome.

.. |Example ImageList Clock| image:: img/example_imagelist_clock.png
.. |Example ImageList Day| image:: img/example_imagelist_day.png
.. |Example ImageList Morning| image:: img/example_imagelist_morning.png


