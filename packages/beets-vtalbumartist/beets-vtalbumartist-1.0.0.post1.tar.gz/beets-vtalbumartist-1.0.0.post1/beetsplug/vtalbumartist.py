from beets.plugins import BeetsPlugin
from beets.importer import action
from beets import ui
from beets import mediafile

class VTAlbumArtist(BeetsPlugin):
  def __init__(self):
    super(VTAlbumArtist, self).__init__()
    
    self.album = None
    self.artist = None
    
    self.register_listener('import_task_choice', self._import_after_apply)
    self.register_listener('write', self._before_write)
    
    field = mediafile.MediaField(
        mediafile.MP3DescStorageStyle(u'VT Album Artist'),
        mediafile.MP4StorageStyle(u'----:com.apple.iTunes:VT Album Artist'),
        mediafile.ASFStorageStyle(u'VT/Album Artist'),
        mediafile.StorageStyle(u'VT_ALBUMARTIST')
    )
    self.add_media_field('vt_albumartist', field)
    
  def _import_after_apply(self, session, task):
    if task.choice_flag == action.APPLY:
      ui.print_(u'Current Virtual Album Artist:')
      if task.is_album:
        ui.print_(u'{}'.format(task.cur_artist))
      else:
        ui.print_(u'{}'.format(task.item.albumartist))
        
      sel = ui.input_options( (u'Accept as-is', u'Edit') )
      if sel == u'a':
        pass
      elif sel == u'e':
        self.artist = ui.input_(u'Virtual Album Artist:').strip()
        self.album = task.cur_album if task.is_album else task.item.album
      else:
        assert False
  
  def _before_write(self, item, path, tags):
    if item.album == self.album:
      item['vt_albumartist'] = self.artist
    elif 'vt_album_artist' not in tags:
      item['vt_albumartist'] = item.albumartist
