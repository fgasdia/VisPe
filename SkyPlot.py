"""
Created May 4, 2016

Produce a plot which represents the path of a satellite through the local sky.

@author: EP-Guy
"""

import matplotlib.pyplot as plt
import numpy as np
import collections


class SkyPlot:
    """A matplotlib plot axes for plotting stars and satellites on."""

    def __init__(self, plot_name):
        self.name = plot_name
        self.ax, self.fig = self._init_plot()

    @staticmethod
    def _mapr(r):
        """Convert polar plot radius axis so 90 is at center."""
        if isinstance(r, collections.Iterable):
            return [90-x for x in r]
        else:
            return 90-r

    @staticmethod
    def _d2r(theta):
        """Convert from degrees to radians."""
        if isinstance(theta, collections.Iterable):
            return [t*np.pi/180 for t in theta]
        else:
            return theta*np.pi/180

    @staticmethod
    def _mag2size(mag):
        """Return plot size for star of magnitude mag."""

        star_mag = [-1, 0, 1, 2, 3, 4]
        star_size = [20, 15, 10, 7, 4, 1.5]

        # interp returns 20 and 1.5 for < -1 and > 4
        return np.interp(mag, star_mag, star_size)

    def _init_plot(self):
        """Initialize matplotlib plot figure."""

        # Turn off interactive plotting
        plt.ioff()

        # Create new figure and close so it's not displayed
        fig = plt.figure(self.name, figsize=(10, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

        ax.set_ylim(90, 0)
        ax.set_yticks(range(0, 90, 10))
        ax.set_yticklabels(list(map(str, range(90, 0, -10))))
        ax.set_theta_zero_location("N")

        return (ax, fig)

    def show(self):
        """Show plot."""
        plt.figure(self.name)
        plt.show()

    def add_points(self, az, alt, size=5, color='b', ls='none'):
        """Add azimuth(theta) and alt(r) points to plot in degrees.

        This function automatically applies mapr so that 90 deg is at zenith.
        """

        az = self._d2r(az)
        alt = self._mapr(alt)
        plt.figure(self.name)
        self.ax.plot(az, alt, marker='.', markersize=size,
                     c=color,
                     linestyle=ls)

    def add_sat(self, az, alt):
        """Add satellite location in az(theta)/alt(r) in degrees."""

        self.add_points(az, alt, size=5, color='r', ls='-')

    def add_stars(self, az, alt, mag):
        """Add star location in az(theta)/alt(r) in degrees.

        Star size corresponds to magnitude.
        """

        s = self._mag2size(mag)
        self.add_points(az, alt, size=s.tolist(), color='k')
