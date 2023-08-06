from collections import namedtuple
import i3ipc as swayipc  # huh

__version__ = '0.1.0'

Rect = namedtuple('Rect', 'x y width height')
Mode = namedtuple('Mode', 'width height refresh')


class Monitor:
    def __init__(self, name, rect, active, modes, current_mode, **kwargs):
        self.name = name
        self.rect = Rect(**rect)
        self.active = active
        self.modes = [Mode(**mode) for mode in modes]
        self.current_mode = Mode(**current_mode) if current_mode else None

    @property
    def mode(self):
        return self.current_mode if self.current_mode else self.modes[-1]

    def disable(self):
        return f'output {self.name} disable'

    def enable(self, res=None, pos=(0, 0)):
        width, height, _ = res if res else self.mode
        return f'output {self.name} res {width}x{height} pos {pos[0]} {pos[1]}'


def extend(primary, secondary, side):
    if side == 'top':
        return [
            primary.enable(pos=(0, secondary.mode.height)),
            secondary.enable(),
        ]
    elif side == 'left':
        return [
            primary.enable(pos=(secondary.mode.width, 0)),
            secondary.enable(),
        ]
    elif side == 'right':
        return [
            primary.enable(),
            secondary.enable(pos=(primary.mode.width, 0)),
        ]
    elif side == 'bottom':
        return [
            primary.enable(),
            secondary.enable(pos=(0, primary.mode.height)),
        ]


def current_mode(primary, secondary):
    if primary.active and not secondary.active:
        return 'primary'
    elif not primary.active and secondary.active:
        return 'secondary'
    elif primary.rect.x != secondary.rect.x or \
            primary.rect.y != secondary.rect.y:
        return 'extend'
    return 'unknown'  # pragma: no cover


def prepare_commands(args, outputs):
    primary, secondary, *others = outputs
    if args.o:
        return [
            primary.enable(), secondary.disable(),
            *(other.disable() for other in others),
        ]
    elif args.s:
        return [
            secondary.enable(), primary.disable(),
            *(other.disable() for other in others),
        ]
    elif args.extend:
        return extend(primary, secondary, args.extend)
    else:
        print('Monitors:', len(outputs))
        print('Mode:', current_mode(primary, secondary))

        for i, output in enumerate(outputs):
            print(
                f'{i}:',
                f'{output.name}{"*" if output.name == args.primary else ""}',
                '(enabled)' if output.active else '(disabled)',
            )
        return []


def main(args):
    sway = swayipc.Connection()

    outputs = [Monitor(**output) for output in sway.get_outputs()]
    outputs.sort(key=lambda o: o.name != args.primary)

    for command in prepare_commands(args, outputs):
        sway.command(command)


def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        epilog='Without argument, it prints connected monitors list with '
               'their names and ids.\nOptions are exclusive and can be used '
               'in conjunction with extra options.'
    )

    options = parser.add_mutually_exclusive_group()
    options.add_argument(
        '-o',
        action='store_true',
        help='primary monitor only'
    )
    options.add_argument(
        '-s',
        action='store_true',
        help='second monitor only'
    )
    options.add_argument(
        '-e',
        choices=['top', 'left', 'right', 'bottom'],
        help='extends the primary monitor to the selected side',
        metavar='<side>',
    )

    parser.add_argument(
        '-p',
        help='select a connected monitor as the primary output',
        metavar='<mon_name>',
    )

    return parser
