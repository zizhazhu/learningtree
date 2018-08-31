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


class Graph:

    def __init__(self, fields):
        self.fields = fields

    def output(self):
        inners = set()
        outters = set()
        result = ''
        end = ''
        result += 'digraph G {\n'
        result += '\tsubgraph cluster_0 {\n'
        for field in self.fields:
            result += '\t\t' + field.name + ';\n'
            for inner in field.inners:
                inners.add(inner)
                end += '\t{} -> {};\n'.format(field.name, inner.name)
        result += '\t}\n'
        result += '\tsubgraph cluster_1 {\n'
        for inner in inners:
            result += '\t\t' + inner.name + ';\n'
            for extend in inner.extends:
                outters.add(extend)
                end += '\t{} -> {};\n'.format(inner.name, extend.name)
        result += '\t}\n'
        result += '\tsubgraph cluster_2 {\n'
        for outter in outters:
            result += '\t\t' + outter.name + ';\n'
        result += '\t}\n'
        result += '\n'
        result += end
        result += '}\n'
        return result


def main():
    dlp = Outter('dlp')
    dlt = Inner('dlt', [dlp])
    com = Field('com', [dlt])
    with open('my_tree.gv', 'w') as file:
        file.write(Graph([com]).output())


if __name__ == '__main__':
    main()
