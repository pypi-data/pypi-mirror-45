import argparse
import logging
import signal
import sys
from multiprocessing import Process
from typing import List, Text

import rasa.cli.run


# noinspection PyProtectedMember
def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    from rasa.core import cli

    shell_parser = subparsers.add_parser(
        "up",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Run the Rasa Interface",
    )

    shell_parser.add_argument(
        "--production", action="store_true", help="Run Rasa in a production environment"
    )

    shell_parser.add_argument("--auth_token", type=str, help="Rasa API auth token")

    shell_parser.add_argument(
        "--nlg",
        type=str,
        default="http://localhost:5002/api/nlg",
        help="Rasa NLG endpoint",
    )

    shell_parser.add_argument(
        "--model_endpoint_url",
        type=str,
        default=(
            "http://localhost:5002/api/projects/" "default/models/tags/production"
        ),
        help="Rasa Stack model endpoint URL",
    )

    shell_parser.add_argument(
        "--project_path",
        type=str,
        default=".",
        help="Path to the Rasa project directory",
    )
    shell_parser.add_argument(
        "--data_path",
        type=str,
        default="data",
        help="Path to the directory containing Rasa NLU training data "
        "and Rasa Core stories",
    )
    shell_parser.add_argument(
        "--vvvv", default=False, action="store_true", help="Verbose mode"
    )

    rasa.cli.run.add_run_arguments(shell_parser)

    shell_parser.set_defaults(func=up)

    cli.arguments.add_logging_option_arguments(shell_parser)


def start_event_service():
    from rasa_platform.services.event_service import main

    main()


def start_core(args: argparse.Namespace, endpoints: "AvailableEndpoints" = None):
    """Starts the Rasa Core application."""
    from rasa.core.run import serve_application

    if endpoints is None:
        from rasa.core.utils import AvailableEndpoints

        endpoints = AvailableEndpoints.read_endpoints(args.endpoints)

    serve_application(
        endpoints=endpoints,
        port=args.port,
        credentials=args.credentials,
        cors=args.cors,
        auth_token=args.auth_token,
        enable_api=True,
        jwt_secret=args.jwt_secret,
        jwt_method=args.jwt_method,
    )


def start_core_for_local_platform(args: argparse.Namespace, platform_token: Text):
    """Starts the Rasa API with Rasa Core as a background process."""

    from rasa.core.utils import AvailableEndpoints
    from rasa.utils.endpoints import EndpointConfig

    endpoints = AvailableEndpoints(
        model=EndpointConfig(
            args.model_endpoint_url, token=platform_token, wait_time_between_pulls=2
        ),
        nlg=EndpointConfig(args.nlg, token=platform_token),
        tracker_store=EndpointConfig(type="sql", db="tracker.db"),
    )

    vars(args).update(
        dict(
            nlu_model=None,
            channel="rasa",
            credentials="credentials.yml",
            cors="*",
            auth_token=args.auth_token,
            enable_api=True,
            endpoints=endpoints,
        )
    )

    p = Process(target=start_core, args=(args, endpoints))
    p.start()


def up(args: argparse.Namespace):
    from rasa.cli.utils import print_success, print_error, signal_handler
    from rasa.core.utils import configure_file_logging
    from rasa.utils.io import configure_colored_logging

    signal.signal(signal.SIGINT, signal_handler)

    logging.getLogger("werkzeug").setLevel(logging.WARN)
    logging.getLogger("engineio").setLevel(logging.WARN)
    logging.getLogger("socketio").setLevel(logging.ERROR)

    if not args.vvvv:
        logging.getLogger().setLevel(logging.ERROR)
        logging.getLogger("py.warnings").setLevel(logging.ERROR)
        logging.getLogger("rasa.cli").setLevel(logging.ERROR)
        logging.getLogger("sanic.root").setLevel(logging.ERROR)
        logging.getLogger("rasa.core").setLevel(logging.ERROR)
        logging.getLogger("rasa.nlu").setLevel(logging.ERROR)

        # TODO: remove once https://github.com/RasaHQ/rasa_nlu/issues/3120
        # is fixed
        logging.getLogger("apscheduler").setLevel(logging.ERROR)

    configure_colored_logging(args.loglevel)
    configure_file_logging(args.loglevel, args.log_file)

    if args.production:
        print_success("Starting Rasa Core")
        start_core(args)
    else:
        try:
            from rasa_platform import config
            from rasa_platform.api.local import main_local
        except ImportError as e:
            print_error(
                "Rasa X is not installed. The `rasa up` "
                "command requires an installation of Rasa X."
                "Error:\n{}".format(e)
            )
            sys.exit()

        print_success("Starting Rasa 🚀")

        p = Process(target=start_event_service)
        p.start()

        start_core_for_local_platform(args, config.platform_token)

        main_local(args.project_path, args.data_path)
