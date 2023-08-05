from encodings.aliases import aliases
from collections import defaultdict
import logging

def matchenc(infile, expected_words):
    '''
    parses available encoding types and checks
    if expected terms are present as such
    when decoded
    '''
    available_encs = list(set(aliases.values()))
    for enc in available_encs:
        try:
            with open(infile, 'r', encoding=enc) as inp:
                try:
                    contents = inp.read()
                    found, missed = defaultdict(list), defaultdict(list)
                    for word in expected_words:
                        if word in contents:
                            found[enc].append(word)
                        else:
                            missed[enc].append(word)

                    if expected_words:
                        if missed[enc]:
                            logging.debug('%s: Missed %s', enc, missed[enc])
                        else:
                            pass
                        if found[enc]:
                            if len(found[enc]) == len(expected_words):
                                logging.info('%s: Full Match %s', enc, found[enc])
                            else:
                                logging.info('%s: Partial (%s/%s) match %s', enc,
                                             len(found[enc]), len(expected_words), found[enc])
                        else:
                            pass
                    else:
                        logging.info('%s: readable. Use expected terms (--exp) to narrow results.',
                                     enc)


                except (UnicodeError, UnicodeDecodeError) as exception:
                    logging.debug('%s: %s', enc, type(exception).__name__)

        except LookupError as exception:
            logging.debug('%s: %s', enc, type(exception).__name__)



    return
