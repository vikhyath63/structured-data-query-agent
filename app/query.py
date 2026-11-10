from typing import Any
OPS={"eq","ne","gt","gte","lt","lte","contains"}
def query_records(records:list[dict[str,Any]],filters:dict[str,dict]|None=None,group_by:str|None=None,aggregate:str|None=None,value_field:str|None=None):
    if not records: return {"fields":[],"count":0,"rows":[],"aggregation":{}}
    fields=set().union(*(r.keys() for r in records)); filters=filters or {}
    for field,rule in filters.items():
        if field not in fields: raise ValueError(f"Unknown field: {field}")
        if rule.get("op") not in OPS: raise ValueError(f"Unsupported operator for {field}")
    def match(row,field,rule):
        a=row.get(field); b=rule.get("value"); op=rule["op"]
        try:
            if op=="eq": return a==b
            if op=="ne": return a!=b
            if op=="contains": return str(b).lower() in str(a).lower()
            if op=="gt": return a>b
            if op=="gte": return a>=b
            if op=="lt": return a<b
            if op=="lte": return a<=b
        except TypeError: return False
    rows=[r for r in records if all(match(r,f,rule) for f,rule in filters.items())]
    summary={}
    if group_by:
        if group_by not in fields: raise ValueError(f"Unknown group field: {group_by}")
        if aggregate not in {"count","sum","avg"}: raise ValueError("aggregate must be count, sum or avg")
        if aggregate!="count" and value_field not in fields: raise ValueError("A valid value_field is required")
        groups={}
        for row in rows: groups.setdefault(str(row.get(group_by)),[]).append(row)
        for key,items in groups.items():
            vals=[float(x[value_field]) for x in items] if value_field else []
            summary[key]=len(items) if aggregate=="count" else (sum(vals) if aggregate=="sum" else (sum(vals)/len(vals) if vals else 0))
    return {"fields":sorted(fields),"count":len(rows),"rows":rows,"aggregation":summary}
