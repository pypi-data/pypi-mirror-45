# -*- coding: utf-8 -*-
import re
import os
import copy
import humanfriendly
from collections import OrderedDict
import subprocess


__all__ = (
    'Runnable',
    'OptSet',
    'Opt',
    'Flag',
    'FlagsOpt',
    'BitOpt',
    'ByteOpt',
    'TimeOpt',
    'IntOpt',
    'FloatOpt',
    'BoundedOpt',
    'EnableOpt',
    'KeyValOpt',
    'GroupOpt',
    'SizeOpt',
    'OneOfOpt'
)


class OptSet(object):
    __slots__ = '_opts', 'META'

    def __init__(self, *opt, **opts):
        self.META = dict()
        self._opts = OrderedDict()

        if len(opt):
            self.add(*opt)

        if len(opts):
            self.set(**opts)

    def __repr__(self):
        cmds = map(str, (x for opt in self.live_opts for x in opt))
        cmds = subprocess.list2cmdline(cmds)
        return '<%s: %s>' % (self.__class__.__name__, cmds)

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            if name == '_opts':
                raise
            if name not in self._opts:
                raise
            return self._opts[name]

    def __setattr__(self, name, value):
        try:
            if name != '_opts':
                self._opts[name].set_value(value)
            else:
                raise AttributeError
        except (AttributeError, KeyError):
            super(OptSet, self).__setattr__(name, value)

    def __delattr__(self, name):
        try:
            if name != '_opts':
                self._opts[name].set_value(None)
            else:
                raise AttributeError
        except (AttributeError, KeyError):
            super(OptSet, self).__delattr__(name)

    def __str__(self):
        return ' '.join(map(str, self.opts))

    def __iter__(self):
        for opt in self.opts:
            yield opt

    def add(self, *opt):
        for o in opt:
            if isinstance(o, (Opt, Flag)):
                _opt = self.get(o.name)
                if _opt is None:
                    self._opts[o.name] = copy.copy(o)
                else:
                    _opt.set_value(o.val)
                    _opt.opt = o.opt
            elif isinstance(o, (OptSet)):
                self.add(*o)
            else:
                raise TypeError('Invalid option: %s; Custom options must be '
                                'of type "transcend.Opt" "transcend.OptSet" or '
                                '"transcend.Flag".' % o.name)

    def get(self, opt_name, default=None):
        try:
            return self._opts[opt_name]
        except KeyError:
            return default

    def set(self, **opts):
        for name, value in opts.items():
            try:
                self._opts[name].set_value(value)
            except KeyError:
                raise NameError('Name %s is not a registered option.' % name)

    def list(self):
        for opt in sorted(self.opts, key=lambda x: x.name[0]):
            print(repr(opt))

    @property
    def opts(self):
        return [opt for opt in self._opts.values()]

    @property
    def opt_names(self):
        return [opt.name for opt in self._opts.values()]

    @property
    def live_opts(self):
        for opt in self._opts.values():
            if opt.val is not None:
                yield opt

    def items(self):
        return {name: value for name, value in self._opts.items()}

    def merge(self, *cls):
        for c in cls:
            try:
                self.add(*c._opts.values())
            except AttributeError:
                pass


class Runnable(OptSet):
    __slots__ = OptSet.__slots__

    def __repr__(self):
        return '<%s>' % ' '.join(self.get_cmd())

    def get_bin(self):
        return os.path.join(self.BINPATH or '', self.BIN)

    def get_cmd(self, no_bin=False):
        if not no_bin:
            yield self.get_bin()

        for opt in self.live_opts:
            for x in opt:
                yield str(x)


class Opt(object):
    __slots__ = ['name', 'opt', 'val', 'desc', 'cast', 'default']

    def __init__(self, opt, name=None, value=None, cast=str, default=None):
        self.name = name or opt
        self.opt = '-%s' % opt.lstrip('-') if len(opt) else ''
        self.cast = cast
        self.val = None
        self.default = default
        self.set_value(value)

    def __call__(self, *args, **kwargs):
        return self.set_value(*args, **kwargs)

    def __repr__(self):
        s = str(self)
        if len(s):
            return '<%s>' % s
        return '<%s: %s [%s]>' % (self.name, self.opt, self.cast)

    def __iter__(self):
        if len(self.opt):
            yield self.opt
        if self.val is None:
            yield str(self.default)
        else:
            yield str(self)

    def __str__(self):
        if self.val is not None:
            return str(self.val if self.val is not None else self.default)
        return ''

    def to_proc(self):
        if self.val:
            return list(self)
        return []

    def set_value(self, value):
        if value is None:
            self.val = None
        else:
            self.val = self.cast(value)
        return self


class IntOpt(Opt):
    __slots__ = Opt.__slots__

    def __init__(self, *args, **kwargs):
        super(IntOpt, self).__init__(*args, cast=int, **kwargs)


class FloatOpt(Opt):
    __slots__ = Opt.__slots__

    def __init__(self, *args, **kwargs):
        super(FloatOpt, self).__init__(*args, cast=float, **kwargs)


class BoundedOpt(Opt):
    __slots__ = Opt.__slots__ + ['_upper_bound', '_lower_bound']

    def __init__(self, opt, name=None, cast=int, lower=0, upper=100, **kwargs):
        self._lower_bound = lower
        self._upper_bound = upper
        super(BoundedOpt, self).__init__(opt, name=name, cast=cast, **kwargs)

    def set_value(self, value):
        if value is None:
            self.val = value
        else:
            value = self.cast(value)
            if self._lower_bound <= value <= self._upper_bound:
                self.val = value
            else:
                raise ValueError('Value `%s` not within bounds %s-%s.' %
                                 (value, self._lower_bound, self._upper_bound))
        return self


class EnableOpt(BoundedOpt):
    __slots__ = BoundedOpt.__slots__

    def __init__(self, opt, name=None, lower=0, upper=1, **kwargs):
        super(EnableOpt, self).__init__(
            opt, name=name, cast=int, upper=upper,  lower=lower, **kwargs)

    def set_value(self, value=True):
        if value is True:
            value = self._upper_bound
        if value is False:
            value = self._lower_bound
        return super(EnableOpt, self).set_value(value)


class Flag(Opt):
    __slots__ = Opt.__slots__

    def __repr__(self):
        s = str(self)
        if len(s):
            return '<%s>' % s
        return '<%s: %s [flag (not set)]>' % (self.name, self.opt)

    def __call__(self, value=True):
        return self.set_value(value)

    def __iter__(self):
        if self.val is None and self.default is True:
            yield str(self.opt)
        else:
            yield str(self.val)

    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return ''

    def to_proc(self):
        if self.val:
            return list(iter(self))
        return []

    def set_value(self, value):
        if value in {True, False, None}:
            self.val = self.opt if value is True else None
        return self


class FlagsOpt(Opt):
    __slots__ = Opt.__slots__

    def set_value(self, flag=None, *flags):
        if flag is None:
            self.val = None
        else:
            flags = list(flags)
            flags.insert(0, flag)
            self.val = ' '.join(map(lambda x: '+' + str(x).strip('+'), flags))
        return self


class BitOpt(Opt):
    __slots__ = Opt.__slots__
    _RE_SIZE = re.compile(r"""([\d.]+)([^\d.])""")

    def set_value(self, bits):
        if isinstance(bits, str):
            bits = bits.strip()
            bitsearch = self._RE_SIZE.search(bits)
            if bitsearch is not None:
                bits = float(bitsearch.group(1))
                abbr = bitsearch.group(2).strip().lower()
            else:
                abbr = None
                bits = float(bits)
            if abbr is None:
                self.val = int(bits)
            elif abbr == 'k':
                self.val = int(bits * 1000)
            elif abbr == 'm':
                self.val = int(bits * (1000 ** 2))
            elif abbr == 'g':
                self.val = int(bits * (1000 ** 3))
        else:
            if bits is None:
                self.val = bits
            else:
                self.val = int(bits)
        return self


class ByteOpt(Opt):
    __slots__ = Opt.__slots__
    _RE_SIZE = re.compile(r"""([\d.]+)([^\d.])""")

    def set_value(self, bytes):
        if isinstance(bytes, str):
            self.val = int(humanfriendly.parse_size(bytes))
        else:
            if bytes is None:
                self.val = bytes
            else:
                self.val = int(bytes)
        return self


class TimeOpt(Opt):
    __slots__ = Opt.__slots__

    def set_value(self, seconds):
        if seconds is None:
            self.val = None
        else:
            try:
                self.val = float(seconds)
            except (ValueError, TypeError):
                time = seconds.split(':')
                seconds = float(time[-1].lstrip('0') or 0)
                minutes = int(time[-2].lstrip('0') or 0)
                try:
                    hours = int(time[-3].lstrip('0') or 0)
                except:
                    hours = 0
                self.val = float(seconds + (minutes * 60) + (hours * 60 * 60))
        return self


class SizeOpt(Opt):
    __slots__ = Opt.__slots__

    def set_value(self, size):
        """ @size: (#tuple) """
        if size is None:
            self.val = None
        elif not isinstance(size, str):
            self.val = 'x'.join(map(str, size))
        else:
            self.val = 'x'.join(map(str.strip, size.lower().split('x')))
        return self


class KeyValOpt(Opt):
    __slots__ = Opt.__slots__ + ['separator']

    def __init__(self, opt, name=None, separator=',', **kwargs):
        self.separator = separator
        super(KeyValOpt, self).__init__(opt, name, **kwargs)

    def _to_str(self, pairs):
        if not isinstance(pairs, dict):
            return str(pairs)
        out = []
        add_out = out.append
        for name, value in pairs.items():
            add_out('%s=%s' % (name, value))
        return self.separator.join(out)

    def __str__(self):
        if self.val is not None:
            return self._to_str(self.val)
        return ''

    def set_value(self, pairs):
        """ @pairs: (#dict) """
        if pairs is None:
            self.val = None
        # elif isinstance(pairs, str) or pairs is None:
        #     self.val = pairs
        else:
            self.val = pairs
        return self

    def set(self, **opt):
        return self.update(opt)

    def update(self, opt):
        old_val = self.val.copy()
        old_val.update(opt)
        self.set_value(old_val)
        return self


class GroupOpt(KeyValOpt):
    __slots__ = KeyValOpt.__slots__

    def set_value(self, items):
        """ @pairs: (#dict) """
        if isinstance(items, str) or items is None:
            self.val = items
        else:
            self.val = self.separator.join(map(lambda x: str(self.cast(x)),
                                               items))
        return self


class OneOfOpt(Opt):
    __slots__ = Opt.__slots__ + ['choices']

    def __init__(self, opt, name=None, cast=str, choices=None, **kwargs):
        self.choices = tuple(choices or [])
        super(OneOfOpt, self).__init__(opt, name=name, cast=cast, **kwargs)

    def set_value(self, val):
        if val is None:
            self.val = val
        elif self.cast(val) in self.choices:
            self.val = self.cast(val)
        else:
            raise ValueError('`%s` not found in %s. Must be one of: \n  %s' %
                             (val, self.name, tuple(self.choices)))
        return self
