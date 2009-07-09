## @package customWidgets
# This is a collection of Custom Widgets

import gtk
import mapPixbuf
from mapConst import *
from inputValidation import allow_only_numbers


## A simple right justify label
def lbl(text):
    l = gtk.Label(text)
    l.set_justify(gtk.JUSTIFY_RIGHT)
    return l

## Pack a given container in a nice frame
def _frame(strName, container, spacing = 5):
    frame = gtk.Frame(strName)
    vbox = gtk.VBox(False, spacing)
    vbox.set_border_width(spacing)
    vbox.pack_start(container)
    frame.add(vbox)
    return frame

## A Spin button that allows numbers only
def _SpinBtn(value=0, lower=MAP_MIN_ZOOM_LEVEL,
             upper=MAP_MAX_ZOOM_LEVEL, step=1, maxChars=2):
    a_zoom = gtk.Adjustment(value, lower, upper, step)
    spin = gtk.SpinButton(a_zoom)
    spin.connect('insert-text', allow_only_numbers, maxChars)
    return spin

## An entry box that allows numbers only
def _myEntry(strText, maxChars=8, isInt=True):
    myEntry = gtk.Entry()
    myEntry.set_text(strText)
    myEntry.connect('insert-text', allow_only_numbers, maxChars, isInt)
    return myEntry

## Prompt user to select a Folder
def FolderChooser():
    strFileName = False
    dialog = gtk.FileChooserDialog("Select Folder", None,
                                   gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    if dialog.run() == gtk.RESPONSE_OK:
        strFileName = dialog.get_filename()
    dialog.destroy()
    return strFileName

## Display a Tooltip
def myToolTip(widget, x, y, keyboard_mode, tooltip, title, desc, filename=None):
    table = gtk.Table(2,2)
    table.set_row_spacings(2)
    table.set_col_spacings(6)
    table.set_border_width(4)

    pixbuf = mapPixbuf.getImage(filename)
    image = gtk.image_new_from_pixbuf(pixbuf)
    image.set_alignment(0, 0)
    table.attach(image, 0,1,0,2)

    titleLabel = gtk.Label()
    titleLabel.set_markup("<b>%s</b>" % title)
    titleLabel.set_alignment(0, 0)
    table.attach(titleLabel, 1,2,0,1)

    descLabel = gtk.Label(desc)
    descLabel.props.wrap = True
    table.attach(descLabel, 1,2,1,2)

    tooltip.set_custom(table)
    table.show_all()
    return True
