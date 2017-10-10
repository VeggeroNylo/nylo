# TEST-CASES to check everything's okay

# this should, like, run at startup in a big try except 
# and swear to the user if there is any exception

import parser

assert parser.parse('"hello" \'world\'') == {'type': 'code', 'value': 
                                                 [{'type': 'string', 'value': 'hello'}, 
                                                  {'type': 'string', 'value': 'world'}]}

assert parser.parse('-3 3 -3 -.3') == {'type': 'code', 'value': 
                                [{'type': 'variable', 'value': 'sub'}, 
                                {'type': 'code', 'value': 
                                    [{'type': 'list', 'value': 
                                        [{'type': 'code', 'value': 
                                            [{'type': 'int', 'value': -3}, 
                                            {'type': 'int', 'value': 3}]}, 
                                        {'type': 'code', 'value': 
                                            [{'type': 'int', 'value': 3}]}, 
                                        {'type': 'code', 'value': [{'type': 'float', 'value': 0.3}]}]}]}]}
                                        
# 1+1 is quite complicated. Surprise!
assert parser.parse('1+1') == {'type': 'code', 'value': 
                                   [{'type': 'variable', 'value': 'sum'}, 
                                    {'type': 'code', 'value': 
                                         [{'type': 'list', 'value': 
                                               [{'type': 'code', 'value': 
                                                     [{'type': 'int', 'value': 1}]}, 
                                               {'type': 'code', 'value': 
                                                    [{'type': 'int', 'value': 1}]}]}]}]}

                                        
assert parser.parse('-.3 .3') == {'type': 'code', 'value': 
                                      [{'type': 'float', 'value': -0.3}, 
                                       {'type': 'float', 'value': 0.3}]}

assert parser.parse('(2)((2)2)') == {'type': 'code', 'value': 
                                         [{'type': 'code', 'value': 
                                               [{'type': 'int', 'value': 2}]}, 
                                         {'type': 'code', 'value': 
                                              [{'type': 'code', 'value': 
                                                    [{'type': 'int', 'value': 2}]}, 
                                              {'type': 'int', 'value': 2}]}]}

assert parser.parse('[1,2]') == {'value': 
                                     [{'value': 
                                           [{'value': 
                                                 [{'value': 1, 'type': 'int'}], 
                                            'type': 'code'}, 
                                           {'value': 
                                                [{'value': 2, 'type': 'int'}], 
                                            'type': 'code'}], 
                                        'type': 'list'}], 
                                    'type': 'code'}

assert parser.parse('[1:2, "hello": "world"]') == {'type': 'code', 'value': 
                                                       [{'type': 'list', 'value': 
                                                             [{'type': 'couple', 'value': 
                                                                   [{'type': 'code', 'value': 
                                                                         [{'type': 'int', 'value': 1}]}, 
                                                                   {'type': 'code', 'value': 
                                                                        [{'type': 'int', 'value': 2}]}]}, 
                                                            {'type': 'couple', 'value': 
                                                                [{'type': 'code', 'value': 
                                                                    [{'type': 'string', 'value': 'hello'}]}, 
                                                                {'type': 'code', 'value': 
                                                                    [{'type': 'string', 'value': 'world'}]}]}]}]}
                                   
assert parser.parse('a[=2]') == {'value': 
                              [{'value': 'a', 'type': 'variable'}, 
                               {'value': 
                                    {'value': 
                                         [{'value': 'equal', 'type': 'variable'}, 
                                          {'value': 
                                               [{'value': 
                                                     [{'value': 
                                                           [{'value': 'implicit', 'type': 'variable'}], 
                                                       'type': 'code'}, 
                                                     {'value': 
                                                          [{'value': 2, 'type': 'int'}], 
                                                      'type': 'code'}], 
                                                 'type': 'list'}], 
                                           'type': 'code'}], 
                                    'type': 'code'}, 
                                'type': 'condition'}], 
                            'type': 'code'}
                                                     
assert parser.parse('{x|x*2}') == {'value': 
                                       [{'arguments': 
                                             {'value': [[['x']]], 'type': 'arguments'}, 
                                        'value': 
                                            {'value': 
                                                 [{'value': 'mol', 'type': 'variable'}, 
                                                  {'value': 
                                                       [{'value': 
                                                             [{'value': 
                                                                   [{'value': 'x', 'type': 'variable'}], 
                                                                'type': 'code'}, 
                                                             {'value': 
                                                                  [{'value': 2, 'type': 'int'}], 
                                                                'type': 'code'}], 
                                                        'type': 'list'}], 
                                                  'type': 'code'}], 
                                            'type': 'code'}, 
                                        'type': 'function'}], 
                                    'type': 'code'}

# {*2} is so short I can't honestly belive the output is 
# so fucking long. Why is this so complicated...
assert parser.parse('{*2}') == {'value': 
                                    [{'value': 
                                          [{'value': 'mol', 'type': 'variable'}, 
                                           {'value': 
                                                [{'type': 'list', 'value': 
                                                      [{'type': 'code', 'value': 
                                                            [{'type': 'variable', 'value': 'implicit'}]}, 
                                                      {'type': 'code', 'value': 
                                                           [{'value': 2, 'type': 'int'}]}]}], 
                                            'type': 'code'}], 
                                      'arguments': 
                                          {'type': 'arguments', 'value': []}, 
                                      'type': 'function'}], 
                                'type': 'code'}

assert parser.parse('{int x, y}') == {'type': 'code', 'value': 
                                          [{'type': 'class', 'value': 
                                                {'type': 'arguments', 'value': [[['int'], ['x']], [['int'], ['y']]]}}]}

# such simple, much cool
assert parser.parse('unnamed unnamed2 unnamed_cool_42') == {'value': 
                                                                [{'value': 'unnamed', 'type': 'variable'}, 
                                                                 {'value': 'unnamed2', 'type': 'variable'}, 
                                                                 {'value': 'unnamed_cool_42', 'type': 'variable'}], 
                                                            'type': 'code'}
                                                                
assert parser.parse('a, int x, y, list string k, z: 0, 0, 0, 0, 0') == {
    'type': 'code', 'value': 
        [{'type': 'variable', 'value': 'assign'}, 
         {'type': 'code', 'value': 
              [{'type': 'list', 'value': 
                    [{'type': 'code', 'value': 
                          [{'type': 'arguments', 'value': [[['a']], [['int'], ['x']], [['int'], ['y']], [['list'], ['string'], ['k']], [['list'], ['string'], ['z']]]}]}, 
                    {'type': 'code', 'value': 
                         [{'type': 'variable', 'value': 'list'}, 
                          {'type': 'code', 'value': 
                               [{'type': 'list', 'value': 
                                     [{'type': 'code', 'value': 
                                           [{'type': 'int', 'value': 0}]}, 
                                     {'type': 'code', 'value': 
                                          [{'type': 'int', 'value': 0}]}, 
                                     {'type': 'code', 'value': 
                                          [{'type': 'int', 'value': 0}]}, 
                                     {'type': 'code', 'value': 
                                          [{'type': 'int', 'value': 0}]}, 
                                     {'type': 'code', 'value': 
                                          [{'type': 'int', 'value': 0}]}]}]}]}]}]}]}

# You don't REALLY have to look (or even worst, actually understand)
# the block of text below
#                                       ...unlucky, I can't be saved.
assert parser.parse('int[=1] a: {list[len()=2] string x}') == {
    'value': 
        [{'value': 'assign', 'type': 'variable'}, 
         {'value': 
              [{'value': 
                    [{'value': 
                          [{'value': [[['int', 
                                        {'value': 
                                             {'value': 
                                                  [{'value': 'equal', 'type': 'variable'}, 
                                                   {'value': 
                                                        [{'value': 
                                                              [{'value': 
                                                                    [{'value': 'implicit', 'type': 'variable'}], 
                                                                'type': 'code'}, 
                                                              {'value': 
                                                                   [{'value': 1, 'type': 'int'}], 
                                                                'type': 'code'}], 
                                                          'type': 'list'}], 
                                                    'type': 'code'}], 
                                              'type': 'code'}, 
                                         'type': 'condition'}], ['a']]], 'type': 'arguments'}], 
                        'type': 'code'}, 
                     {'value': 
                          [{'value': 
                                {'value': [[['list', 
                                    {'value': 
                                         {'value': 
                                              [{'value': 'equal', 'type': 'variable'}, 
                                               {'value': 
                                                    [{'value': 
                                                          [{'value': 
                                                                [{'value': 'len', 'type': 'variable'}, 
                                                                 {'value': [], 'type': 'code'}], 
                                                            'type': 'code'}, 
                                                            {'value': 
                                                                 [{'value': 2, 'type': 'int'}], 
                                                             'type': 'code'}], 
                                                      'type': 'list'}], 
                                                'type': 'code'}], 
                                          'type': 'code'}, 
                                     'type': 'condition'}], ['string'], ['x']]], 'type': 'arguments'}, 
                            'type': 'class'}], 
                     'type': 'code'}], 
                 'type': 'list'}], 
            'type': 'code'}], 
        'type': 'code'}


'''print(parse("""
pyramid: {list int layer|
    len(layer)=1{return [layer]}
    next_layer: layer(2)sum
    return [layer] & pyramid(next_layer)
} """))'''
