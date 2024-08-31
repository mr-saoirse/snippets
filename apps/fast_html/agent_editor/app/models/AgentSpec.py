"""BlockParser is for parsing editorjs block output """

from fasthtml.common import *
from typing import Dict, Any
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class FunctionLinks(BaseModel):
    url: HttpUrl
    description: Optional[str]
    name: Optional[str]
    
    def __ft__(cls):
        """provide the divs that provide the functions that are called"""
        return Div(*[H4(cls.name), P(cls.description), P((I(cls.url)))],cls='agent_function_links')

class SchemaTables(BaseModel):
    name: str
    rows: List[List[str]]
    
    def __ft__(cls):
        """return a table of fields"""
        data_rows = [Tr(*[Td(c) for c in r]) for r in cls.rows]
        header_rows = [Tr(*[Td(B(c)) for c in ['field name', 'description', 'type']])   ]
        return Div(*[H3(cls.name), Table(*
            header_rows + data_rows
        )])

class AgentSpec(BaseModel):
    """
    this model parsers and can be used to render blocks from the EditorJS
    
    In jupyter remember you can display this with the show method
    
    from fasthtml.components import show
    
    """
    name: str
    description: Optional[str]
    tables: List[SchemaTables] = []
    links: List[FunctionLinks] = []
     
    def __ft__(cls):
        """"""
        return Div(*[H1(cls.name), P(cls.description), *cls.tables, *cls.links], cls='editor')
        
    def _repr_html_(cls):
        """the default here is to show the object in jupyter as html.
        this might not always be what you want but i prefer to use the model_dump to see the data instead of the class repr.
        but if you want to see it you can use the repr(cls)
        """
        return to_xml(cls)
    
    @classmethod  
    def parse_agent_data(cls, blocks: List[Dict[str, Any]]) -> "AgentSpec":
        """
        block data from editor.js is parsed and can then be rendered as a div
        """
        name = None
        description = None
        tables = []
        links = []

        current_table_name = None

        for block in blocks:
            block_type = block.get('type')
            block_data = block.get('data', {})

            if block_type == 'header':
                level = block_data.get('level')
                text = block_data.get('text', '')

                if level == 1:
                    name = text
                elif level == 3:
                    #the last level three is assumed to be the type name
                    current_table_name = text
                else:
                    current_table_name = None

            elif block_type == 'paragraph':
                description = block_data.get('text', '')

            elif block_type == 'table' and current_table_name:
                # Extract table content, excluding the title row
                content = block_data.get('content', [])
                if content:
                    table_rows = content[1:]  # Exclude the title row
                    tables.append(SchemaTables(name=current_table_name, rows=table_rows))

            elif block_type == 'linkTool':
                link_data = block_data.get('link')
                meta = block_data.get('meta', {})
                title = meta.get('title', '')
                link = FunctionLinks(url=link_data, description=meta.get('description', ''), name=title)
                links.append(link)

        return cls(name=name, description=description, tables=tables, links=links)