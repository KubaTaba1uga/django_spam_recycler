import aiospamc
import codecs
import re
import os

PORT = os.environ.get('SPAMASSASIN_PORT', '783')
HOST = os.environ.get('SPAMASSASIN_HOST', 'localhost')

CONFIG = {'port': PORT, 'host': HOST}

async def check_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.check(message=message, **CONFIG)


async def report_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.report(message=message, **CONFIG)


def format_report(report):
    SPAM_DESCRIPTION_START = 'pts rule name'
    REGEX = ".?[0-9]\.[0-9] "
    report_content = codecs.decode(report, errors='ignore')
    report_content = report_content[
        report_content.find(SPAM_DESCRIPTION_START):]

    for point in set(re.findall(REGEX,
                                report_content)):

            report_content = re.sub(point, f"\n{point}", report_content)

    return report_content

async def create_report(message):

    response = await report_for_spam(message)
    report_content = format_report(response.body)

    return {
        'spam_score': response.headers['Spam'].score,
        'spam_description': report_content,
        'response': response
    }
