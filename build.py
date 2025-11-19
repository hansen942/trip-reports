import os, glob, json, datetime

docs_dir = os.path.abspath('docs')

print("rebuilding index.md")

with open(os.path.join(docs_dir, 'index.md'), 'w+') as output:
    with open(os.path.join(docs_dir, 'template.md'), 'r') as template:
        for line in template.readlines():
            output.write(line)
        trips = []
        for trip_metadata_file_name in glob.glob(os.path.join(docs_dir, "*/metadata.json")):
            with open(trip_metadata_file_name) as trip_metadata_file:
                metadata = json.load(trip_metadata_file)
                split_path = os.path.split(trip_metadata_file_name)
                contents_path = os.path.join(split_path[0], "contents.md")
                contents_filename = os.path.relpath(contents_path, docs_dir)
                date = datetime.date.fromisoformat(metadata["date"])
                trips.append((date, metadata, contents_filename))
        read_date = lambda trip : trip[0]
        trips.sort(key=read_date)
        trip_count = 0
        for (date, metadata, contents_filename) in trips:
            trip_count += 1
            date_str = date.strftime("%a %d %b %Y")
            if metadata.get("end_date") is not None:
                date_str += " to "
                end_date = datetime.date.fromisoformat(metadata["end_date"])
                date_str += end_date.strftime("%a %d %b %Y")
            line = str(trip_count) + ". " + "[" + metadata["name"] + " - " + date_str + "](" + contents_filename + ")"
            if metadata.get("image_link") is not None:
                image_link = metadata["image_link"]
                line += " ![thumbnail-" + str(trip_count) + "](" + image_link + ")"
            line += "\n"
            output.write(line)
