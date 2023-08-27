"""
.. module:: contextpaths
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`ContextPaths` enumeration which is an enumeration
               of wellknown context paths.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from enum import Enum

class ContextPaths(str, Enum):

    # ========================== environment paths ==============================
    BEHAVIORS_LOG_CONFIGURATION = "/environment/behaviors/log-configuration-declarations"

    BUILD_RELEASE = "/environment/build/release"
    BUILD_BRANCH = "/environment/build/branch"
    BUILD_FLAVOR = "/environment/build/flavor"
    BUILD_NAME = "/environment/build/name"
    BUILD_URL = "/environment/build/url"

    CONFIG_CREDENTIAL_NAMES = "/environment/credential/names"
    CONFIG_CREDENTIAL_URIS = "/environment/credential/uris"
    CONFIG_CREDENTIAL_SOURCES = "/environment/credential/sources"

    CONFIG_LANDSCAPE_NAMES = "/environment/landscape/names"
    CONFIG_LANDSCAPE_URIS = "/environment/landscape/uris"
    CONFIG_LANDSCAPE_SOURCES = "/environment/landscape/sources"

    CONFIG_RUNTIME_NAMES = "/environment/runtime/names"
    CONFIG_RUNTIME_URIS = "/environment/runtime/uris"
    CONFIG_RUNTIME_SOURCES = "/environment/runtime/sources"

    CONFIG_TOPOLOGY_NAMES = "/environment/topology/names"
    CONFIG_TOPOLOGY_URIS = "/environment/topology/uris"
    CONFIG_TOPOLOGY_SOURCES = "/environment/topology/sources"

    JOB_ID = "/environment/job/id"
    JOB_INITIATOR = "/environment/job/initiator"
    JOB_LABEL = "/environment/job/label"
    JOB_NAME = "/environment/job/name"
    JOB_OWNER = "/environment/job/owner"
    JOB_TYPE = "/environment/job/type"

    LOGFILE_DEBUG = "/environment/logfile_debug"
    LOGFILE_OTHER = "/environment/logfile_other"

    PIPELINE_ID = "/environment/pipeline/id"
    PIPELINE_NAME = "/environment/pipeline/name"
    PIPELINE_INSTANCE = "/environment/pipeline/instance"

    RUNTIME_HOME_DIRECTORY = "/environment/runtime/home"
    RUNTIME_CONFIG_DIRECTORY = "/environment/runtime/config"

    OUTPUT_DIRECTORY = "/environment/output_directory"

    RUNID = "/environment/runid"
    STARTTIME = "/environment/starttime"

    # ========================== configuration paths ==============================
    CONFIG_CREDENTIALS = "/configuration/credentials"
    CONFIG_LANDSCAPE = "/configuration/landscape"
    CONFIG_RUNTIME = "/configuration/runtime"
    CONFIG_TOPOLOGY = "/configuration/topology"

    DATABASES = "/configuration/runtime/databases"

    DEBUG_BREAKPOINTS = "/configuration/runtime/breakpoints"
    DEBUG_DEBUGGER = "/configuration/runtime/debugger"

    DIR_RESULTS_RESOURCE_DEST = "/configuration/runtime/results-configuration/static-resource-dest-dir"
    DIR_RESULTS_RESOURCE_SRC = "/configuration/runtime/results-configuration/static-resource-src-dir"

    FILE_RESULTS_TEMPLATE = "/configuration/runtime/results-configuration/html-template"

    LOGGING_LEVEL_CONSOLE = "/configuration/runtime/logging/levels/console"
    LOGGING_LEVEL_LOGFILE = "/configuration/runtime/logging/levels/logfile"

    LOGGING_LOGNAME = "/configuration/runtime/logging/logname"
    LOGGING_BRANCHED = "/configuration/runtime/logging/branched"

    RESULT_PATH_FOR_CONSOLE = "/configuration/runtime/paths/results/console"
    RESULT_PATH_FOR_ORCHESTRATION = "/configuration/runtime/paths/results/orchestration"
    RESULT_PATH_FOR_SERVICES = "/configuration/runtime/paths/results/service"
    RESULT_PATH_FOR_TESTS = "/configuration/runtime/paths/results/tests"

    SKIPPED_DEVICES = "/configuration/runtime/skip-devices"

    TEMPLATE_PATH_FOR_CONSOLE = "/configuration/runtime/paths-templates/results/console"
    TEMPLATE_PATH_FOR_TESTS = "/configuration/runtime/paths-templates/results/tests"

    TESTROOT = "/configuration/runtime/testroot"

    TIMETRAVEL = "/configuration/runtime/timetravel"
    TIMEPORTALS = "/configuration/runtime/timeportals"

    UPNP_EXCLUDE_INTERFACES = "/configuration/runtime/networking/protocols/upnp/exclude_interfaces"
    UPNP_LOGGED_EVENTS = "/configuration/runtime/networking/protocols/upnp/subscriptions/logged-events"
