from rprojc import StandardProject

class Application(StandardProject):
    def do(self):
        print(self.config)

if __name__ == '__main__':
    app = Application('test')
    app.do()       