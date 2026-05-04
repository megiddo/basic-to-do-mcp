#!/usr/bin/env python3
import argparse
import json
import sys
from todo_lib import (
    create_task, update_task, delete_task, get_task,
    create_update, update_update, delete_update,
    add_artifact, delete_artifact,
    get_tasks_by_urgency
)

def format_output(data, format_type):
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'markdown':
        if isinstance(data, list):
            if not data: return "No data found."
            cols = data[0].keys()
            header = "| " + " | ".join(cols) + " |"
            sep = "| " + " | ".join(["---"] * len(cols)) + " |"
            rows = []
            for item in data:
                rows.append("| " + " | ".join(str(item.get(c, "")) for c in cols) + " |")
            return "\n".join([header, sep] + rows)
        elif isinstance(data, dict):
            lines = [f"# {data.get('title', 'Task Detail')}"]
            for k, v in data.items():
                if k not in ['updates', 'subtasks', 'artifacts']:
                    lines.append(f"- **{k}**: {v}")
            
            if data.get('updates'):
                lines.append("\n## Updates")
                for u in data['updates']:
                    lines.append(f"- *{u['date']}*: {u['comment']}")
            
            if data.get('artifacts'):
                lines.append("\n## Artifacts")
                for a in data['artifacts']:
                    atype = a.get('type', 'Content')
                    content = a.get('content', '')
                    mtype = a.get('mimetype', '')
                    if atype == 'URL':
                        lines.append(f"- [Link]({content}) ({mtype})")
                    elif atype == 'File':
                        lines.append(f"- `File`: {content} ({mtype})")
                    else:
                        lines.append(f"- `Note`: {content} ({mtype})")
            
            if data.get('subtasks'):
                lines.append("\n## Subtasks")
                for s in data['subtasks']:
                    lines.append(f"- [{s['id']}] {s['title']}")
            return "\n".join(lines)
        return str(data)
    else: # plain
        if isinstance(data, list):
            return "\n".join(str(item) for item in data)
        return str(data)

def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--format", choices=['plain', 'json', 'markdown'], default='plain', help="Output format")

    parser = argparse.ArgumentParser(description="Multi-Agent To-Do Tool CLI", parents=[common_parser])
    parser.add_argument("--agent", required=True, help="Agent name/keyword for namespace resolution")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create Task
    p_create = subparsers.add_parser("create", parents=[common_parser], help="Create a task")
    p_create.add_argument("title_pos", nargs='?', help="Task title")
    p_create.add_argument("--title", dest="title_opt", help="Task title (optional if positional provided)")
    p_create.add_argument("--desc", help="Description")
    p_create.add_argument("--due", help="Due date (ISO format)")
    p_create.add_argument("--priority", choices=['low', 'medium', 'high', 'urgent'], default='medium')
    p_create.add_argument("--subtask-of", type=int, help="ID of parent task")
    
    # Update Task
    p_update = subparsers.add_parser("update", parents=[common_parser], help="Update a task")
    p_update.add_argument("id", type=int, help="Task ID")
    p_update.add_argument("--title", help="New title")
    p_update.add_argument("--desc", help="New description")
    p_update.add_argument("--due", help="New due date")
    p_update.add_argument("--status", choices=['created', 'in-progress', 'complete'])
    p_update.add_argument("--priority", choices=['low', 'medium', 'high', 'urgent'])
    
    # Delete Task
    p_delete = subparsers.add_parser("delete", parents=[common_parser], help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID")
    
    # Get Task
    p_get = subparsers.add_parser("get", parents=[common_parser], help="Get task details")
    p_get.add_argument("id", type=int, help="Task ID")
    
    # Create Update
    p_add_upd = subparsers.add_parser("add-update", parents=[common_parser], help="Add a comment/update to a task")
    p_add_upd.add_argument("id", type=int, help="Task ID")
    p_add_upd.add_argument("comment", help="Update comment")
    
    # Add Artifact
    p_add_art = subparsers.add_parser("add-artifact", parents=[common_parser], help="Add an artifact to a task")
    p_add_art.add_argument("id", type=int, help="Task ID")
    p_add_art.add_argument("content", help="Artifact content (URL, path, or text)")
    p_add_art.add_argument("--type", choices=['URL', 'Content', 'File'], default='Content', help="Type of artifact")
    p_add_art.add_argument("--mimetype", help="MIME type (e.g. application/pdf, image/png)")
    
    # Report
    p_report = subparsers.add_parser("report", parents=[common_parser], help="Get tasks by urgency")
    
    args = parser.parse_args()
    
    result = None
    if args.command == "create":
        title = args.title_opt or args.title_pos
        if not title:
            p_create.error("the following arguments are required: title")
        result = create_task(args.agent, title, args.desc, args.due, args.priority, args.subtask_of)
    elif args.command == "update":
        kwargs = {k: v for k, v in vars(args).items() if v is not None and k not in ['command', 'id', 'format', 'agent']}
        result = update_task(args.agent, args.id, **kwargs)
    elif args.command == "delete":
        result = delete_task(args.agent, args.id)
    elif args.command == "get":
        result = get_task(args.agent, args.id)
    elif args.command == "add-update":
        result = create_update(args.agent, args.id, args.comment)
    elif args.command == "add-artifact":
        result = add_artifact(args.agent, args.id, args.content, args.mimetype, args.type)
    elif args.command == "report":
        result = get_tasks_by_urgency(args.agent)
    else:
        parser.print_help()
        return

    print(format_output(result, args.format))

if __name__ == "__main__":
    main()
