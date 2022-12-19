from git import Repo as gitm
import properties as pr

is_debug = True


def read_repos_names(path):
    with open(path) as f:
        names = [line.rstrip() for line in f]
        names = list(set(names))
        return names


def clone_repos(name_set, path_to_save, git_url):
    report = []
    for i in range(len(name_set)):
        try:
            gitm.clone_from(url=git_url + name_set[i], to_path=path_to_save + name_set[i])
        except Exception as ex:
            if is_debug:
                print(f"An exception of type {type(ex).__name__} occurred. Arguments:\n{ex.args!r}")
            report.append((name_set[i], "FAIL"))
            continue
        report.append((name_set[i], "OK"))
    return report


def save_report_to_file(save_path, report):
    with open(save_path, "w") as f:
        f.write("Report\n")
        for record in report:
            f.write(f"{record[0]} (status: {record[1]})\n")


if __name__ == "__main__":
    repo_names = read_repos_names(pr.repos_names_path)
    if is_debug:
        print("Repository names are set from file:")
        for num in range(len(repo_names)):
            print(f"Repo №{num + 1}: {repo_names[num]}")

    report = clone_repos(repo_names, pr.repo_clone_path, pr.base_url)
    save_report_to_file(pr.report_save_path, report)
