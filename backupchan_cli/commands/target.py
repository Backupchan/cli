import requests
from backupchan_cli.config import Config
from backupchan_cli import utility
from backupchan import API, BackupType, BackupRecycleCriteria, BackupTarget, BackupRecycleAction

#
#
#

def setup_subcommands(subparser):
    list_cmd = subparser.add_parser("list", help="List all targets")
    list_cmd.set_defaults(func=do_list)

#
# Value to human-readable string conversions and lookup tables
#

HR_TYPES = {
    BackupType.SINGLE: "Single file",
    BackupType.MULTI: "Multiple files"
}

HR_RECYCLE_ACTIONS = {
    BackupRecycleAction.DELETE: "Delete",
    BackupRecycleAction.RECYCLE: "Recycle"
}

def hr_recycle_criteria(target: BackupTarget) -> str:
    if target.recycle_criteria == BackupRecycleCriteria.NONE:
        return "None"
    elif target.recycle_criteria == BackupRecycleCriteria.AGE:
        return f"After {target.recycle_value} days"
    elif target.recycle_criteria == BackupRecycleCriteria.COUNT:
        return f"After {target.recycle_value} copies"
    return "(broken value)"

#
# backupchan target list
#

def do_list(args, config: Config, api: API):
    try:
        targets = api.list_targets()
    except requests.exceptions.ConnectionError:
        utility.failure_network()

    for index, target in enumerate(targets):
        spaces = " " * (len(str(index + 1)) + 1)
        print(f" {index + 1}. |  {target.name}")
        print(f" {spaces} | ID: {target.id}")
        print(f" {spaces} | Type: {HR_TYPES[target.target_type]}")
        print(f" {spaces} | Recycle criteria: {hr_recycle_criteria(target)}")
        if target.recycle_criteria != BackupRecycleCriteria.NONE:
            print(f" {spaces} | Recycle action: {HR_RECYCLE_ACTIONS[target.recycle_action]}")
        print(f" {spaces} | Location: {target.location}")
        print(f" {spaces} | Name template: {target.name_template}")
        print("=========")
