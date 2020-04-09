import argparse
from ccl_scratch_tools import Scraper

def get_arguments():
    parser = argparse.ArgumentParser(description="Download Scratch projects.")

    # Arguments related to input
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("-s", dest="studio", nargs="*", help="Studio ID. Will scrape all projects from the studio with the given ID.")
    inputs.add_argument("-p", dest="project", nargs="*", help="Project ID. Will scrape one project for each ID provided.")
    inputs.add_argument("-f", dest="studio_list", nargs="*", help="File name for a line-separated list of studio URLs (or IDs). Will scrape all projects in all studios.")
    inputs.add_argument("-g", dest="project_list", nargs="*", help="File name for a line-separated list of project URLs (or IDs). Will scrape all projects.")

    # Arguments related to output
    parser.add_argument("-d", dest="output_directory", help="Output directory. Will save output to this directory, and create the directory if doesn’t exist.")
    parser.add_argument("-n", dest="output_name", help="Name of the output JSON file, if only a single output file is desired. Otherwise, will save projects to individual JSON files.")
    parser.add_argument("-b", dest="studio_subdirectories", action="store_const", const=True, default=False, help="If downloading a list of studios, add this flag to save projects to subdirectories named for the studio ID.")

    return parser.parse_args()

def get_project_ids(scrape, arguments):
    """Given input arguments, return a set of all the project IDs."""
    projects = list()
    projects_to_studio = dict()
    if arguments.project is not None:
        for p in arguments.project:
            projects.append(scrape.get_id(p))
    elif arguments.studio is not None:
        for s in arguments.studio:
            projects += scrape.get_projects_in_studio(scrape.get_id(s))
    elif arguments.project_list is not None:
        for p in arguments.project_list:
            projects += scrape.get_ids_from_file(p)
    elif arguments.studio_list is not None:
        for s in arguments.studio_list:
            studios = scrape.get_ids_from_file(s)
            for studio in studios:
                studio_projects = scrape.get_projects_in_studio(studio)
                projects += studio_projects
                if arguments.studio_subdirectories:
                    for p in studio_projects:
                        projects_to_studio[p] = studio

    return set(projects), projects_to_studio

def main():
    scrape = Scraper()
    arguments = get_arguments()
    projects, projects_to_studio = get_project_ids(scrape, arguments)

    if arguments.output_directory is None:
        scrape.download_projects(projects, projects_to_studio, file_name=arguments.output_name)
    else:
        scrape.download_projects(projects, projects_to_studio, output_directory=arguments.output_directory, file_name=arguments.output_name)


if __name__ == "__main__":
    main()