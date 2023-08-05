class Song:
    def __init__(self, **options):
        self.name = options.get('name')
        self.author = options.get('author')
        self.id = options.get('_id')
        self.size = options.get('size')
        self.size_mb = options.get('size_mb')
        self.links = options.get('links')
        #get other things here

    @property
    def name(self):
        return self.name

    @property
    def id(self):
        return self.id

    @property
    def size(self):
        return self.size

    @property
    def size_mb(self):
        return self.size_mb

    @property
    def author(self):
        return self.author
    
    @property
    def link(self):
        return self.links[0]

    @property
    def dl_link(self):
        return self.links[1]

    def download(self):
        link = self.links[1]
        pass
