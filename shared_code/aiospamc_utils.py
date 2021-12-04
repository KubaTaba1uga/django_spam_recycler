import aiospamc
import codecs


async def check_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.check(message=message)


async def report_for_spam(message):
    # https://aiospamc.readthedocs.io/en/latest/protocol.html?highlight=threshold#report-request
    return await aiospamc.report(message=message)


async def report_spam_async(message):
    return await report_for_spam(message.obj)


async def create_report(message):
    SPAM_DESCRIPTION_START = 'pts rule name'
    response = await report_for_spam(message)
    report_content = codecs.decode(response.body, errors='ignore')
    return {
        'spam_score': response.headers['Spam'].score,
        'spam_description':
        report_content[report_content.find(SPAM_DESCRIPTION_START):],
        'response': response
    }
