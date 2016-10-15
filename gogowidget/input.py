from .exceptions import PatchException

def yesorno(q, strictness=1, repeat=True, default=True, answers=('yes', 'no')):
    """
    Ask a boolean question. Handles the errors.

    kwargs:
    -strictness (0, 1 or 2. default: 1):
    0: accepts everything that starts by "y" or "n" (may be changed in answers)
    1: accepts "y", "n", "yes" or "no" (may be changed in answers)
    2: only accepts "yes" or "no" (may also be changed)
    -repeat (True or False, default: True):
    set to False to don't bother the user and return the 'default' arg if the answer is not correct.
    -default (default: True):
    returned when answer is empty or when not correct if repeat is False
    -answers (default: ("yes", "no") (unless patched by yesorno_default_answers))
    affects the available answers. For example, if strictness = 1 and answers = ("hai", "iie"),
    the possible answers will be "hai", "iie", "h" and "i".
    Used in international settings. Can be patched by yesorno_default_answers().
    """
    yes, no = answers
    if strictness == 0 or strictness == 1:
        full = q + ' ({}/{}, default: {}) '.format(yes[0], no[0], yes[0] if default else no[0])
    elif strictness == 2:
        full = q + ' ({}/{}, default: {}) '.format(yes, no, yes if default else no)

    valid = False
    while not valid:
        answer = input(full)
        valid = True
        # first case: the answer is empty
        if len(answer) == 0:
            return default
        # parse the answer depending on 
        if strictness == 0:
            if answer[0] != yes[0] and answer[0] != no[0]:
                valid = False
        elif strictness == 1:
            if answer not in (yes[0], no[0], yes, no):
                valid = False
        elif strictness == 2:
            if answer != yes and answer != no:
                valid = False
        # if the user wants the default answer when the first answer isn't good
        if not valid and repeat:
            return default
    if strictness == 0:
        return True if answer[0] == yes[0] else False
    if strictness == 1:
        return True if answer in (yes, yes[0]) else False
    if strictness == 2:
        return True if answer == yes else False



def yesorno_default_answers(answers):
    """
    NOT WORKING. Todo.
    Brutally, metaprogrammatically monkey patch the yesorno function to definitely change the default answers.

    The answers arg must be a 2 item iterable.
    """
    if not hasattr(answers, '__iter__'):
        raise PatchException('patch could not be done: %s is not iterable' % answers)
    if len(answers) != 2:
        raise PatchException('patch could not be done: length of %s is not 2' % answers)
    yesorno.__defaults__ = (1, answers)
