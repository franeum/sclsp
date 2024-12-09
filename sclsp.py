#!/usr/bin/env python3

import logging
import json
from pygls.server import LanguageServer
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    InitializeParams,
    TextDocumentSyncKind,
    TEXT_DOCUMENT_COMPLETION
)

classes = None
items = []

# Create the Language Server

logging.basicConfig(filename="server_lsp_mio.log", level=logging.DEBUG)


class SuperColliderLanguageServer(LanguageServer):
    def __init__(self):
        super().__init__("supercollider-ls", "v0.1")


server = SuperColliderLanguageServer()

# Configura l'inizializzazione


def init():
    with open('./only_classes.txt', 'r') as f:
        global classes, items
        classes = f.readlines()
        classes = [_class.strip(None) for _class in classes]

    with open('./summaries.json', 'r') as j:
        summaries = json.load(j)

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

    document = params.text_document
    position = params.position

    print(document)

    if is_class_context(document, position):
        methods = [
            CompletionItem(
                label="method1", kind=CompletionItemKind.Method, insert_text="method1()"),
            CompletionItem(
                label="method2", kind=CompletionItemKind.Method, insert_text="method2()"),
        ]
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
