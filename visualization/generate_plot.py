# imports
import pathlib
import json
import graphviz
import pydot


if __name__ == "__main__":

    # set paths for .json file with taxonomy information and .png of taxonomy
    data_dir = "terms"
    data_path = pathlib.Path(pathlib.Path().resolve().parent, data_dir)
    out_path = pathlib.Path().resolve()
    
    json_filename = "taxonomy_for_annotations.json"
    json_filepath = pathlib.Path(data_path, json_filename)
    
    dot_filename = "taxonomy_for_annotations_plot"
    dot_filepath = pathlib.Path(out_path, dot_filename)
    
    # read from .json file
    with open(json_filepath, "r") as read_file:
        data = json.load(read_file)
    # list of categories (indicated by an ellipse)
    cat_list = [
        "sounds",
        "human",
        "nature",
        "mechanical",
        "music",
        "oral_nasal",
        "hands_arms",
        "feet_legs",
        "animal",
        "nonanimal",
    ]
    
    # draw taxonomy
    dot = graphviz.Digraph("taxonomy", comment="Taxonomy", graph_attr={"rankdir":"LR"})
    for key, value in data.items():
        if key == "sounds":
            dot.node(key, value["label"], shape="hexagon")
        elif key in cat_list:
            dot.node(key, value["label"], shape="ellipse")
        else:
            dot.node(key, value["label"], shape="box")
    
    for key, value in data.items():
        for parent in value["parents"]:
            if len(value["parents"]) > 1:
                dot.edge(parent, key, style="dashed")
            else:
                dot.edge(parent, key)
    # save PDF
    
    dot.render(dot_filepath, view=False)
    dot_filepath
    
    (graph,) = pydot.graph_from_dot_file(str(pathlib.Path(out_path, "taxonomy_for_annotations_plot")))
    graph.write_png(str(pathlib.Path(out_path, "taxonomy_for_annotations_plot.png")))
