================
MGL EFIS Plotter
================

The MGL EFIS Plotter package parses the flight data logs from
MGL EFIS products, such as the iEFIS.
It can read both ``IEFISS.REC`` and ``IEFISBB.DAT`` files.

The package is intended to be used inside a Jupyter Notebook
to create graphs. It can also save data as CSV files.

Installation
------------

Install Jupyter Notebook as part of Anaconda_
or from the Jupyter_ website.

.. _Anaconda: https://www.anaconda.com/
.. _Jupyter: https://jupyter.org/

Install mgl_efis_plotter with pip or your favorite Python package manager::

  pip install mgl_efis_plotter


Sample Usage
------------

Jupyter Notebook cell:

.. code-block:: python

    from mgl_efis_plotter import *

    config = Config()
    flights = create_flights('IEFIS.REC', config)

    p = Plot(flights[0])
    # plot pressure altitude vs. density altitude vs. outside air temperature
    p.plot2(['pAltitude', 'densityAltitude', 'oat']).show()

Configuration
-------------

Here is the default configuration. You can do one of three things:

1. Use it as-is.
2. Use it mostly as-is, replacing just a few values.
3. Replace almost everything, keeping only a few things unchanged.

.. code-block:: python

    class Config:
        units = {
            'airspeed': 'knots',  # 'knots' or 'kph'
            'barometer': 'hg',  # 'hg' or 'millibars'
            'fuel': 'gallons',  # 'gallons' or 'liters'
            'manifoldPressure': 'hg',  # 'hg' or 'millibars'
            'oilPressure': 'psi',  # 'psi' or 'millibars'
            'ambientTemperature': 'c',  # 'f' or 'c'
            'engineTemperature': 'f',  # 'f' or 'c'
        }

        # set each thermocouple value to one of 'cht' or 'egt' or None (capitalized and without quotation marks)
        # the values that you set here must match the configuration of your RDAC
        thermocouples = {
            1: 'cht',
            2: 'egt',
            3: 'cht',
            4: 'egt',
            5: 'cht',
            6: 'egt',
            7: 'cht',
            8: 'egt',
            9: None,
            10: None,
            11: None,
            12: None,
        }

        plot_dimensions = (12, 8)  # width & height in inches
        plot_dpi = 100  # dots per inch
        plot_font_size = 14

        rolling_window = 16  # bigger numbers make smoother graphs; start with 16

        # iEFIS seems to add about 260 seconds to the timestamp at the top of the hour
        new_flight_delta = 300

To use it as-is, create a cell like this:

.. code-block:: python

    config = Config

To use it mostly as-is, replacing just a few values, create a cell like this:

.. code-block:: python

    config = Config
    config.units['barometer'] = 'millibars'
    config.units['fuel'] = 'liters'

Replace almost everything, keeping only a few things unchanged, create a cell like this:

.. code-block:: python

    class MyConfig(Config):
        units = {
            'airspeed': 'kph',  # 'knots' or 'kph'
            'barometer': 'millibars',  # 'hg' or 'millibars'
            'fuel': 'liters',  # 'gallons' or 'liters'
            'manifoldPressure': 'millibars',  # 'hg' or 'millibars'
            'oilPressure': 'millibars',  # 'psi' or 'millibars'
            'ambientTemperature': 'c',  # 'f' or 'c'
            'engineTemperature': 'c',  # 'f' or 'c'
        }

        # set each thermocouple value to one of 'cht' or 'egt' or None (capitalized and without quotation marks)
        # the values that you set here must match the configuration of your RDAC
        thermocouples = {
            1: 'cht',
            2: 'cht',
            3: 'cht',
            4: 'cht',
            5: 'egt',
            6: 'egt',
            7: 'egt',
            8: 'egt',
            9: None,
            10: None,
            11: None,
            12: None,
        }
    config = MyConfig()

Load the Flights
----------------

Once you have set up your configure, load the flights from your file and print a list of them with a cell like this:

.. code-block:: python

    flights = create_flights('IEFIS.REC', config)

    for i in range(0, len(flights)):
        print(i, ':', flights[i])

It will print a list something like this:

.. code-block::

    0 : Flight at 2019-03-31 11:20:44 to 2019-03-31 11:40:48,  5775 messages, timestamps 486,454,570 to 486,455,853
    1 : Flight at 2019-03-31 12:11:53 to 2019-03-31 12:48:18, 10501 messages, timestamps 486,458,099 to 486,460,433
    2 : Flight at 2019-03-31 11:20:42 to 2019-03-31 11:20:42,     8 messages, timestamps 486,454,568 to 486,454,568

Select the flight you want and create a plot object out of it. For example, to work with flight #1, create this cell:

.. code-block:: python

    p = Plot(flights[1])

Plot One Attribute
------------------

Plot one attribute with lines like these examples:

.. code-block:: python

    p.plot('asi').show()
    p.plot('asi', 'Airspeed').show()
    p.plot('cht').show()

The second parameter is optional and is used to label the Y-axis. The two attributes "cht" and "egt" are special;
they display multiple lines on the graph, one per cylinder.

Plot Multiple Attributes
------------------------

Plot multiple attributes on a single graph with lines line these examples.
Note that the list of attributes is surrounded by square brackets.

.. code-block:: python

    p.plot(['asi', 'groundSpeed']).show()
    p.plot(['asi', 'groundSpeed'], ['Airspeed', 'Ground Speed']).show()
    p.plot(['pAltitude', 'densityAltitude', 'oat']).show()

Put It All Together
-------------------

Here are a few examples, putting everything together into a single cell.
Note that you can keep reusing the ``p`` object after you have created it.

.. code-block:: python

    from mgl_efis_plotter import *

    config = Config()
    flights = create_flights('IEFIS.REC', config)

    p = Plot(flights[0])

    p.plot('asi').show()

    p.plot2(['asi', 'oilTemperature1']).show()

    p.plot2(['pAltitude', 'densityAltitude', 'oat']).show()

List All Available Attributes
-----------------------------

You can get a list of all of the attributes available for your flight with this line.

.. code-block:: python

    p.list_attributes()

Save a Plot to a File
---------------------

You can save a plot to a file by replacing ``show()`` with ``save(FILENAME)`` like this:

.. code-block:: python

    p.plot('vsi', 'Vertical Speed').save('verticalspeed.png')

Export Data to a CSV File
-------------------------

You can export any set of attributes to a CSV file with a cell like this:

.. code-block:: python

    p.flight.save_csv('flightdata.csv', ['asi', 'vsi', 'densityAltitude', 'oat', 'rpm', 'manifoldPressure'])

Advanced Usage
--------------

The X-axis of every plot is minutes from the beginning of the flight.
You can zoom in on any section of the flight by limiting the X-axis to a range of minutes by adding the ``xlim`` option
to either ``plot()`` or ``plot2()``.
Here is an example, zooming in on the timespan beginning 5 minutes after takeoff and ending 10 minutes after takeoff.

.. code-block:: python

    p.plot('cht', xlim=(5, 10)).show()

Author
------

| Art Zemon
| Email: art@zemon.name
| Blog: https://cheerfulcurmudgeon.com/

Copyright and MIT License
-------------------------

|copy| Copyright 2019 Art Zemon.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |copy| unicode:: U+000A9 .. COPYRIGHT SIGN
