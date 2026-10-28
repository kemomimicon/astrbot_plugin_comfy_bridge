import ast,hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
for p in root.rglob("*.py"):
 if ".git" not in p.parts:compile(p.read_text(encoding="utf-8-sig"),str(p),"exec")
for p in root.rglob("*.json"):
 if ".git" not in p.parts:json.loads(p.read_text(encoding="utf-8-sig"))
schema=json.loads((root/"_conf_schema.json").read_text(encoding="utf-8-sig"))
for key in ("workflow_path","hq_workflow_path","refine_workflow_path","reverse_workflow_path"):
 p=root/schema[key]["default"];assert p.is_file(),key
 graph=json.loads(p.read_text(encoding="utf-8-sig"))
 for node in graph.values():
  for v in node.get("inputs",{}).values():
   if isinstance(v,list) and len(v)==2 and isinstance(v[0],str):assert v[0] in graph
for file in ("anima_random_prompt_pool.json","kp_prompt_pool.json"):
 assert json.loads((root/"data"/file).read_text(encoding="utf-8-sig"))["prompts"]==[]
manifest=json.loads((root/"qq-package-manifest.json").read_text(encoding="utf-8-sig"))
for name,h in manifest["files"].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,name
assert "repo: \"https://github.com/kemomimicon/astrbot_plugin_comfy_bridge\"" in (root/"metadata.yaml").read_text(encoding="utf-8-sig")
print("PASS: syntax, JSON, default workflow links, empty public pools, exact source hashes")
