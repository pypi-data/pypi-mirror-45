class User:
    def __init__(self, **options):
        self.name = options.get('name')
    
    @property
    def name(self):
        return self.name
