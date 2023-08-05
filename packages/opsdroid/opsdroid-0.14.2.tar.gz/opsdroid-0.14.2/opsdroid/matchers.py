"""Decorator functions to use when creating skill modules."""

import logging

from opsdroid.const import REGEX_SCORE_FACTOR
from opsdroid.helper import add_skill_attributes


_LOGGER = logging.getLogger(__name__)


def match_regex(regex, case_sensitive=True, score_factor=None):
    """Return regex match decorator."""
    def matcher(func):
        """Add decorated function to skills list for regex matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"regex": {
                "expression": regex,
                "case_sensitive": case_sensitive,
                "score_factor": score_factor or REGEX_SCORE_FACTOR,
            }}
        )
        return func
    return matcher


def match_apiai_action(action):
    """Return Dialogflow action match decorator."""
    def matcher(func):
        """Add decorated function to skills list for Dialogflow matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"dialogflow_action": action}
        )
        return func
    _LOGGER.warning(_("Api.ai is now called Dialogflow, this matcher "
                      "will stop working in the future. "
                      "Use match_dialogflow_action instead."))
    return matcher


def match_apiai_intent(intent):
    """Return Dialogflow intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for Dialogflow matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"dialogflow_intent": intent}
        )
        return func
    _LOGGER.warning(_("Api.ai is now called Dialogflow, this matcher "
                      "will stop working in the future. "
                      "Use match_dialogflow_intent instead."))
    return matcher


def match_dialogflow_action(action):
    """Return Dialogflowi action match decorator."""
    def matcher(func):
        """Add decorated function to skills list for Dialogflow matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"dialogflow_action": action}
        )
        return func
    return matcher


def match_dialogflow_intent(intent):
    """Return Dialogflow intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for Dialogflow matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"dialogflow_intent": intent}
        )
        return func
    return matcher


def match_luisai_intent(intent):
    """Return luisai intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for luisai matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"luisai_intent": intent}
        )
        return func
    return matcher


def match_rasanlu(intent):
    """Return Rasa NLU intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for Rasa NLU matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"rasanlu_intent": intent}
        )
        return func
    return matcher


def match_recastai(intent):
    """Return recastai intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for recastai matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"recastai_intent": intent}
        )
        return func
    return matcher


def match_witai(intent):
    """Return witai intent match decorator."""
    def matcher(func):
        """Add decorated function to skills list for witai matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"witai_intent": intent}
        )
        return func
    return matcher


def match_crontab(crontab, timezone=None):
    """Return crontab match decorator."""
    def matcher(func):
        """Add decorated function to skills list for crontab matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"crontab": crontab,
             "timezone": timezone}
        )
        return func
    return matcher


def match_webhook(webhook):
    """Return webhook match decorator."""
    def matcher(func):
        """Add decorated function to skills list for webhook matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"webhook": webhook}
        )

        return func
    return matcher


def match_always(func=None):
    """Return always match decorator."""
    def matcher(func):
        """Add decorated function to skills list for always matching."""
        func = add_skill_attributes(func)
        func.matchers.append(
            {"always": True}
        )
        return func

    # Allow for decorator with or without parenthesis as there are no args.
    if callable(func):
        return matcher(func)
    return matcher
