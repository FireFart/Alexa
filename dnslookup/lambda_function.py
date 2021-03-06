# -*- coding: utf-8 -*-

import logging
import gettext
import socket

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type

import data

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        return handler_input.response_builder.speak(_(data.WELCOME_MESSAGE)).ask(_(data.WELCOME_RETRY)).response


class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.COPYRIGHT))
        return handler_input.response_builder.response


class LookupIntentHandler(AbstractRequestHandler):
    """Handler for lookup intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LookupIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LookupIntent")
        _ = handler_input.attributes_manager.request_attributes["_"]

        slots = handler_input.request_envelope.request.intent.slots
        dnsSlot = slots["dns"].value
        ipSlot = slots["ip"].value
        ip1 = slots["ip_a"].value
        ip2 = slots["ip_b"].value
        ip3 = slots["ip_c"].value
        ip4 = slots["ip_d"].value

        speech = ""
        if dnsSlot:
            # replace stuff like "google punkt d. e." in german
            dnsSlot = dnsSlot.replace(". ", "")
            # replace stuff like 'google dot com'
            dnsSlot = dnsSlot.replace(" {} ".format(_(data.DOT)), ".")
            try:
                addr = socket.gethostbyname(str(dnsSlot))
                speech = _(data.ANSWER_DNS).format(dnsSlot, addr)
            except Exception as e:
                logger.info("Input: %s", dnsSlot)
                logger.info(e)
                speech = _(data.ANSWER_DNS_FALSE).format(dnsSlot)
        elif ipSlot:
            # replace stuff like '8 dot 8 dot 8 dot 8 dot 8'
            ipSlot = ipSlot.replace(" {} ".format(_(data.DOT)), ".")
            try:
                name = socket.gethostbyaddr(str(ipSlot))[0]
                speech = _(data.ANSWER_IP).format(ipSlot, name)
            except Exception as e:
                logger.info("Input: %s", ipSlot)
                logger.info(e)
                speech = _(data.ANSWER_IP_FALSE).format(ipSlot)
        elif ip1 and ip2 and ip3 and ip4:
            ip = "{}.{}.{}.{}".format(ip1, ip2, ip3, ip4)
            try:
                name = socket.gethostbyaddr(ip)[0]
                speech = _(data.ANSWER_IP).format(ip, name)
            except Exception as e:
                logger.info("Input: %s", ip)
                logger.info(e)
                speech = _(data.ANSWER_IP_FALSE).format(ip)
        else:
            speech = _(data.ANSWER_INVALID_INPUT)

        return handler_input.response_builder.speak(speech).set_should_end_session(True).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: %s", handler_input.request_envelope.request.reason)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.HELP_MESSAGE)).ask(_(data.HELP_MESSAGE))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")

        return handler_input.response_builder.set_should_end_session(True).response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.FALLBACK_MESSAGE)).ask(_(data.FALLBACK_MESSAGE))

        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was %s", handler_input.request_envelope.request)
        _ = handler_input.attributes_manager.request_attributes["_"]

        return handler_input.response_builder.speak(_(data.EXCEPTION_MESSAGE)).set_should_end_session(True).response


class LocalizationInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is %s", locale)
        i18n = gettext.translation(
            'messages', localedir='locales', languages=[locale.replace("-", "_")], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext


class LoggingInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request received: %s", handler_input.request_envelope.request)


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(LookupIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Localization
sb.add_global_request_interceptor(LocalizationInterceptor())
# Logging
sb.add_global_request_interceptor(LoggingInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
