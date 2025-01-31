# MCP Server for LinkedIn

A Model Context Protocol (MCP) server for linkedin to apply Jobs and search through feed seamlessly. 

This uses Unoffical [Linkedin API Docs](https://linkedin-api.readthedocs.io/en/latest/api.html) for hitting at the clients Credentials.

---

# Configuration

After cloning the repo, adjust the `<LOCAL_PATH>` accordingly

```python
{
    "linkedin":{
        "command":"uv",
        "args": [
            "--directory",
            "<LOCAL_PATH>",
            "run",
            "linkedin.py"
        ]
    }   
}     

```

---

# Usage

I have been testing using [MCP-client](https://github.com/chrishayuk/mcp-cli) and found as the best one for testing your `MCP-Servers`.



