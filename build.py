import os, glob, json

docs_dir = os.path.abspath('docs')

print("rebuilding index.md")

with open(os.path.join(docs_dir, 'index.md'), 'w+') as output:
    with open(os.path.join(docs_dir, 'template.md'), 'r') as template:
        for line in template.readlines():
            output.write(line)
        trip_count = 1
        for trip_metadata_file_name in glob.glob(os.path.join(docs_dir, "*/metadata.json")):
            with open(trip_metadata_file_name) as trip_metadata_file:
                metadata = json.load(trip_metadata_file)
                split_path = os.path.split(trip_metadata_file_name)
                contents_path = os.path.join(split_path[0], "contents.md")
                contents_filename = os.path.relpath(contents_path, docs_dir)
                line = str(trip_count) + ". " + "[" + metadata["name"] + " - " + metadata["date"] + "](" + contents_filename + ")\n"
                output.write(line)
