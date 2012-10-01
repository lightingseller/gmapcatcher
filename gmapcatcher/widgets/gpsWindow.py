# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.gpsWindow
# Widget to show GPS information

import pygtk
pygtk.require('2.0')
import gtk

from gobject import timeout_add_seconds
from pango import FontDescription
from gmapcatcher.mapConst import *
from gmapcatcher import mapUtils


class gpsWindow(gtk.Window):
    def __init__(self, mapsObj):
        gtk.Window.__init__(self)
        self.mapsObj = mapsObj

        self.gps_values = []

        vbox = gtk.VBox(False)
        vbox.pack_start(self._createLabels(FontDescription("16")))
        self.add(vbox)
        self.set_title("GPS")
        self.set_border_width(10)
        self.update_widgets()
        self.set_size_request(200, 300)
        self.show_all()
        self.connect('delete-event', self.on_delete)
        timeout_add_seconds(1, self.update_widgets)

    def on_delete(self, widget, event):
        self.mapsObj.gpsw = None

    def _createLabels(self, font):
        texts = ['GPS time', 'Latitude', 'Longitude', 'Speed', 'Heading', 'Altitude']
        table = gtk.Table(len(texts) + 2, 2)
        table.set_col_spacings(5)
        table.set_row_spacings(5)

        self.fix_label = gtk.Label()
        self.fix_label.set_use_markup(True)
        self.fix_label.modify_font(font)
        table.attach(self.fix_label, 0, 2, 0, 1)

        for i in range(len(texts)):
            label = gtk.Label('<b>%s</b>' % texts[i])
            label.set_use_markup(True)
            label.set_alignment(0, 0.5)
            label.modify_font(font)
            table.attach(label, 0, 1, i + 1, i + 2)

            label = gtk.Label()
            label.set_alignment(0, 0.5)
            label.modify_font(font)
            self.gps_values.append(label)
            table.attach(self.gps_values[-1], 1, 2, i + 1, i + 2)

        i += 1
        button = gtk.Button('copy GPS location to clipboard')
        button.connect('clicked', self.locationToClipboad)
        table.attach(button, 0, 2, i + 1, i + 2)

        return table

    def locationToClipboad(self, w=None):
        ## add GPS location latitude/longitude to clipboard
        clipboard = gtk.Clipboard()
        if self.mapsObj.gps and self.mapsObj.gps.gpsfix:
            clipboard.set_text("Latitude=%.6f, Longitude=%.6f" %
                              (self.mapsObj.gps.gpsfix.latitude, self.mapsObj.gps.gpsfix.longitude))
        else:
            clipboard.set_text("No GPS location detected.")

    def update_widgets(self):
        if self.mapsObj.gps and self.mapsObj.gps.gpsfix:
            if self.mapsObj.gps.gpsfix.mode > MODE_NO_FIX:
                self.fix_label.set_text('<b><span foreground=\"green\">FIX</span></b>')
            else:
                self.fix_label.set_text('<b><span foreground=\"red\">NO FIX</span></b>')
            if self.mapsObj.gps.gpsfix.time != 0.0:
                gps_time = str(self.mapsObj.gps.gpsfix.time)
                self.gps_values[0].set_text('%s:%s:%s' % (gps_time[0:2], gps_time[2:4], gps_time[4:6]))
            else:
                self.gps_values[0].set_text('0.0')
            self.gps_values[1].set_text('%.6f' % self.mapsObj.gps.gpsfix.latitude)
            self.gps_values[2].set_text('%.6f' % self.mapsObj.gps.gpsfix.longitude)
            speed_unit = self.mapsObj.conf.units
            speed = self.mapsObj.gps.gpsfix.speed
            if speed_unit != UNIT_TYPE_NM:
                speed = mapUtils.convertUnits(UNIT_TYPE_NM, speed_unit, speed)
            self.gps_values[3].set_text('%.1f %s' % (speed, SPEED_UNITS[speed_unit]))
            self.gps_values[4].set_text('%.1f' % self.mapsObj.gps.gpsfix.track)
            self.gps_values[5].set_text('%.1f' % self.mapsObj.gps.gpsfix.altitude)
        else:
            self.fix_label.set_text('<span foreground=\"red\">No GPS detected</span>')
            for gps_value in self.gps_values:
                gps_value.set_text('---')
        self.fix_label.set_use_markup(True)
        return True