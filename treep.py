#!/usr/bin/env python3
"""
Este comando, um clone simplifcado do comando tree utilizado em Linux, 
lista o conteúdo de directorias num formato semelhante a uma árvore.

A sintaxe de invocação é a seguinte:

    $ treep [-df] [-L <level>] <directory>

Consulte a ajuda do comando tree ("man tree" em Linux, também disponível
na Web) para obter o signifcado das opções -d, -f e -L. É utilizada a 
biblioteca argparse para análise dos argumentos da linha de comandos.
"""

import sys
import os
from typing import List

# Em baixo vamos utilizar um 'namedtuple'. Um namedtuple é um objecto
# similar a tuplo mas a cujos membros podemos aceder através de um
# índice ou de um nome.
#
# Exemplo:
#   from collections import namedtuple
#
#   Pessoa = namedtuple('Pessoa', 'nome apelido') 
#   pessoa1 = Pessoa('Alberto', 'Antunes')
#   pessoa2 = Pessoa(nome='Armando', apelido='Alves')
#   pessoa3 = Pessoa(apelido='Almeida', nome='António')
#
#   print(pessoa1[0], pessoa1[1])         # mostra "Alberto Antunes"
#   print(pessoa1.nome, pessoa1.apelido)  # mostra "Alberto Antunes"
#   print(pessoa2.nome, pessoa2.apelido)  # mostra "Armando Alves"
#   pessoa1 = pessoa1._replace(apelido='Amaral')  # devolve um novo tuplo 
#   print(pessoa1.nome, pessoa1.apelido)  # mostra "Alberto Amaral"
#
#   type(pessoa1)  # mostra <class 'Pessoa'>
#   isinstance(pessoa1, Pessoa)  # True
#
#   # Alternativamente podemos definir Pessoa das seguintes formas:
#   Pessoa = namedtuple('Pessoa', 'nome, apelido')
#   Pessoa = namedtuple('Pessoa', ['nome', 'apelido'])
#
# Um namedtuple é um tipo agregado de dados imutável. É semelhante
# a uma struct em C ou a um record em Pascal. É útil quando queremos
# agregar um conjunto de atributos relacionados entre si. No exemplo
# anterior agregámos nome e apelido. Seria um tipo estruturado de 
# dados se cada um dos atributos tivesse um tipo de dados definido.
# Podíamos ter utilizado uma classe, mas um namedtuple é mais simples
# e eficiente do que uma classe (mas mais limitado). Também podíamos
# ter utilizado um dicionário. Mas um dicionário é menos conveniente
# além do que não nos dá um tipo de dados específico (eg, 'Pessoa').
#
#   pessoa4 = {'nome': 'Alberto', 'apelido': 'Antunes'}
#   print(pessoa4['nome'], pessoa4['apelido'])
#   pessoa4['apelido'] = 'Amaral'
#   type(pessoa4)  # mostra <class 'dict'> e não <class 'Pessoa'>
#   isinstance(pessoa4, dict)  # True
# 

from dataclasses import dataclass

@dataclass(frozen=True)
class DirEntry():
    """
    A directory entry is just a node in a directory tree. It's either a 
    directory or a file (for now, other entry types, like soft links, 
    fifos, sockets, etc., are ignored), packed with some extra attributes 
    to make it easier to render the directory tree. 
    Field 'path' is the path relative to a base or start dir and
    'is_dir' indicates if the entry is a directory or not.
    The 'depth', or level, of an entry is the number of levels
    counting from base dir. 'children' is a list of directory entries that are
    the offspring of this 'DirEntry' and 'ndesc' is the number of 
    descendants (children, grand-childrent, etc.) of this 'DirEntry'.
    """
    path: str 
    is_dir: bool 
    depth: int 
    children: List['DirEntry']
    ndesc: int

    @classmethod
    def with_base_dir(
            cls,
            base_dir: str,
            path: str,
            is_dir: bool,
            children: List['DirEntry'] = None,
            ndesc: int = 0,
    ) -> 'DirEntry':
        assert bool(children) == bool(ndesc)  # has children iff has descendants
        assert is_dir or not children         # not a dir implies no children
        if children is None:                  #     (and no descendants)
            children = []            
        entry_rel_path = path.partition(base_dir)[-1]
        depth = entry_rel_path.count(os.path.sep)        
        return cls(path, is_dir, depth, children, ndesc)
    #:
#:

def make_tree(base_dir: str, dirs_only: bool=False, max_depth: int = 2**32) -> DirEntry:
    """
    Recursively build a tree rooted at base dir. Returns the root 
    'DirEntry' and the tree depth.

    Given the directory below,

        tmp2/
        |--- bin/
        |    |--- sheet.pdf
        |--- data.txt
        |--- file.bin
        |--- local/

    make_tree returns a 'DirEntry' that looks like the following 
    ('DE' is shorthand for 'DirEntry'; 'is_dir' omitted for brevity):

    DE(path='tmp2', depth=0, ndesc=5, children=[
        DE(path='tmp2/bin', depth=1, ndesc=1, children=[
             DE(path='tmp2/bin/sheet.pdf', depth=2, ndesc=0, children=[])
        ]), 
        DE(path='tmp2/data.txt', depth=1, ndesc=0, children=[]), 
        DE(path='tmp2/file.bin', depth=1, ndesc=0, children=[]), 
        DE(path='tmp2/local', depth=1, ndesc=0, children=[])
    ])
    """
    tree_depth = -1  # this will be the actual treep_depth of this tree
    ndirs = 0
    nfiles = 0
    join_paths = os.path.join

    def do_make_tree(start_dir, depth):
        nonlocal tree_depth, ndirs, nfiles
        curr_dir, subdirs, files = next(os.walk(start_dir))

        children = []
        if depth < max_depth:
            ndirs += len(subdirs)
            children += [
                do_make_tree(join_paths(start_dir, subdir), depth + 1) 
                for subdir in subdirs
            ]
            if not dirs_only:
                nfiles += len(files)
                children += [
                    DirEntry.with_base_dir(base_dir, join_paths(curr_dir, file), False)
                    for file in files
                ]
        children.sort(key=lambda entry: str.lower(entry.path))

        tree_depth = max(tree_depth, depth + bool(files))
        ndesc = len(children) + sum(entry.ndesc for entry in children)
        return DirEntry.with_base_dir(base_dir, curr_dir, True, children, ndesc)

    return do_make_tree(base_dir, 0), tree_depth, ndirs, nfiles
#:

def render_tree(tree: DirEntry, depth: int, full_path: bool=False) -> List[List[str]]:
    """
    Builds a "screen" object, a matrix with as many rows as the number
    of 'tree' descendants, and as many columns as the 'depth' of the
    tree.
    Then it "draws" the tree in that "screen" object. 
    """
    screen = [['' for h in range(depth + 1)] for l in range(tree.ndesc + 1)]

    def do_rendering(entry, start_line):
        # Insert the appropriate path into the appropriate cell
        path = entry.path if full_path else os.path.basename(entry.path)
        if entry.is_dir:
            path += '/'
        screen[start_line][entry.depth] = path

        # Render the column below this entry.
        line = start_line + 1
        for child in entry.children:
            # Render connection coming from the left for this child
            last = child is entry.children[-1]
            screen[line][entry.depth] = "└── " if last else "├── " 

            # Render a connection to the tree for each descendant of 
            # the current child
            left = "    " if last else "│   "
            for i in range(child.ndesc):
                screen[line + i + 1][entry.depth] = left

            # Recursively render child
            do_rendering(child, line)
            line += child.ndesc + 1
        #:
    #:
    do_rendering(tree, 0)
    return screen
#:

def list_dirs(
        dirs,         
        dirs_only=False, 
        full_path=False, 
        max_depth=2**32,
        out=sys.stdout,
):
    for base_dir in dirs:
        if not os.path.isdir(base_dir):
            print("Path %s is not a directory" % base_dir, file=sys.stderr)
            continue

        base_dir = os.path.normpath(base_dir)
        tree, depth, ndirs, nfiles = make_tree(base_dir, dirs_only, max_depth)
        screen = render_tree(tree, depth, full_path)

        print('\n'.join(''.join(line) for line in screen))
        print()
        print(ndirs, "directory" if ndirs == 1 else "directories", end=", ")
        print(nfiles, "file" if nfiles == 1 else "files")
    #:
#:

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Tree clone")
    parser.add_argument(
        '-d',
        help="List directories only",
        action='store_true',
    )
    parser.add_argument(
        '-f',
        help="Print the full path prefix for each file",
        action='store_true',
    )
    parser.add_argument(
        '-L',
        help="Max display depth of the directory tree.",
        type=int,
        metavar='<level>',
        default=2**32,
    )
    parser.add_argument(
        'directory',
        help="Directory to be listed.",
        metavar='<directory>',
        default='.',
        nargs='?',
    )
    # Se pretendessemos zero ou mais caminhos
    #
    # parser.add_argument(
    #     'directory',
    #     help="Directory to be listed.",
    #     metavar='<directory>',
    #     nargs='*'       # '+' para um ou mais caminhos
    # )

    args = parser.parse_args()
    list_dirs(
        [args.directory], 
        dirs_only=args.d,
        full_path=args.f,
        max_depth=args.L,
    )
#:
