import base64
import io
import sys
from os import walk
from os.path import abspath, isdir, join
from typing import TypedDict

import xmlschema
from xmlschema import XMLSchema
from xmlschema.exceptions import XMLResourceParseError
from xmlschema.validators.exceptions import (
    XMLSchemaParseError,
    XMLSchemaValidationError,
)

from linter.exceptions import (
    LinterError,
    LinterErrorType,
    LinterSuccess,
    LinterSuccessType,
)


class Content(TypedDict):
    Content: str


class Document(TypedDict):
    Document: Content


class DocumentRel(TypedDict):
    DocumentRel: list[Document]


class Linter:
    def __init__(self, xsd_dir: str = "xsd"):
        self.xsd_dir: str = xsd_dir
        self.create_schema()
        # TODO: Temp solution
        if self.schema is None:
            raise Exception

    def create_schema(self):
        xsds = self.find_xsd_files(self.xsd_dir)
        self.schema: XMLSchema | None = self.load_schema(xsds)

    def validate(self, file: str | io.StringIO) -> LinterError | LinterSuccess:
        if self.schema is None:
            self.schema = self.create_schema()

        result = self.validate_xml(file)
        if isinstance(result, LinterSuccess):
            # If root XML file is valid, check Documents
            if self.schema is not None:
                data = self.schema.to_dict(file)  # TODO: Fix this typing
            base64_docs = self.extract_base64_documents(data)  # type: ignore
            if base64_docs:
                result = self.validate_base64_documents(base64_docs)
        return result

    def find_xsd_files(self, xsd_dir: str) -> list[str]:
        if not isdir(xsd_dir):
            raise LinterError(LinterErrorType.NOT_A_DIRECTORY)
        xsds: list[str] = []
        for path, _, files in walk(xsd_dir, topdown=True):
            xsds.extend(abspath(join(path, f)) for f in files if f.endswith(".xsd"))
        if not xsds:
            print("WARNING: No XSD files found in the specified directory")
        return xsds

    def load_schema(self, xsds: list[str]):
        try:
            print("Creating schema...")
            return xmlschema.XMLSchema(xsds)  # type: ignore
        except XMLSchemaParseError as e:
            print(LinterError(LinterErrorType.SCHEMA_ERROR, e))
        except Exception as e:
            print(e)
        sys.exit(1)

    def validate_xml(self, file: str | io.StringIO) -> LinterSuccess | LinterError:
        if self.schema is not None:
            try:
                self.schema.validate(file)
                return LinterSuccess(LinterSuccessType.BASE_MESSAGE)
            except XMLSchemaValidationError as e:
                return LinterError(LinterErrorType.VALIDATION_ERROR, e)
            except XMLResourceParseError as e:
                return LinterError(LinterErrorType.SYNTAX_ERROR, e)
            except Exception as e:
                return LinterError(LinterErrorType.UNKNOWN_ERROR, e)
        else:
            raise LinterError(LinterErrorType.SCHEMA_ERROR)

    def extract_base64_documents(self, data: DocumentRel) -> list[str]:
        # Assumes structure: data["DocumentRel"][...]["Document"]["Content"]
        docs: list[str] = []
        if "DocumentRel" in data:
            for rel in data.get("DocumentRel", []):
                doc = rel.get("Document", {})
                content: str | None = doc.get("Content", None)
                if content:
                    docs.append(content)
        return docs

    def validate_base64_documents(
        self, base64_docs: list[str]
    ) -> LinterError | LinterSuccess:
        # TODO: fix logic here
        for idx, encoded_doc in enumerate(base64_docs):
            try:
                decoded_xml = base64.b64decode(encoded_doc).decode("utf-8")
            except Exception as e:
                return LinterError(LinterErrorType.BASE64_ERROR, e)
            print(f"Validating embedded base64 XML document #{idx + 1}...")
            q = self.validate_xml(io.StringIO(decoded_xml))
            if isinstance(q, LinterError):
                return q
        return LinterSuccess(LinterSuccessType.DOCUMENT_SUCCESS)
