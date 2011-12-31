# Copyright (c) 2010 IP Global, LLC.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Form(object):
    def __init__(self, **kwargs):
        self._elements = []
        for name in dir(self):
            attr = object.__getattribute__(self, name)
            if isinstance(attr, FormElement):
                attr.name = name
                attr.value = kwargs.get(name, None)
                self._elements.append(attr)

    def __setattr__(self, name, value):
        elem = getattr(type(self), name, None)
        if elem and isinstance(elem, FormElement):
            elem.value = value
        else:
            object.__setattr__(self, name, value)

    def __iter__(self):
        return iter(self._elements)


class FormElement(object):
    def __init__(self, **kwargs):
        self._name = None

        self._value = kwargs.get('value', None)

        self._attrs = kwargs.get('attrs', {})
        if not isinstance(self._attrs, dict):
            raise ValueError('Attributes must be of type dict')

        self._required = kwargs.get('required', False)
        if not isinstance(self._required, bool):
            raise ValueError('Required must be of type bool')


    def __call__(self):
        return self.render()

    def __repr__(self):
        return "'%s'" % (self._value or '')

    def __str__(self):
        return self._value or ''

    def validate(self, value):
        """
        Child classes should raise an exception if it fails validation
        """
        pass

    @property
    def value(self):
        return self.__str__()

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = unicode(name)

    def render(self):
         """
         Default method that should be overridden in the subclass
         """
         raise NotImplementedError


class Input(FormElement):
    """
    Base class for handling all HTML <input> elements

    Usage
    =====
    field = Input(
        input_type='text',
        attrs = {
            'class': 'inputClass',
            'onfocus': 'js_onfocus();',
            'onblur': 'js_onblur();',
            },
        required = False,
        )
    """

    _INPUT_TYPES = [
        "text", "password", "checkbox",
        "radio", "submit", "reset", "file",
        "hidden", "image", "button"
        ]

    _IMMUTABLE_INPUT_TYPES = [
        "submit", "reset", "button"
        ]

    def __init__(self, input_type='text', **kwargs):
        super(Input, self).__init__(**kwargs)

        self._input_type = input_type
        if self._input_type not in self._INPUT_TYPES:
            raise ValueError('Invalid type specified for %s' % (self._name))

        self._immutable = self._input_type in self._IMMUTABLE_INPUT_TYPES

    def render(self):
        attrs, value = '', ''
        if self._attrs:
            attrs = ['%s="%s"' % (k,v) for k,v in self._attrs.iteritems()]
            attrs = " ".join(attrs)
        if self._value and self._input_type != 'password':
            value = 'value="%s"' % (self._value)
        return '<input id="id_%s" name="%s" type="%s" %s %s>' % (
            self._name, self._name, self._input_type, attrs, value)


class TextInput(Input):
    """
    Input object with input_type = 'text'
    """
    def __init__(self, **kwargs):
        super(TextInput, self).__init__(input_type='text', **kwargs)


class PasswordInput(Input):
    """
    Input object with input_type = 'password'
    """
    def __init__(self, **kwargs):
        super(PasswordInput, self).__init__(input_type='password', **kwargs)


class Textarea(FormElement):
    """
    Base class for handling HTML <textarea> elements.
    """

    def __init__(self, **kwargs):
        super(Textarea, self).__init__(**kwargs)

    def render(self):
        attrs = ''
        if self._attrs:
            attrs = ['%s="%s"' % (k,v) for k,v in self._attrs.iteritems()]
            attrs = " ".join(attrs)
        return '<textarea id="id_%s" name="%s" %s>%s</textarea>' % (
            self._name, self._name, attrs, self._value or '')


class Select(FormElement):
    """
    Base class for handling HTML <select><option></option></select> elements.

    Usage
    =====
    field = Select(
        options = (('label1', 'value1'), ('label2', 'value2')),
        attrs = { # specify element attributes
            'class': 'inputClass',
            'size': '4',
            },
        required = False,
        )
    """

    def __init__(self, options, **kwargs):
        super(Select, self).__init__(**kwargs)

        self._options = options
        if not isinstance(self._options, tuple):
            raise ValueError('Options must be a tuple of tuples')

    def render(self):
        attrs, options = '', ''
        if self._attrs:
            attrs = ['%s="%s"' % (k,v) for k,v in self._attrs.iteritems()]
            attrs = " ".join(attrs)

        if self._options:
            ol = []
            try:
                for o in self._options:
                    selected = ''
                    if o[1] == self._value:
                        selected = ' selected="selected"'
                    ol.append('<option value="%s"%s>%s</option>' % (
                        o[1], selected, o[0]))
            except:
                raise ValueError('Invalid option construction')

            options = "".join(ol)

        return '<select id="id_%s" name="%s" %s>%s</select>' % (
            self._name, self._name, attrs, options)

