from business import (
    Uploader,
    Getter,
    Setter,
    Deleter
)

# Making sure the objects do not get initiated again
UPLOADER = Uploader()
GETTER = Getter()
SETTER = Setter()
DELETER = Deleter()