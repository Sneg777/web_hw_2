from mongoengine import Document, StringField, BooleanField, connect


uri = "mongodb+srv://Sneg321:***@clusterbes.tzjea.mongodb.net/?retryWrites=true&w=majority&appName=ClusterBes"


connect(host=uri, db="HW_08")

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    sent = BooleanField(default=False)
    meta = {"collection": "Contact"}
