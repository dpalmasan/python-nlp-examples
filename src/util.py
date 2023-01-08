from nltk.corpus.reader import xmldocs
from nltk import tree
from nltk.util import LazyMap, LazyConcatenation
from nltk.corpus.reader import SyntaxCorpusReader
from typing import List
from typing import Tuple
import xml


class AncoraCorpusReader(SyntaxCorpusReader):
    """Implementación lectura de CORPUS AnCora."""

    def __init__(self, path: str, files: List[str] = None):
        """Constructor.

        Si no se provee una lista de archivos, lee el CORPUS completo.

        :param path: Ruta al directorio del CORPUS.
        :type path: str
        :param files: Lista de archivos a considerar, defaults to None
        :type files: List[str], optional
        """
        if files is None:
            files = ".*\.tbf\.xml"
        self.xmlreader = xmldocs.XMLCorpusReader(path, files)

    @staticmethod
    def parsed(element):
        """Procesa corpus.

        Convierte una 'oración' XML element (xml.etree.ElementTree.Element) a
        un árbol en formato NLTK.
        element -- the XML sentence element (or a subelement)

        :param element: Oración a procesar.
        :type element: xml.etree.ElementTree.Element
        :return: Árbol en formato NLTK
        :rtype: tree.Tree
        """
        if element:
            subtrees = map(AncoraCorpusReader.parsed, element)
            subtrees = [t for t in subtrees if t is not None]
            return tree.Tree(element.tag, subtrees)
        else:
            if element.get("elliptic") == "yes" and not element.get("wd"):
                return None
            else:
                return tree.Tree(
                    element.get("pos") or element.get("ne") or "unk",
                    [element.get("wd")],
                )

    @staticmethod
    def tagged(element: xml.etree.ElementTree.Element) -> List[Tuple[str, str]]:
        """Convierte elemento de XML a oración etiquetada.

        :param element: Oración a procesar.
        :type element: xml.etree.ElementTree.Element
        :return: Lista de tags de la oración.
        :rtype: List[Tuple[str, str]]
        """
        pos = AncoraCorpusReader.parsed(element).pos()
        # Puede terminar en lista vacía!
        return list(filter(lambda x: x[0] is not None, pos))

    @staticmethod
    def untagged(element: xml.etree.ElementTree.Element) -> List[str]:
        """Obtiene lista de palabras sin etiqueta.

        :param element: Oración a procesar.
        :type element: xml.etree.ElementTree.Element
        :return: Lista de palabras de la oración.
        :rtype: List[str]
        """

        sent = AncoraCorpusReader.parsed(element).leaves()
        return list(filter(lambda x: x is not None, sent))

    def parsed_sents(self, fileids=None):
        """Obteniene oraciones como árboles NLTK."""
        return LazyMap(AncoraCorpusReader.parsed, self.elements(fileids))

    def tagged_sents(self, fileids=None):
        """Obtiene oraciones como tuplas de palabras/tag."""
        return LazyMap(AncoraCorpusReader.tagged, self.elements(fileids))

    def sents(self, fileids=None):
        """Obtiene oraciones como listas de palabras."""
        return LazyMap(AncoraCorpusReader.untagged, self.elements(fileids))

    def elements(self, fileids=None):
        """Obtiene lista de oraciones como elementos XML."""
        if not fileids:
            fileids = self.xmlreader.fileids()
        return LazyConcatenation(self.xmlreader.xml(f) for f in fileids)

    def tagged_words(self, fileids=None):
        """Obtiene listas de palabras etiquetdas como tuplas palbra/tag."""
        return LazyConcatenation(self.tagged_sents(fileids))

    def __repr__(self):
        return "<AncoraCorpusReader>"


class SimpleAncoraCorpusReader(AncoraCorpusReader):
    """Ancora Corpus con conjunto de tags simplificados de Stanford.

    Revisar el siguiente enlace para ver descripción de los tags.
    https://nlp.stanford.edu/software/spanish-faq.shtml#tagset
    """

    def __init__(self, path, files=None):
        super().__init__(path, files)

    @staticmethod
    def simple_tag(t: str) -> str:
        """Convierte etiqueta Ancora en Stanford.

        :param t: Etiqueta a convertir.
        :type t: str
        :return: Etiqueta en formato Stanford.
        :rtype: str
        """
        if t.startswith("a"):
            return t[:2] + "0000"
        if t.startswith("d"):
            return t[:2] + "0000"
        if t.startswith("f"):
            return t
        if t in ["cc", "cs", "i", "w", "zm", "zu"]:
            return t
        if t.startswith("nc"):
            return "nc0{}000".format(t[3])
        if t.startswith("np"):
            return "np00000"
        if t.startswith("p"):
            return t[:2] + "000000"
        if t.startswith("r"):
            return t
        if t.startswith("sp"):
            return "sp000"
        if t.startswith("v"):
            return t[:4] + "000"
        if t.startswith("z"):
            return "z0"
        # Probablemente inválido o "unk"
        return t

    def tagged_sents(self, fileids=None):
        """Obtener oraciones etiquetadas con tags de Stanford."""

        def f(s):
            return [(w, SimpleAncoraCorpusReader.simple_tag(t)) for w, t in s]

        return LazyMap(f, super().tagged_sents(fileids))

    def parsed_sents(self, fileids=None):
        """Obtener arboles NLTK etiquetados con tags de Stanford."""

        def f(t):
            for p in t.treepositions("leaves"):
                if len(p) > 1:
                    tag = t[p[:-1]].label()
                    t[p[:-1]].set_label(SimpleAncoraCorpusReader.simple_tag(tag))
            return t

        return LazyMap(f, super().parsed_sents(fileids))