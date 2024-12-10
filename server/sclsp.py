#!/usr/bin/env python3

import logging
import json
from pygls.server import LanguageServer
from pygls.workspace import TextDocument, Workspace
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    InitializeParams,
    TextDocumentSyncKind,
    TextDocumentItem,
    TEXT_DOCUMENT_COMPLETION
)

classes = None
methods = []
items = []

# Create the Language Server

logging.basicConfig(filename="server_lsp_mio.log", level=logging.DEBUG)

"""
class SuperColliderLanguageServer(LanguageServer):
    def __init__(self):
        super().__init__("supercollider-ls", "v0.1")
"""
server = LanguageServer("supercollider-ls", "v0.1")

# server = SuperColliderLanguageServer()

# Configura l'inizializzazione


def init():
    with open('./only_classes.txt', 'r') as f:
        global classes, items
        classes = f.readlines()
        classes = [_class.strip(None) for _class in classes]

    with open('./summaries.json', 'r') as j:
        summaries = json.load(j)

    with open('./all_methods.txt', 'r') as m:
        for method in m.readlines():
            # methods.append(method.strip(None))
            methods.append(CompletionItem(method.strip(
                None), kind=CompletionItemKind.Method))

    for _class in classes:
        items.append(CompletionItem(_class, kind=CompletionItemKind.Class,
                                    detail=summaries.get(_class)))

    return None


@server.feature("initialize")
def initialize(params: InitializeParams):
    logging.debug(f"Server initialized with params: {params}")
    return {
        "capabilities": {
            "textDocumentSync": TextDocumentSyncKind.Full,
            "completionProvider": {
                "resolveProvider": True,
                'triggerCharacters': ['.']
            },
        }
    }


# Implementa il completamento
@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams):
    # Esempio di completamenti per SuperCollider
    """
    completions = [
        CompletionItem("SinOsc", kind=CompletionItemKind.Class,
                       detail="Sine wave oscillator"),
        CompletionItem("play", kind=CompletionItemKind.Method,
                       detail="Play the current SynthDef"),
        CompletionItem(
            "Server.default", kind=CompletionItemKind.Property, detail="Default server"),
        CompletionItem(
            "boot", kind=CompletionItemKind.Property, detail="Default server")
    ]
    """

    uri = params.text_document.uri
    document = server.workspace.get_document(uri)
    position = params.position

    print(document)

    if is_class_context(document.source, position):
        return CompletionList(is_incomplete=False, items=methods)

    return CompletionList(is_incomplete=False, items=items)


def is_class_context(document, position):
    # Funzione per determinare se il contesto del completamento è all'interno di una classe
    # In questo esempio, verificiamo se la parola precedente è 'MyClass' e se c'è un punto subito dopo
    line = document.split('\n')[position.line]
    # Verifica se 'SinOsc' è nel contesto

    if "SinOsc" in line[:position.character]:
        return True

    return False


# Avvia il server
if __name__ == "__main__":
    """
    logging.debug("Starting SuperCollider Language Server...")
    server.start_io()
    logging.debug("Server stopped.")
    """
    init()
    logging.debug("Starting SuperCollider Language Server...")
    server.start_io()
    logging.debug("Server stopped.")
