from letterboxd_pipeline.export import export_activity


def main():
    return export_activity(output_path="/data/pipelines/letterboxd/raw/activity.json")
