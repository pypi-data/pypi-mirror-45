
import os
import datetime
import logging
import pytest

from selenium.common.exceptions import (
    WebDriverException,
    ElementNotVisibleException,
    InvalidElementStateException,
    InvalidSelectorException,
    NoSuchElementException,
    StaleElementReferenceException
)

from promium.logger import Logger
from promium.core.exceptions import BrowserConsoleException


log = logging.getLogger(__name__)


def pytest_sessionstart(session):
    if hasattr(session.config, 'cache'):
        cache = session.config.cache
        cache_path = "cache/{}".format(session.config.lastfailed_file)
        print("Lastfailed:", cache.get(cache_path, set()))
    session.run_duration = datetime.datetime.now()
    print("\nPytest session start %s\n" % session.run_duration)


@pytest.mark.trylast
def pytest_sessionfinish(session):
    finish = datetime.datetime.now()
    duration = datetime.timedelta(
        seconds=(finish - session.run_duration).seconds
    )
    print("\n\nPytest session finish %s (duration=%s)\n" % (finish, duration))


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption(
        "--capturelog",
        dest="logger",
        default=None,
        action="store_true",
        help="Show log messages for each failed test"
    )
    parser.addoption(
        "--fail-debug-info",
        action="store_true",
        help="Show screenshot and test case urls for each failed test"
    )
    parser.addoption(
        "--duration-time",
        action="store_true",
        help="Show the very slow test"
    )
    parser.addoption(
        "--highlight",
        action="store_true",
        help="Highlighting elements"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Enable headless mode for Chrome browser only"
    )
    parser.addoption(
        "--chrome",
        action="store_true",
        help="Use chrome browser"
    )
    parser.addoption(
        "--firefox",
        action="store_true",
        help="Use firefox browser"
    )
    parser.addoption(
        "--opera",
        action="store_true",
        help="Use opera browser"
    )
    parser.addoption(
        "--ie",
        action="store_true",
        help="Use ie browser"
    )
    parser.addoption(
        "--edge",
        action="store_true",
        help="Use edge browser"
    )
    parser.addoption(
        "--grid",
        help=(
            "Use selenium grid host for example: "
            "'http://192.168.0.1:4444/wd/hub' "
            "or  with base auth "
            "'http://test:test-password@192.168.0.1:4444/wd/hub'"
        )
    )
    parser.addoption(
        "--repeat",
        action="store",
        default=1,
        type="int",
        metavar='repeat',
        help='Number of times to repeat each test. Mostly for debug purposes'
    )
    parser.addoption(
        "--check-console",
        action="store_true",
        help="Check browser console js and other errors"
    )


def pytest_generate_tests(metafunc):
    if metafunc.config.option.repeat > 1:
        metafunc.fixturenames.append('repeat')
        metafunc.parametrize('repeat', range(metafunc.config.option.repeat))


@pytest.fixture(autouse=True)
def logger(request):
    return logging.getLogger()


@pytest.mark.trylast
def pytest_runtest_call(item):
    if hasattr(item.config, "assertion_errors"):
        if item.config.assertion_errors:
            msg = "\n{assertion_errors_list}\n".format(
                assertion_errors_list="\n".join(item.config.assertion_errors)
            )
            raise AssertionError(msg)
    if item.config.getoption("--check-console"):
        if hasattr(item.config, "check_console_errors"):
            browser_console_errors = item.config.check_console_errors()
            if browser_console_errors:
                msg = (
                    "Browser console js errors found:"
                    "\n{console_errors}\n".format(
                        console_errors=u"\n".join(
                            browser_console_errors
                        )
                    )
                )
                raise BrowserConsoleException(msg)


@pytest.mark.tryfirst
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """pytest failed test report generator"""
    html_plugin = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    when = report.when
    excinfo = call.excinfo
    extra = getattr(report, 'extra', [])

    # remove webdriver java traceback
    if excinfo:
        if excinfo.type in [
            ElementNotVisibleException,
            InvalidElementStateException,
            InvalidSelectorException,
            NoSuchElementException,
            StaleElementReferenceException
        ] and report.longrepr:
            report.longrepr.reprtraceback.reprentries[-1].lines = \
                report.longrepr.reprtraceback.reprentries[-1].lines[:2]

    if when == "call" and not report.passed:
        if item.config.getoption("--fail-debug-info"):
            fail_info = "Fail info not found."
            try:
                if hasattr(item.config, "get_fail_debug"):
                    fail_debug = item.config.get_fail_debug()
                    for k in (dict(os.environ)).keys():
                        if 'VAGGA' in k:
                            break
                    if fail_debug[0] == 'webdriver':
                        (
                            url,
                            screenshot,
                            test_case_url,
                            txid,
                            failed_test_command,
                        ) = fail_debug[1:]
                        test_case = (
                            "\nTEST CASE: {}".format(test_case_url)
                            if test_case_url else u''
                        )
                        run_test_command = (
                            "\nVAGGA COMMAND: {}".format(
                                failed_test_command
                            )

                        )
                        test_command = failed_test_command.split(' se ')[1]
                        run_docker_command = (
                            f"\nDOCKER COMMAND: docker-compose run se "
                            f"{test_command}"
                        )
                        fail_info = (
                            (
                                "\nURL: {url}"
                                "{test_case_url}"
                                "\nSCREENSHOT: {screenshot}"
                                "{run_test_command}"
                                "{run_docker_command}"
                                "\nTXID: {txid}"

                            ).format(
                                url=url,
                                screenshot=screenshot,
                                test_case_url=test_case,
                                run_test_command=run_test_command,
                                run_docker_command=run_docker_command,
                                txid=txid
                            )
                        )
                        extra.append(html_plugin.extras.url(
                            screenshot, name="SCREENSHOT"
                        ))
                        extra.append(
                            html_plugin.extras.html(
                                "<img src=\"{img}\" "
                                "height=\"230\" width=\"auto\" align=\""
                                "right\" bottom=\"0px\">Screenshot</img>"
                                .format(
                                    img=screenshot
                                )
                            )
                        )
                    elif fail_debug[0] == 'request':
                        (
                            url,
                            status_code,
                            test_case_url,
                            txid,
                            vagga_failed_test_command
                        ) = fail_debug[1:]
                        test_case = (
                            "\nTEST CASE: {}".format(test_case_url)
                            if test_case_url else u''
                        )
                        run_test_command = (
                            "\nVAGGA COMMAND: {}".format(
                                vagga_failed_test_command
                            )
                        )
                        test_command = (
                            vagga_failed_test_command.split(' se ')[1]
                        )
                        run_docker_command = (
                            f"\nDOCKER COMMAND: docker-compose run se "
                            f"{test_command}"
                        )
                        fail_info = (
                            "\nURL: {url} (status code: {status_code})"
                            "{test_case_url}"
                            "{run_test_command}"
                            "{run_docker_command}"
                            "\nTXID: {txid}"
                        ).format(
                            url=url,
                            status_code=status_code,
                            test_case_url=test_case,
                            run_test_command=run_test_command,
                            run_docker_command=run_docker_command,
                            txid=txid
                        )
                    extra.append(html_plugin.extras.url(
                        url, name="URL"
                    ))
                    extra.append(html_plugin.extras.url(
                        test_case_url, name="TEST CASE"
                    ))
                    report.extra = extra

            except WebDriverException as e:
                fail_info = (
                    "\nWebdriver instance must have crushed: {msg}".format(
                        msg=e.msg
                    )
                )
            finally:
                longrepr = getattr(report, 'longrepr', None)
                if hasattr(longrepr, 'addsection'):
                    longrepr.sections.insert(
                        0, ("Captured stdout %s" % when, fail_info, "-")
                    )

        if item.config.getoption("--duration-time"):
            duration = call.stop - call.start
            if duration > 120:
                report.sections.append((
                    "Captured stdout %s" % when,
                    ("\n\n!!!!! The very slow test. "
                     "Duration time is %s !!!!!\n\n")
                    % datetime.datetime.fromtimestamp(duration).strftime(
                        "%M min %S sec"
                    )
                ))


def pytest_configure(config):
    os.environ['PYTHONWARNINGS'] = (
        'ignore:An HTTPS request has been made, '
        'ignore:A true SSLContext object is not available, '
        'ignore:Unverified HTTPS request is being made'
    )

    if config.getoption('--headless'):
        os.environ['HEADLESS'] = 'Enabled'
    if config.getoption("--highlight"):
        os.environ['HIGHLIGHT'] = 'Enabled'
    if config.getoption("--capturelog"):
        config.pluginmanager.register(Logger(), "logger")
    if config.getoption("--check-console"):
        os.environ['CHECK_CONSOLE'] = 'Enabled'
    if not getattr(config, "lastfailed_file"):
        config.lastfailed_file = "lastfailed"
