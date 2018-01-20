import pyinotify
import asyncore

import logging

logger = logging.getLogger(__name__)

# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
	 # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)
        logger.debug('Created dawg')

    def process_IN_DELETE(self, event):
        print("Removing:", event.pathname)

    def process_IN_MODIFY(self, event):
        print("Modifying:", event.pathname)

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch('gallery', mask, rec=True)

asyncore.loop()