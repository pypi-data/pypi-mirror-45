import itertools
from unittest import SkipTest

from zuper_json.monkey_patching_typing import RegisteredClasses
from zuper_json.test_utils import assert_object_roundtrip, assert_type_roundtrip
from zuper_ipcl import  private_register


def check_one_klass(T):
    if not hasattr(T, 'get_examples'):
        raise SkipTest("No examples.")

    f = getattr(T, 'get_examples')

    examples = f(seed=32)
    # print(f'examples: {examples}')
    top5 = itertools.islice(examples, 3)

    with private_register('classes'):
        assert_type_roundtrip(T, {})
    #with private_register(T.__name__):
        for name, el in top5:
            data = assert_object_roundtrip(el, {})

    # print(f'Testing {T}')


def test_generated():
    # noinspection PyUnresolvedReferences
    import zuper_schemas

    for (module, name), K in list(RegisteredClasses.klasses.items()):
        if 'zuper_schemas' in module.split('.'):
            # print(f"I know {name}")
            class MyCheck:
                def __call__(self):
                    return check_one_klass(K)
            check = MyCheck()
            setattr(check, 'description', f'Examples for {name}')
            yield check
