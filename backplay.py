# -*- coding: utf-8 -*-

import xbmc
import xbmcgui

from magio.addon import MagioGoAddon
from magio.magiogo import MagioGo


# sys.argv = list(lambda arg: arg.decode('utf-8'), sys.argv)
addon = MagioGoAddon()
client = addon.client # type: MagioGo
channelName = xbmc.getInfoLabel('ListItem.ChannelName')
channels = client.channels()
channelId = {ch.id for ch in channels if ch.name == channelName.decode('utf-8')}
stream = client.channel_back_play_stream_info(channelId)

xbmc.log("Backplay stream url: " + stream.url, level=xbmc.LOGNOTICE)

#Player Stream
channel_name = xbmc.getInfoLabel('ListItem.ChannelName').replace("*", "")
info = {
        'Title': channel_name + ": " + xbmc.getInfoLabel('Listitem.Title') + " (Archív)",
        'year': xbmc.getInfoLabel('ListItem.Year'),
        'genre': xbmc.getInfoLabel('ListItem.Genre'),
        'plot': xbmc.getInfoLabel('ListItem.Plot')
    }
picture = {
    'thumb': xbmc.getInfoLabel('Listitem.Icon'),
    'icon': xbmc.getInfoLabel('Listitem.Icon'),
}
item = xbmcgui.ListItem()
item.setInfo('video', info)
item.setArt(picture)

item.setProperty('inputstream', 'inputstream.adaptive')
item.setProperty('inputstream.adaptive.manifest_type', 'mpd' if stream.manifest_type == 'mpd' else 'hls')
item.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
if stream.user_agent:
    stream.headers.update({'User-Agent': stream.user_agent})
if stream.headers:
    item.setProperty('inputstream.adaptive.stream_headers', '&'.join(['%s=%s' % (k, v) for (k, v) in
                                                                      list(stream.headers.items())]))

xbmc.Player().play(stream.url, item)
