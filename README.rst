Simple `nose` plugin that enables developers to run subset of collected tests
to spare some waiting time for better things. 

Usage
-----

Examples of using the plugin on the plugin package itself:

Run all tests::

    $ nosetests -v

    test_configure_complex (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_empty_string (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_case_insensitive (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_negative (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_unselected (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_unselected_override (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_wildcard (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_options (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_prepareTestCase_exclude (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_prepareTestCase_select (noseselecttests.tests.NoseSelectPluginTest) ... ok

    ----------------------------------------------------------------------
    Ran 13 tests in 0.008s

    OK

Only run tests with keyword `configure`::

    $ nosetests -v -t configure

    test_configure_complex (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_empty_string (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.006s

    OK

Case insensitive::

    $ nosetests -v -t CONFIGURE

    test_configure_complex (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_empty_string (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.006s

    OK

Only run tests with keyword `configure` but exclude tests with keyword `complex`::

    $ nosetests -v -t configure -e complex

    test_configure_empty_string (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 0.006s

    OK

Multiple keywords resolve to ``OR`` operation::

    $ nosetests -v -t none -t simple

    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_is_selected_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.018s
    
    OK


To just exclude some tests, use `-e` which is provided by `nose` itself::

    $ nosetests -v -e is_selected

    test_configure_complex (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_empty_string (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_none (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_configure_simple (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_options (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_prepareTestCase_exclude (noseselecttests.tests.NoseSelectPluginTest) ... ok
    test_prepareTestCase_select (noseselecttests.tests.NoseSelectPluginTest) ... ok

    ----------------------------------------------------------------------
    Ran 7 tests in 0.005s

    OK
