from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import importlib
from ext.routes import getMods
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/attach", StaticFiles(directory="attach"), name="attach")
##cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
##动态加载
#arr=["forum.index.forum","forum.index.forum_group","index.index.login","forum.index.forum_search"]
arr=getMods()
for module_name in arr:
#module_name="forum.index.forum"
    metaclass=importlib.import_module(module_name)
    app.include_router(metaclass.router)
    module_name="forum.index.forum_group"
    metaclass=importlib.import_module(module_name)
    app.include_router(metaclass.router)
