# -*- coding: utf-8 -*-

from gettext import gettext as _

WELCOME_MESSAGE = _("Welcome to d. n. s. lookup. Please define your query.")
WELCOME_RETRY = _("Please ask your question.")
COPYRIGHT = _("copyright by firefart")
HELP_MESSAGE = _("Please ask for a DNS name or an I. P. Address")
EXCEPTION_MESSAGE = _("Sorry, there was some problem. Please try again.")
FALLBACK_MESSAGE = _("Sorry, I don't know how to interpret that. Please try again.")

# specific
DOT = _("dot")
ANSWER_DNS = _("Domain {} has address {}")
ANSWER_DNS_FALSE = _("Domain {} does not exist")
ANSWER_IP = _("I. P. {} has reverse lookup {}")
ANSWER_IP_FALSE = _("I. P. {} does not have a reverse lookup")
ANSWER_INVALID_INPUT = _("Could not determine I. P. address or domain name in your query.")
