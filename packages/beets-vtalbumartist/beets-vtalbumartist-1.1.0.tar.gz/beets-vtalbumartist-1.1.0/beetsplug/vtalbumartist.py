from beets.plugins import BeetsPlugin
from beets.importer import action
from beets import ui
from beets import mediafile

class VTAlbumArtist(BeetsPlugin):
  def __init__(self):
    super(VTAlbumArtist, self).__init__()
    
    self.albumartist = None
    self.should_set = False
    
    self.register_listener('import_task_choice', self._import_after_apply)
    self.register_listener('write', self._before_write)
    
    field = mediafile.MediaField(
        mediafile.MP3DescStorageStyle(u'VT Album Artist'),
        mediafile.MP4StorageStyle(u'----:com.apple.iTunes:VT Album Artist'),
        mediafile.ASFStorageStyle(u'VT/Album Artist'),
        mediafile.StorageStyle(u'VT_ALBUMARTIST')
    )
    self.add_media_field('vt_albumartist', field)
  
  def commands(self):      
    vtalbumartist_cmd = ui.Subcommand('vtalbumartist',
                                      help=u'set vt_albumartist field/tag for matching items')
    vtalbumartist_cmd.parser.add_option(
      u'-r', u'-R', u'--reset', dest='reset',
      action='store_true', default=False,
      help=u'match even those with field/tag already set')
    vtalbumartist_cmd.parser.add_option(
      u'-q', u'-Q', u'--quiet', dest='quiet',
      action='store_true', default=False,
      help=u'never prompt for input: set field/tag automatically')
    vtalbumartist_cmd.parser.add_option(
      u'-s', u'-S', u'--singletons', dest='singletons',
      action='store_true', default=False,
      help=u'match only non-album tracks (singletons)')
    vtalbumartist_cmd.func = self.cmd_func
    return [vtalbumartist_cmd]
  
  def cmd_func(self, lib, opts, args):
    if opts.singletons:
      items = lib.items(ui.decargs(args) + [u'singleton:true'])
      self.singleton_func(items, opts)
    else:
      albums = lib.albums(ui.decargs(args))
      self.album_func(albums, opts)
  
  def album_func(self, albums, opts):
    tagged_item_count = 0
    tagged_album_count = 0
    for album in albums:
      self.albumartist = None
      self.should_set = opts.reset
      
      if not opts.reset or not opts.quiet:
        for item in album.items():
          if 'vt_albumartist' in item:
            if self.albumartist is None:
              self.albumartist = item['vt_albumartist']
            elif self.albumartist != item['vt_albumartist']:
              self.albumartist = ""
          else:
            self.should_set = True
      else:
        self.albumartist = album.albumartist
      
      if not self.should_set:
        continue
      
      if not opts.quiet:
        fmt = u'    $albumartist - $album'
        self.process_item(album, fmt)
      for item in album.items():
        tagged_item_count += self.try_sync(item)
      tagged_album_count += 1
    ui.print_()
    ui.print_(u'Changed {} item(s) in {} album(s)'.format(tagged_item_count, tagged_album_count))
  
  def singleton_func(self, items, opts):
    tagged_item_count = 0
    for item in items:
      if not opts.reset and 'vt_albumartist' in item:
        continue
      
      if opts.reset and opts.quiet:
        self.albumartist = item.albumartist
      elif 'vt_albumartist' in item:
        self.albumartist = item['vt_albumartist']
      else:
        self.albumartist = None
      
      self.should_set = True
      
      if not opts.quiet:
        fmt = u'    $albumartist - $title'
        self.process_item(item, fmt)
      
      tagged_item_count += self.try_sync(item)
    ui.print_()
    ui.print_(u'Changed {} item(s)'.format(tagged_item_count))
  
  def process_item(self, item, fmt):
    ui.print_(u'Tagging:')
    ui.print_(format(item, fmt))
    self.set_albumartist(item.albumartist)
  
  def try_sync(self, item):
    if 'vt_albumartist' in item and item['vt_albumartist'] == self.albumartist:
      return 0
    
    item.try_write()
    item.store()
    return 1
  
  def set_albumartist(self, default_albumartist):
    input_options = None
    if self.albumartist is None or self.albumartist == "":
      self.albumartist = default_albumartist
      input_options = (u'Accept as-is', u'Edit')
      ui.print_(u'Default Virtual Album Artist:')
    else:
      if self.albumartist == default_albumartist:
        input_options = (u'Accept as-is', u'Edit')
      else:
        input_options = (u'Accept as-is', u'Edit', u'Default value')
      ui.print_(u'Current Virtual Album Artist:')
    ui.print_(u'    {}'.format(self.albumartist))
    
    sel = ui.input_options(input_options)
    if sel == u'a':
      pass
    elif sel == u'e':
      self.albumartist = ui.input_(u'Virtual Album Artist:').strip()
    elif sel == u'd':
      self.albumartist = default_albumartist
    else:
      assert False
  
  def _import_after_apply(self, session, task):
    if task.choice_flag != action.APPLY:
      return
    
    self.albumartist = None
    self.should_set = True
    
    for item in task.items:
      if 'vt_albumartist' in item:
        if self.albumartist is None:
          self.albumartist = item['vt_albumartist']
        elif self.albumartist != item['vt_albumartist']:
          self.albumartist = ""
    
    chosen_albumartist = task.chosen_ident()[0]    
    self.set_albumartist(chosen_albumartist)
  
  def _before_write(self, item, path, tags):
    if self.should_set:
      item['vt_albumartist'] = self.albumartist
      tags['vt_albumartist'] = self.albumartist
