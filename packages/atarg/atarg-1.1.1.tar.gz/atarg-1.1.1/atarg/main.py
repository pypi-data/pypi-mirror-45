import argparse
import sys

from atarg import utils
from atarg.testcase import run_tests
from atarg.submit import submit


def parse_arguments():
    CONTESTS = ['ABC', 'ARC', 'AGC']
    TASKS = ['A', 'B', 'C', 'D']
    parser = argparse.ArgumentParser(
            prog='atarg',
            description='Testing tool before submit for atcoder',
            epilog='end',
            add_help=True,
            )
    parser.add_argument('-s', '--submit', help='submit source code', action='store_true')
    parser.add_argument('contest', choices=CONTESTS, help='Contest name')
    parser.add_argument('contest_no', type=int, help='Contest No.')
    parser.add_argument('task', choices=TASKS, help='Task name')
    parser.add_argument(
            'command',
            help='Commands or File to solve',
            nargs='+')
    return parser.parse_args()


def main():
    args = parse_arguments()
    task = utils.translate_task(args.contest, args.contest_no, args.task)

    if args.submit:
        source_code_filename = args.command[0]
        submit(args.contest, args.contest_no, args.task, source_code_filename)
    else:
        url = utils.compose_task_url(args.contest, args.contest_no, task)
        inputs_and_outputs = utils.fetch_inputs_and_outputs(url, args.contest, args.contest_no)
        inputs = inputs_and_outputs[::2]
        outputs = inputs_and_outputs[1::2]
        run_tests(inputs, outputs, args.command)


if __name__ == '__main__':
    main()
