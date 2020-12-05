#!/usr/bin/env python3
import argparse
import json


def main(arguments):
    path = "/tmp/centreon_matrix_bridge.fifo"

    message = {
        "type": "host" if args.host else "service",
        "level": arguments.level,
        "host": arguments.hostname,
        "output": arguments.output,
        "target": arguments.target
    }
    if args.service:
        message["description"] = arguments.description
    if args.host:
        message["alias"] = arguments.alias

    with open(path, "w") as fifo:
        fifo.write(json.dumps(message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--service",
        action="store_true",
        dest="service",
        help="Specify if notification is a Service Notification"
    )
    parser.add_argument(
        "--host",
        action="store_true",
        dest="host",
        help="Specify if notification is a Host Notification"
    )
    parser.add_argument(
        "--level",
        action="store",
        dest="level",
        required=True,
        help="Level of notification"
    )
    parser.add_argument(
        "--hostname",
        action="store",
        dest="hostname",
        required=True,
        help="Hostname"
    )
    parser.add_argument(
        "--description",
        action="store",
        dest="description",
        help="Service description"
    )
    parser.add_argument(
        "--alias",
        action="store",
        dest="alias",
        help="Alias of the host"
    )
    parser.add_argument(
        "--output",
        action="store",
        dest="output",
        required=True,
        help="Output of the service"
    )
    parser.add_argument(
        "--url",
        action="store",
        dest="url",
        help="URL to centreon"
    )
    parser.add_argument(
        "--target",
        action="store",
        dest="target",
        required=True,
        help="Target group to send the notification to"
    )
    args = parser.parse_args()
    main(args)
