import base64
import io
import os
import tempfile
import uncompyle6
from github import Github

GITHUB_KEY = os.environ["GITHUB_TOKEN"]
secrets = ["secrets.pyc", "config.pyc"]
g = Github(GITHUB_KEY)
repos  = g.get_organization(os.environ["ORG"]).get_repos(type="private")

items = []

for repo in repos:
	print (repo)
	try:
		contents = repo.get_contents("")
	except:
		continue
	for file_ in contents:
		try:
			extension = file_.name.split(".")[1]
		except IndexError:
			extension = None
		if file_.name in secrets or ( extension and extension  == "pyc"):
			items.append(file_)

if not items:
	print ("No files found, you are good!")


for item in items:
    print(f"DECOMPILING REPO https://github.com/{item.repository.full_name}")
    print(f"OWNER TYPE: {item.repository.owner.type}")
    try:
        contents = base64.b64decode(item.content)
        with tempfile.NamedTemporaryFile(suffix=".pyc") as f:
            f.write(contents)
            f.seek(0)

            out = io.StringIO()
            uncompyle6.decompile_file(f.name, out)
            out.seek(0)
            print(out.read())
    except Exception as e:
        print(e)
        print(f"COULD NOT DECOMPILE REPO https://github.com/{item.repository.full_name}")
        continue
    print("\n\n\n")
