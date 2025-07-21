class Place:
    def __init__(self, title, notes, tags, url, comment):
        self.title = title
        self.notes = notes
        self.tags = tags
        self.url = url
        self.comment = comment
        self.data = {
            'title': title,
            'notes': notes,
            'tags': tags,
            'url': url,
            'comment': comment
        }

    def __str__(self):
        return self.title or ''

# pageSize
# 
