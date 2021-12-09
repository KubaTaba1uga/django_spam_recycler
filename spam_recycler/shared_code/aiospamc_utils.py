import aiospamc
import codecs
import re

PORT = 783

async def check_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.check(message=message, port=PORT)


async def report_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.report(message=message, port=PORT)


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
