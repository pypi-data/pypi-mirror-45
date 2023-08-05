from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
import traceback
from contextlib import contextmanager
from io import StringIO


class Tool(object):
    @classmethod
    @contextmanager
    def stdout_in_memory(cls, output):
        output.setdefault('data', '')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        result = StringIO()
        sys.stdout = result
        sys.stderr = result
        try:
            yield
        except:
            if output['data']:
                output['data'] = "%s\n%s" % (output['data'], traceback.format_exc())
            else:
                output['data'] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            if output['data']:
                output['data'] = "%s\n%s" % (output['data'], result.getvalue())
            else:
                output['data'] = result.getvalue()

    @classmethod
    @contextmanager
    def protecting_attributes(cls, obj, attrs, **kwargs):
        backup_data = {k: getattr(obj, k) for k in attrs}
        [setattr(obj, k, v) for k, v in kwargs.items()]
        try:
            yield
        except:
            raise
        finally:
            [setattr(obj, k, v) for k, v in backup_data.items()]

    @classmethod
    @contextmanager
    def protecting_items(cls, obj, items, **kwargs):
        backup_data = {k: obj[k] for k in items}
        for k, v in kwargs.items():
            obj[k] = v
        try:
            yield
        except:
            raise
        finally:
            for k, v in backup_data.items():
                obj[k] = backup_data[k]

    @classmethod
    def contruct_domain_from_str(cls, domain):
        AND, OR = ' and ', ' or '
        assert '(' not in domain, "can not process parenthese in string domain"
        if AND in domain:
            assert OR not in domain, "domain should not have or and and operators"
        if OR in domain:
            assert AND not in domain, "domain should not have or and and operators"
        and_or = '|' if OR in domain else '&'
        tuples = []
        tuples1 = domain.split(AND)
        [tuples.extend(t.split(OR)) for t in tuples1 if t]
        domain = [tuple(t.split()) for t in tuples if t]
        if not domain:
            res = []
        else:
            for ttuple in domain:
                assert len(ttuple) == 3, 'a condition should have 3 parts [%s]' % ttuple
            i = 0
            for key, op, value in domain:
                float_parts = value.split('.')
                isfloat = len(float_parts) == 2
                if op == "==": op = '='
                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value.isdigit():
                    value = int(value)
                elif isfloat and float_parts[0].isdigit() and float_parts[1].isdigit():
                    value = float(value)
                try:
                    value = eval(value)
                except Exception as e:
                    pass
                domain[i] = (key, op, value)
                i += 1
            if len(domain) > 1:
                domain = [and_or] * (len(domain) - 1) + domain
            res = domain
        return res
