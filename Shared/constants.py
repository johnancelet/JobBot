class MetaConst(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError


class Const(object, metaclass=MetaConst):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError

class HTMLConstants(Const):

    class TagType(Const):
        DIV = 'div'
        SPAN = 'span'
        INPUT = 'input'
        TEXT_AREA = 'textarea'
        SELECT = 'select'
        H2 = 'h2'
        ANCHOR = 'a'
        PARAGRAPH = 'p'

    class Attributes(Const):
        HREF = 'href'
        TYPE = 'type'
        ID = 'id'
        INNER_TEXT = 'innerText'
        NAME = 'name'
        FOR = 'for'
        VALUE = 'value'
        CLASS = 'class'

    class InputTypes(Const):
        RADIO = 'radio'
        TEXT = 'text'
        PHONE = 'tel'
        EMAIL = 'email'
        FILE = 'file'
        TEXT_AREA = 'textarea'
        HIDDEN = 'hidden'
        CHECK_BOX = 'checkbox'
        SELECT_ONE = 'select-one'

