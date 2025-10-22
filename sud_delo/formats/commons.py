class Err:
    def __init__(self, val):
        self.value = val

class Ok:
    def __init__(self, val):
        self.value = val

def all_text(selector, separator='\n'):
    return separator.join(
        [s.strip() for s in selector.xpath('.//text()').getall()])
