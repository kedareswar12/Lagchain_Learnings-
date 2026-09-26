# simple function that can help us to inject hitl to any agent in langchain


from langchain.agents.middleware import HumanInTheLoopMiddleware
def build_hitl_middelware() -> HumanInTheLoopMiddleware :
    return HumanInTheLoopMiddleware(
        interrupt_on= {
            "read_file" : False , # no hitl
            "list_files" : False,
            "list_jobs": False, # no hitl for list_jobs tool
            "stop_job": False, # no hitl for stop_job tool
            "run_command": {
                "allowed_decisions": ["approve", "edit", "reject"],
                "description": "Run a bash command in the current working directory (host machine not a sandbox)"
            },
            "write_files" : 
            {
                "allowed_decisions" : ["approve" , "edit", "reject", "respond"],
                "description" : "write or overwrite a file on a disk "        
            },
            "edit_file" :
             {
                "allowed_decisions" : ["approve" , "edit", "reject", "respond"],
                "description" : "Edit an exsisting file "           
             }
        },
        description_prefix= " Coding agent needs your approvement to move ahed"
    )