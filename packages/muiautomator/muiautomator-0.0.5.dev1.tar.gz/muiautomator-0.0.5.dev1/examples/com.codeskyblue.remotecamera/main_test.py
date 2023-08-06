# coding: utf-8

import muiautomator as u2


pkg_name = 'com.codeskyblue.remotecamera'
d = u2.connect()


def setup_function():
    d.app_start(pkg_name)


def test_simple():
    assert d(text="Hello World!").exists

