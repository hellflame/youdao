import json
import os


class Config:
    def __init__(self, conf_dir, default_data):
        self.config_path = conf_dir
        self.config = {}
        self.default = default_data
        self.check_path()

    def check_path(self):
        dirs = self.config_path[: self.config_path.rindex('/')]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as handle:
                handle.write(json.dumps(self.default, indent=2))

    def save(self):
        with open(self.config_path, 'w') as handle:
            handle.write(json.dumps(self.config, indent=2))

    def load(self):
        with open(self.config_path) as handle:
            self.config = json.loads(handle.read())
        return self.config


if __name__ == '__main__':
    test = Config('/home/hellflame/test/fine.conf', default_data={'author': 'hellflame'})
    #test.config['name'] = 'hellflame'
    #test.save()
    print(test.load())

