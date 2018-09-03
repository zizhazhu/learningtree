class Inner:

    def __init__(self, name, extends):
        self.name = name
        self.extends = extends


class Outter:

    def __init__(self, name):
        self.name = name


class Field:

    def __init__(self, name, inners):
        self.name = name
        self.inners = inners


class Context:
    def __init__(self, result, tab):
        self.result = result
        self.tab = tab
        self.end = '\n'
        self.link = []

    def add(self, line):
        self.result += self.tab + line + self.end

    def addlink(self, src, des):
        self.link.append('{} -> {}'.format(src, des))

    def writelink(self):
        for line in self.link:
            self.result += self.tab + line + self.end

    def __str__(self):
        return self.result


class PrintContext:

    def __init__(self, context, name=''):
        self.context = context
        self.name = name

    def __enter__(self):
        self.context.tab += '\t'

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.tab = self.context.tab[:-1]
        self.context.add('}')


class PrintGraph(PrintContext):

    def __init__(self, context, name='G'):
        super().__init__(context, name)

    def __enter__(self):
        self.context.add('digraph G {')
        super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.writelink()
        super().__exit__(exc_type, exc_val, exc_tb)


class PrintSubGraph(PrintContext):

    def __init__(self, context, name):
        super().__init__(context, name)

    def __enter__(self):
        self.context.add('subgraph cluster{} {{'.format(self.name))
        super().__enter__()


class Graph:

    def __init__(self, fields):
        self.fields = fields

    def output(self):
        inners = set()
        outters = set()
        context = Context(result='', tab='')
        end = ''
        with PrintGraph(context):
            with PrintSubGraph(context, 0):
                for field in self.fields:
                    context.add(field.name)
                    for inner in field.inners:
                        inners.add(inner)
                        context.addlink(field.name, inner.name)
            with PrintSubGraph(context, 1):
                for inner in inners:
                    context.add(inner.name)
                    for extend in inner.extends:
                        outters.add(extend)
                        context.addlink(inner.name, extend.name)
            with PrintSubGraph(context, 2):
                for outter in outters:
                    context.add(outter.name)
            context.add(end)
        return context


def main():
    dlp = Outter('dlp')
    dlt = Inner('dlt', [dlp])
    com = Field('com', [dlt])
    with open('my_tree.gv', 'w') as file:
        file.write(str(Graph([com]).output()))


if __name__ == '__main__':
    main()
