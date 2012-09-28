from mongoengine import *                           # To define a schema for a
                                                    # document, we create a
class Metadata(EmbeddedDocument):                   # class that inherits from
    tags = ListField(StringField())                 # Document.
    revisions = ListField(IntField())               #
                                                    # Fields are specified by
class WikiPage(Document):                           # adding field objects as
    title = StringField(required=True)              # class attributes to the
    text = StringField()                            # document class.
    metadata = EmbeddedDocumentField(Metadata)      #
                                                    # Querying is achieved by
if __name__=="__main__":
    page.title = "Hello, World!"                    # calling the objects
    for page in WikiPage.objects:                   # attribute on a document
        print page.title                            # class.
