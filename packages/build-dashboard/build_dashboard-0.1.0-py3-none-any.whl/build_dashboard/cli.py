from os import environ, path
from argparse import ArgumentParser
from build_dashboard.model import BuildbotModel, BuildbotClient
from build_dashboard.views import BuildbotView
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import toml

def run(screen, old_scene, model):
    scenes = [Scene([BuildbotView(screen, model)], -1, name="BuildbotView")]
    screen.play(scenes, 
        stop_on_resize=True, 
        start_scene=old_scene)

def main():
    parser = ArgumentParser(prog='build_dashboard', description='A buildbot client')
    parser.add_argument('--unix', type=str)
    parser.add_argument('--config', type=str)
    parser.add_argument('--protocol', type=str)
    parser.add_argument('--host', type=str)
    args = parser.parse_args()
    
    config_file = None
    if args.config:
        config_file = args.config
    elif environ.get('HOME') != None:
        config_file = environ.get('HOME') + '/.buildbotrc'

    config = {}

    if (config_file is not None and
            path.exists(config_file)):
        with open(config_file) as f:
            config.update(toml.load(f))

    for key in vars(args):
        value = getattr(args, key)
        if value != None:
            config[key] = value

    client = BuildbotClient(
            path=config.get('unix', None), 
            protocol=config.get('protocol', 'http'),
            host=config.get('host', 'localhost'))
    
    model = BuildbotModel(client)

    last_scene = None
    while True:
        try:
            Screen.wrapper(run, catch_interrupt=False, arguments=[last_scene, model])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        except KeyboardInterrupt as e:
            break

