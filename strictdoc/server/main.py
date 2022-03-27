import os
import uuid
from typing import List, Optional

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

from strictdoc.backend.sdoc.models.inline_link import InlineLink
from strictdoc.backend.sdoc.models.requirement import Requirement
from strictdoc.backend.sdoc.models.section import Section
from strictdoc.backend.sdoc.reader import SDReader
from strictdoc.core.document_iterator import DocumentCachingIterator
from strictdoc.export.rst.rst_to_html_fragment_writer import RstToHtmlFragmentWriter


class RequirementModel(BaseModel):
    title: Optional[str]
    statement: Optional[str]


class RequirementsModel(BaseModel):
    requirements: List[RequirementModel]


class NodeUpdateModel(BaseModel):
    text_source: str
    text_html: Optional[str]


DOC_FILE = "docs/strictdoc.sdoc"


def create_uid() -> str:
    return str(uuid.uuid4())


def create_requirements_router() -> APIRouter:
    router = APIRouter()

    document = SDReader().read_from_file(DOC_FILE)

    @router.get("/requirements", response_class=JSONResponse)
    def get_requirements():
        print(os.getcwd())
        requirements = []

        iterator = DocumentCachingIterator(document)
        for node in iterator.all_content():
            if isinstance(node, Requirement):
                requirement_dict = {
                    "type": "REQUIREMENT",
                    "uid": create_uid(),
                    "title": node.title,
                    "statement_source": RstToHtmlFragmentWriter.write(
                        node.get_statement_single_or_multiline()
                    ),
                    "statement_html": RstToHtmlFragmentWriter.write(
                        node.get_statement_single_or_multiline()
                    )
                }
                if node.has_meta:
                    fields = []
                    for meta_field in node.enumerate_meta_fields():
                        field_dict = {
                            "uid": create_uid(),
                            "title": meta_field[0],
                            "value": meta_field[1]
                        }
                        fields.append(field_dict)
                    requirement_dict["fields"] = fields
                requirements.append(requirement_dict)
            elif isinstance(node, Section):
                section_dict = {
                    "type": "SECTION",
                    "uid": create_uid(),
                    "title": node.title,
                }
                requirements.append(section_dict)
                if len(node.free_texts) > 0:
                    free_text = ""
                    for part in node.free_texts[0].parts:
                        if isinstance(part, str):
                            free_text += part
                        elif isinstance(part, InlineLink):
                            free_text += part.link
                    free_text_dict = {
                        "type": "FREETEXT",
                        "uid": create_uid(),
                        "text_source": free_text,
                        "text_html": RstToHtmlFragmentWriter.write(
                            free_text
                        )
                    }
                    requirements.append(free_text_dict)

        return {"requirements": requirements}

    @router.put("/nodes", response_class=JSONResponse)
    def put_nodes(node: NodeUpdateModel):
        node.text_html = RstToHtmlFragmentWriter.write(
            node.text_source
        )
        return node

    return router


def create_app(_):
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(create_requirements_router())

    @app.get("/")
    def get_root():
        return {"Hello": "World"}

    return app


def strictdoc_production_app():
    # database = RealDatabase()
    # database.use_real_database()
    return create_app(None)
